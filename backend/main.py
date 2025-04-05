# main.py
import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.api import auth_routes, video_routes
from app.domain.entities.user import User
from app.domain.entities.video import Video
from app.infrastructure.persistence.user_repository_impl import InMemoryUserRepository
from app.infrastructure.persistence.video_repository_impl import InMemoryVideoRepository
from app.application.services.auth_service import AuthService

# Crear aplicación FastAPI
app = FastAPI(title="Video Streaming API")

# Configurar CORS para permitir peticiones desde el frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # URL del frontend en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(video_routes.router, prefix="/api/videos", tags=["Videos"])

# Crear directorios necesarios
os.makedirs("videos", exist_ok=True)

# Inicializar datos de ejemplo
@app.on_event("startup")
async def startup_event():
    # Crear algunos videos de ejemplo si no existen
    videos_dir = "videos"
    if len(os.listdir(videos_dir)) == 0:
        print("Inicializando videos de ejemplo...")
        # En un entorno real, descargarías o copiarías videos reales
        # Aquí solo creamos archivos vacíos para simular
        for i in range(1, 4):
            file_path = os.path.join(videos_dir, f"video{i}.mp4")
            with open(file_path, "wb") as f:
                f.write(b"Placeholder para el video")  # Solo un marcador de posición

    # Crear usuario de prueba
    user_repo = InMemoryUserRepository()
    auth_service = AuthService(user_repo)

    try:
        test_user = User(
            id=str(uuid.uuid4()),
            username="test",
            email="test@example.com",
            hashed_password=auth_service.get_password_hash("password123")
        )
        await user_repo.create(test_user)
        print(f"Usuario de prueba creado: {test_user.username}")
    except Exception as e:
        print(f"Error al crear usuario de prueba: {e}")

@app.get("/")
async def root():
    return {"message": "Video Streaming API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

