from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends, HTTPException,status
from models.user import User, UserCreate, UserResponse, UserLogin, UserOtp
from sqlalchemy.orm import Session
from config.database import get_db
from models.user import UserResponse, UserCreate
from services.user_service import register_user, login_user, verify_otp, get_current_user, resend_otp
from utils.response import create_response

router = APIRouter()


@router.post('/users/signup', response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(user, db)
        return new_user

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



@router.post('/users/login', response_model=UserResponse, status_code=200)
def create_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        user = login_user(user, db)
        return user

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post('/users/verify-otp',  status_code=200)
def verify_user_otp(user: UserOtp):
    try:
        access_token = verify_otp(user)
        return access_token

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post('/users/resend-otp', response_model=UserResponse, status_code=200)
def resend_user_otp(user: UserLogin,  db: Session = Depends(get_db)):
    try:
        otp = resend_otp(user, db)
        return otp

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))



@router.get('/users/me', response_model=UserResponse, status_code=200)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user