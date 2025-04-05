import os
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from typing import List
from app.domain.entities.user import User
from app.application.dto.video_dto import VideoCreateDTO, VideoUpdateDTO, VideoResponseDTO
from app.application.services.video_service import VideoService
from app.infrastructure.api.auth_routes import get_current_user

router = APIRouter()

def get_video_service():
    # Debe ser reemplazado por una inyección de dependencias adecuada
    from app.infrastructure.persistence.video_repository_impl import InMemoryVideoRepository
    video_repository = InMemoryVideoRepository()
    return VideoService(video_repository)

@router.get("/", response_model=List[VideoResponseDTO])
async def get_videos(current_user: User = Depends(get_current_user)):
    video_service = get_video_service()
    return await video_service.get_all_videos()

@router.get("/{video_id}", response_model=VideoResponseDTO)
async def get_video(video_id: str, current_user: User = Depends(get_current_user)):
    video_service = get_video_service()
    video = await video_service.get_video(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    return video

@router.post("/", response_model=VideoResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_video(
        title: str,
        description: str,
        video_file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
):
    # Verificar que el archivo es un video
    content_type = video_file.content_type
    if not content_type.startswith("video/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File provided is not a video"
        )

    # Guardar el archivo
    videos_dir = "videos"
    os.makedirs(videos_dir, exist_ok=True)

    file_extension = os.path.splitext(video_file.filename)[1]
    file_path = os.path.join(videos_dir, f"{title.replace(' ', '_')}{file_extension}")

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await video_file.read()
        await out_file.write(content)

    # Crear el video en el repositorio
    video_service = get_video_service()
    video_data = VideoCreateDTO(
        title=title,
        description=description,
        file_path=file_path
    )

    return await video_service.create_video(video_data)

@router.put("/{video_id}", response_model=VideoResponseDTO)
async def update_video(
        video_id: str,
        video_data: VideoUpdateDTO,
        current_user: User = Depends(get_current_user)
):
    video_service = get_video_service()
    updated_video = await video_service.update_video(video_id, video_data)
    if not updated_video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    return updated_video

@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: str, current_user: User = Depends(get_current_user)):
    video_service = get_video_service()
    success = await video_service.delete_video(video_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

# Función para entregar el video por partes (streaming)
async def video_streamer(video_path):
    async with aiofiles.open(video_path, mode="rb") as f:
        while chunk := await f.read(1024 * 1024):  # 1MB por chunk
            yield chunk

@router.get("/stream/{video_id}")
async def stream_video(video_id: str, request: Request, current_user: User = Depends(get_current_user)):
    video_service = get_video_service()
    video = await video_service.get_video(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )

    # Verificar que el archivo existe
    if not os.path.exists(video.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video file not found"
        )

    # Determinar el tipo MIME
    file_ext = os.path.splitext(video.file_path)[1].lower()
    media_type = "video/mp4"  # Por defecto
    if file_ext == ".webm":
        media_type = "video/webm"
    elif file_ext == ".mov":
        media_type = "video/quicktime"

    return StreamingResponse(
        video_streamer(video.file_path),
        media_type=media_type
    )