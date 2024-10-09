from typing import Dict, Any

from fastapi import FastAPI, Depends, HTTPException,status
from models.user import User, UserCreate, UserResponse
from config.database import get_db
from sqlalchemy.orm import Session

from utils.response import create_response, create_error_response


def register_user(user:UserCreate, session:Session) -> HTTPException | UserResponse | Any:
    # try:
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

    # except Exception as err:
    #     return create_error_response(err, 'Error', 500)

