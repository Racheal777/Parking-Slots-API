
from sqlalchemy.ext.declarative import declarative_base
from  sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()



DATABASE_URL = f"postgresql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOSTNAME')}/{os.getenv('DATABASE')}"


engine = create_engine(DATABASE_URL)

SessionMaker = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()



def get_db():
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()
