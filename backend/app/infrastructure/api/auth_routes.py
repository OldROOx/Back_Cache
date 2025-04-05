from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from app.application.dto.user_dto import UserCreateDTO, UserResponseDTO, TokenDTO
from app.application.services.auth_service import AuthService, SECRET_KEY, ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_auth_service():
    # Debe ser reemplazado por una inyección de dependencias adecuada
    from app.infrastructure.persistence.user_repository_impl import InMemoryUserRepository
    user_repository = InMemoryUserRepository()
    return AuthService(user_repository)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    auth_service = get_auth_service()
    user = await auth_service.user_repository.get_by_username(username)
    if user is None:
        raise credentials_exception

    return user

@router.post("/register", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateDTO):
    auth_service = get_auth_service()
    try:
        return await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=TokenDTO)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_service = get_auth_service()
    token = await auth_service.login(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token