from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    picture = Column(String)
    is_adopted = Column(Boolean, default=True)
    create_date= Column(DateTime)
    #items = relationship("Item", back_populates="owner")

    id_user =  Column(Integer, ForeignKey("users.id"))
    owner= relationship("User",back_populates="dogs")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    last_name = Column( String)
    email = Column(String)
    hashed_password= Column(String)
    dogs = relationship("Dog", back_populates="owner")
