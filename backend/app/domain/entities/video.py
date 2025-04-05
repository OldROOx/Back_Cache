from datetime import datetime
from typing import Optional

class Video:
    def __init__(
            self,
            id: Optional[str] = None,
            title: str = "",
            description: str = "",
            file_path: str = "",
            thumbnail_path: Optional[str] = None,
            duration: Optional[int] = None,  # en segundos
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.file_path = file_path
        self.thumbnail_path = thumbnail_path
        self.duration = duration
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()