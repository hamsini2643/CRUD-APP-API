from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from dotenv import load_dotenv
import os

from sqlalchemy.ext.declarative import declarative_base

#load_dotenv()
#engine=create_engine(os.getenv(DATABASE_CONNECTION_STRING),echo=True)
engine=create_engine("postgresql://postgres:Jasmine@localhost/Person",echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(engine)