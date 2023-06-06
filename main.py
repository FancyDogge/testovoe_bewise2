from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from db.database import get_db
from uuid import uuid4
from db.models import User
from sqlalchemy.orm import Session


app = FastAPI()


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    user_id: int
    access_token: str


@app.post("/users", response_model=UserResponse)
def create_user(create_model: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == create_model.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    access_token = uuid4()
    user = User(username=create_model.username, access_token=access_token)
    db.add(user)
    db.commit()
    return UserResponse(user_id=user.id, access_token=user.access_token)