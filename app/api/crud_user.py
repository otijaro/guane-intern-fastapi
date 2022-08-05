import json
from pickle import TRUE
from sqlalchemy.orm import Session
import requests
from passlib.context import CryptContext

from .. import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_name(db: Session, name: str):
    print(name)
    resp=db.query(models.User).filter(models.User.name == name).all()
    return resp

def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()
    
def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


#To assign a password to Token
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_users_by_lastname(db: Session, last_name):
    return db.query(models.User).filter(models.User.last_name == last_name).all()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    password=pwd_context.hash(user.hashed_password)
    db_user = models.User(name=user.name, last_name=user.last_name,
                          email=user.email, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(id:int, db: Session, user: schemas.User):
    resp=db.query(models.User).filter(models.User.id == id).first()
    if resp is None:
        return None
    else:
        password=pwd_context.hash(user.hashed_password)
        user.hashed_password=password
        db.query(models.User).filter(models.User.id == id).update({"name":user.name,
                                                                    "last_name":user.last_name,
                                                                    "email":user.email,
                                                                    "hashed_password":user.hashed_password,
                                                                    "id":id})
        db.commit()
        db.close()
        return user

def delete_by_id(db: Session, id: int):
    user=db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        return None
    else:
        db.delete(user)
        db.commit()
        return 0