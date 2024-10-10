from datetime import timedelta, datetime, timezone
from typing import Dict, Any, Annotated
from fastapi import FastAPI, Depends, HTTPException,status
from models.user import User, UserCreate, UserResponse, UserLogin, TokenData, UserOtp
from config.database import get_db
from sqlalchemy.orm import Session
from utils.cachings import write_to_redis, read_from_redis, clear_redis_data
from utils.messaging import send_messages
from utils.otp import generate_otp
from utils.response import create_response, create_error_response
import  jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORYTHM = os.getenv('ALGORITHM')


def create_access_token(data: dict, expires_in: timedelta | None = None):
    to_encode = data.copy()

    if isinstance(expires_in, str):
        expires_in = timedelta(minutes=int(expires_in))

    if expires_in:
        expire = datetime.now(timezone.utc) + expires_in
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=720)

    to_encode.update({'exp': expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORYTHM)
    return encoded_jwt

def register_user(user:UserCreate, session:Session) -> HTTPException | UserResponse | Any:
    try:
        existing_user = session.query(User).filter(
            (User.email == user.email) | (User.phone_number == user.phone_number)
        ).first()
        if existing_user:
            if existing_user.email == user.email:
                raise HTTPException(status_code=400, detail="Email already registered")
            else:
                raise HTTPException(status_code=400, detail="Phone number already registered")

        new_user = User(name=user.name, email=user.email, phone_number=user.phone_number)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return UserResponse(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            phone_number=new_user.phone_number,
           is_verified = new_user.is_verified,
           created_at = new_user.created_at,
        )

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


def login_user(user:UserLogin, session:Session) -> HTTPException | UserResponse | Any:
    try:
        existing_user = session.query(User).filter(User.phone_number == user.phone_number).first()
        if not existing_user:
                raise HTTPException(status_code=400, detail="User Not Found")

        otp = generate_otp()
        write_to_redis(f"user-otp-{existing_user.phone_number}", otp)

        send_messages(existing_user.phone_number, f'This is your OTP {otp}')

        return  existing_user

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


def resend_otp(user: UserLogin, session: Session) -> HTTPException | UserResponse | Any:
    try:
        existing_user = session.query(User).filter(User.phone_number == user.phone_number).first()
        if not existing_user:
            raise HTTPException(status_code=400, detail="User Not Found")

        otp = generate_otp()
        write_to_redis(f"user-otp-{existing_user.phone_number}", otp)

        send_messages(existing_user.phone_number, f'This is your OTP {otp}')

        return existing_user

    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))




def verify_otp( user: UserOtp) -> HTTPException | Any:
    try:

        get_otp = read_from_redis(f"user-otp-{user.phone_number}")

        if get_otp == user.otp:
            access_token = create_access_token(data={'sub': user.phone_number})
            clear_redis_data(f"user-otp-{user.phone_number}")

            return access_token
        else:
            return  None

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"OTP verification error: {str(err)}")



def get_user(phone_number: str, db: Session) :
    existing_user = db.query(User).filter(User.phone_number == phone_number).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return existing_user




def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
   try:
       token = credentials.credentials

       payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM], leeway=10)

       phone_number: str = payload.get("sub")


       if phone_number is None:
           raise
       token_data = TokenData(phone_number=phone_number)

       user = get_user(phone_number=token_data.phone_number, db=db)

       if user is None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

       return user

   except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User number not found")


