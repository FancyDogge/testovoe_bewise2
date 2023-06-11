from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    access_token = Column(String, unique=True) #index?
    record_files = relationship("AudioRecord", back_populates="user")


class AudioRecord(Base):
    __tablename__ = "audio_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    uuid = Column(String, unique=True, index=True)
    record_data = Column(LargeBinary)
    user = relationship("User", back_populates="record_files")