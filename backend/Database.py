from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


sqlalchemy_database_url = os.getenv("DATABASE_URL")

engine = create_engine(
    sqlalchemy_database_url , connect_args = {"check_same_thread" : False}
)

sessionlocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)

base = declarative_base()