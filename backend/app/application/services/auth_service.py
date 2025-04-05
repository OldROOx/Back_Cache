from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.application.dto.user_dto import UserCreateDTO, UserResponseDTO, TokenDTO

# Constantes de configuración para JWT
SECRET_KEY = "your-secret-key"  # En producción, usar una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def register_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        # Verificar si el usuario ya existe
        existing_user = await self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise ValueError("Username already registered")

        existing_email = await self.user_repository.get_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already registered")

        # Crear el nuevo usuario
        hashed_password = self.get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        created_user = await self.user_repository.create(new_user)

        return UserResponseDTO(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, username: str, password: str) -> Optional[TokenDTO]:
        user = await self.authenticate_user(username, password)
        if not user:
            return None

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        return TokenDTO(
            access_token=access_token,
            token_type="bearer"
        )