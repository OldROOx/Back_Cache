from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoCreateDTO(BaseModel):
    title: str
    description: str
    file_path: str
    thumbnail_path: Optional[str] = None
    duration: Optional[int] = None


class VideoUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_path: Optional[str] = None
    duration: Optional[int] = None


class VideoResponseDTO(BaseModel):
    id: str
    title: str
    description: str
    file_path: str
    thumbnail_path: Optional[str] = None
    duration: Optional[int] = None
    created_at: datetime
    updated_at: datetime