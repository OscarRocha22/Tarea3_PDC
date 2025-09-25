import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List, Optional


import models
from database import engine, SessionLocal

# ----- Cargar variables de entorno (.env) -----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----- Iniciar app -----
app = FastAPI(title="users API", version="1.0.0")

# ----- Crear tablas -----
models.Base.metadata.create_all(bind=engine)

# ----- Dependencia DB -----
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----- Seguridad por header -----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ----- Esquema Pydantic -----
class UserSchema(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Optional[int] = None
    recommendations: List[str]
    ZIP: Optional[str] = None

# ----- Endpoints -----
@app.post("/api/v1/users/", tags=["users"])
def create_user(user: UserSchema, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    existing_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already exists")

    user_model = models.User(
        user_name=user.user_name,
        user_id=user.user_id,
        user_email=user.user_email,
        age=user.age,
        recommendations=",".join(user.recommendations),
        ZIP=user.ZIP
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = ",".join(user.recommendations)
    user_model.ZIP = user.ZIP

    db.commit()
    db.refresh(user_model)
    return user_model

@app.get("/api/v1/users/{user_id}", tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user_model

@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    db.delete(user_model)
    db.commit()
    return {"deleted_id": user_id}
