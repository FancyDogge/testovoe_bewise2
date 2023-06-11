from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    user_id: int
    access_token: str

class AudioRecordResponse(BaseModel):
    record_url: str