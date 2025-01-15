from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
#import os
#from dotenv import load_dotenv


#load_dotenv()
#engine=create_engine(os.get_env(DATABASE_CONNECTION_STRING),echo=True)
engine=create_engine("postgresql://postgres:Jasmine@localhost/Person",echo=True)

Base=declarative_base()
SessionLocal=sessionmaker(engine)