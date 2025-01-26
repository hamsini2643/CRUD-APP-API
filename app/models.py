from sqlalchemy import String, Integer, Column, Boolean, ForeignKey, TIME

from database import Base,engine
def create_tables():
    Base.metadata.create_all(engine)
class Person(Base):
    __tablename__='person'
    id=Column(Integer,primary_key=True,  index=True, autoincrement=True)
    firstname=Column(String(40),nullable=False)
    lastname=Column(String(40),nullable=False)
    is_male=Column(Boolean)
    password_hash = Column(String(128), nullable=True)  # Add a password hash column
class Slots(Base):
    __tablename__='slots'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column(String(10), nullable=False)
    end_time = Column(String(10), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)  # Foreign key reference to 'person' table    