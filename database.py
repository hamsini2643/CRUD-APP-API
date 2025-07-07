from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


# Retrieve the connection string
DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")
print(f"Database Connection String: {DATABASE_CONNECTION_STRING}")


#data = os.getenv(DATABASE_CONNECTION_STRING)
#print(data)

engine = create_engine(DATABASE_CONNECTION_STRING, echo=True)

#engine=create_engine(DATABASE_CONNECTION_STRING, echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()