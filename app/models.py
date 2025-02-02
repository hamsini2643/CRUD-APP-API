from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, TIME

from database import Base,engine
def create_tables():
    Base.metadata.create_all(engine)
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True,  index=True, autoincrement=True)
    
    firstname=Column(String(40),nullable=False)
    lastname=Column(String(40),nullable=False)
    gender=Column(String(10), nullable=False)
    password_hash = Column(String(128), nullable=True)  # Add a password hash column
class Slots(Base):
    __tablename__='slots'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  