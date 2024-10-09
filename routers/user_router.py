
from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends, HTTPException,status
from models.user import User, UserCreate, UserResponse
from sqlalchemy.orm import Session
from config.database import get_db
from models.user import UserResponse, UserCreate
from services.user_service import  register_user
from utils.response import create_response

router = APIRouter()




@router.post('/users', response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(user, db)
        return new_user

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

