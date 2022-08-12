import json
from pickle import TRUE
from sqlalchemy.orm import Session
import requests
from time import sleep

from fastapi import BackgroundTasks
from celery import current_task

from .. import models, schemas

def celery_on_message(body):
    print(body)

def background_on_message(task):
    print(task.get(on_message=celery_on_message, propagate=False))

def get_dog_by_name(db: Session, name: str):
    return db.query(models.Dog).filter(models.Dog.name == name).first()

def get_dogs_by_name(db: Session, name: str):
    if (name=="is_adopted"):
        return db.query(models.Dog).filter(models.Dog.is_adopted == "t").all()
    else:
        return db.query(models.Dog).filter(models.Dog.name == name).all()

def get_dog_adopted(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted == "t").all()

def get_dogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dog).offset(skip).limit(limit).all()

def create_dog(db: Session, dog: schemas.DogCreate):
    for i in range(1, 4):
        sleep(1)
        if not current_task:
            print("Creando Dog "+dog.name+"...")
        elif current_task.request.id is None:
            print("Llamado asincronicamente")
        else:
            print("dispatched")

    res1=requests.get('https://dog.ceo/api/breeds/image/random')
    url=res1.text
    urldata=json.loads(url)

    db_dog = models.Dog(name=dog.name, picture=urldata['message'],
                        is_adopted=dog.is_adopted,
                        create_date=dog.create_date,
                        id_user=dog.id_user)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog

def update_dog(name:str, db: Session, dog: schemas.DogCreate):
    res1=requests.get('https://dog.ceo/api/breeds/image/random')
    url=res1.text
    urldata=json.loads(url)
    dog.picture=urldata['message']
    resp=db.query(models.Dog).filter(models.Dog.name == name).first()
    if resp is None:
        return None
    else:
        db.query(models.Dog).filter(models.Dog.name == name).update({"name":dog.name,
                                                                    "picture":urldata['message'],
                                                                    "is_adopted":dog.is_adopted,
                                                                    "create_date":dog.create_date,
                                                                    "id":dog.id, "id_user":dog.id_user})
        db.commit()
        db.close()
        return dog

def delete_by_name(db: Session, name: str):
    dog=db.query(models.Dog).filter(models.Dog.name == name).first()
    if dog is None:
        return None
    else:
        db.delete(dog)
        db.commit()
        return 0
    
def send_file(file: bytes):
    url = 'https://gttb.guane.dev/api/files'
    myobj = {'Content-Type': 'multipart/form-data','accept': 'application/json'}
    myfile={'file':file}
    res1=requests.post(url,json=myobj,files=myfile)
    for t in res1: c=1;
    return {t} 