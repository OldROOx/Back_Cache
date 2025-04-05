import uuid
from typing import Dict, List, Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}

    async def create(self, user: User) -> User:
        # Generar ID si no existe
        if not user.id:
            user.id = str(uuid.uuid4())

        self.users[user.id] = user
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    async def get_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def update(self, user: User) -> User:
        if user.id not in self.users:
            raise ValueError(f"User with ID {user.id} not found")

        self.users[user.id] = user
        return user

    async def delete(self, user_id: str) -> bool:
        if user_id not in self.users:
            return False

        del self.users[user_id]
        return True
