from datetime import datetime, timedelta
from typing import Union
from pickle import TRUE
from typing import List
from urllib import response

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from . import crud_dog, crud_user, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI, Docker, and Celery")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Token words
SECRET_KEY="a804700940cb7db09d0fab1f1c4c9f35f6c6c9f50e00a303cfc723cd5f818c66"
ALGORITHM="HS256"
ACCES_TOKEN_EXPIRE_MINUTES=30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, name: str, password: str):
    user = crud_user.get_users_by_name(db, name)
    if not user:
        return False
    if not crud_user.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session= Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_users_by_name(db, name=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#endpoints
@app.post("/api/dogs/", response_model=schemas.Dog)
async def create_dog(dog: schemas.Dog, db: Session = Depends(get_db),current_user:schemas.User = Depends(get_current_user)):
    db_dog = crud_dog.get_dog_by_name(db, name=dog.name)
    if db_dog:
        raise HTTPException(status_code=400, detail="Nombre ya registrado")
    return crud_dog.create_dog(db=db, dog=dog)


@app.get("/api/dogs/{name}", response_model=List[schemas.Dog])
def read_dog(name: str, db: Session = Depends(get_db)):
    if (name=="is_adopted"):
        db_dog=crud_dog.get_dog_adopted(db)
    else:
        db_dog = crud_dog.get_dogs_by_name(db, name=name)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Nombre no encontrado")
    return db_dog


@app.get("/api/dogs/", response_model=List[schemas.Dog])
def read_dogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dogs = crud_dog.get_dogs(db, skip=skip, limit=limit)
    return dogs

@app.put("/api/dogs/{name}", response_model=schemas.Dog)
def update_dog(name: str, dog: schemas.Dog, db: Session = Depends(get_db)):
    dogs = crud_dog.update_dog(name, db, dog)
    if dogs is None:
        raise HTTPException(status_code=404, detail = "Nombre no encontrado")
    else:
        return dogs

@app.delete("/api/dogs/{name}", response_model = List[schemas.Dog])
def read_dogs(name: str, db: Session = Depends(get_db)):
    db_dog = crud_dog.delete_by_name(db, name = name)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog no encontrado")
    else:
        raise HTTPException(status_code=201, detail="Dog "+name+" borrado")

#Token signin
@app.post("/api/user/signin", response_model = schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                    db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/user/", response_model = schemas.UserBase)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    resp=crud_user.create_user(db=db, user=user)
    return user

@app.get("/api/users/{name}", response_model = List[schemas.UserBase])
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_name(db, name=name)
    if db_user==[]:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.get("/api/user/{id}", response_model = schemas.UserBase)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.get("/api/users/", response_model=List[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/api/user/{id}", response_model=schemas.UserBase)
def update_user(id: int, user: schemas.User, db: Session = Depends(get_db)):
    resp=crud_user.update_user(id,db=db,user=user)
    return resp

@app.delete("/api/user/{id}", response_model=List[schemas.User])
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud_user.delete_by_id(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        raise HTTPException(status_code=201, detail="Usuario con id "+str(id)+" eliminado")

@app.post("/api/files/")
async def upload_file(file: bytes = File()):
    if not file:
        return {"message": "No upload file sent"}
    else:
        res_api_guane=crud_dog.send_file(file)
        return res_api_guane