from fastapi import FastAPI
from config.database import Base, engine, SessionMaker
import models
from  routers.user_router import router as user_router
from jwt.exceptions import InvalidTokenError

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router, prefix='/api/v1')

@app.get("/")
def read_root():
    return {"Hello": "World"}