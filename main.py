import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request, Query
from fastapi.responses import FileResponse
from uuid import uuid4
from sqlalchemy.orm import Session
from pydub import AudioSegment

from db.database import get_db
from db.models import User, AudioRecord
from schemas import UserCreate, UserResponse, AudioRecordResponse


app = FastAPI()


@app.post("/users", response_model=UserResponse)
def create_user(create_model: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == create_model.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    access_token = str(uuid4())
    user = User(username=create_model.username, access_token=access_token)
    db.add(user)
    db.commit()
    return UserResponse(user_id=user.id, access_token=user.access_token)


@app.post("/record", response_model=AudioRecordResponse)
def add_audio_record(
    request: Request,
    user_id: int,
    access_token: str,
    audio_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id, User.access_token == access_token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    audio_id = uuid4()
    os.makedirs("recordings", exist_ok=True)
    file_path = f"recordings/{audio_id}.mp3"

    # конвертируем wav запись в mp3
    audio = AudioSegment.from_file(audio_file.file, format="wav")
    audio.export(file_path, format="mp3")

    # Открываем mp3 файл как binary данные, которые будут хранится в моделе AudioRecord
    with open(file_path, "rb") as file:
        audio_data = file.read()

    # Сохраняем аудио в бд
    audio_record = AudioRecord(user_id=user.id, uuid=str(audio_id), record_data=audio_data)
    db.add(audio_record)
    db.commit()

    base_url = str(request.base_url)
    record_url = f"{base_url}record?id={audio_record.id}&user={audio_record.user_id}"
    return AudioRecordResponse(record_url=record_url)



@app.get("/record")
def download_audio_record(
    id: int = Query(..., description="Record ID"),
    user: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):

    audio_record = db.query(AudioRecord).filter(AudioRecord.id == id, AudioRecord.user_id == user).first()
    if not audio_record:
        raise HTTPException(status_code=404, detail="Audio record not found")

    file_path = f"recordings/{audio_record.uuid}.mp3"
    with open(file_path, "wb") as file:
        file.write(audio_record.record_data)

    return FileResponse(file_path, media_type="audio/mp3")