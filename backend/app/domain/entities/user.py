from datetime import datetime
from typing import Optional, List

class User:
    def __init__(
            self,
            id: Optional[str] = None,
            username: str = "",
            email: str = "",
            hashed_password: str = "",
            is_active: bool = True,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()