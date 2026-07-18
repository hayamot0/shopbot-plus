from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
engine=create_engine(os.getenv("DATABASE_URL"))

SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()