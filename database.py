from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from dotenv import load_dotenv
import os

from sqlalchemy.ext.declarative import declarative_base

#load_dotenv()
#engine=create_engine(os.getenv(DATABASE_CONNECTION_STRING),echo=True)
host = "127.0.0.1"
user = "postgres"
password = "Jasmine"
db_name = "Person"
DATABASE_CONNECTION_STRING=f"postgresql://{user}:{password}@{host}/{db_name}"
engine=create_engine(DATABASE_CONNECTION_STRING, echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()