from typing import List, Optional
from app.domain.repositories.video_repository import VideoRepository
from app.domain.entities.video import Video
from app.application.dto.video_dto import VideoCreateDTO, VideoUpdateDTO, VideoResponseDTO

class VideoService:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    async def create_video(self, video_data: VideoCreateDTO) -> VideoResponseDTO:
        new_video = Video(
            title=video_data.title,
            description=video_data.description,
            file_path=video_data.file_path,
            thumbnail_path=video_data.thumbnail_path,
            duration=video_data.duration
        )

        created_video = await self.video_repository.create(new_video)

        return VideoResponseDTO(
            id=created_video.id,
            title=created_video.title,
            description=created_video.description,
            file_path=created_video.file_path,
            thumbnail_path=created_video.thumbnail_path,
            duration=created_video.duration,
            created_at=created_video.created_at,
            updated_at=created_video.updated_at
        )

    async def get_video(self, video_id: str) -> Optional[VideoResponseDTO]:
        video = await self.video_repository.get_by_id(video_id)
        if not video:
            return None

        return VideoResponseDTO(
            id=video.id,
            title=video.title,
            description=video.description,
            file_path=video.file_path,
            thumbnail_path=video.thumbnail_path,
            duration=video.duration,
            created_at=video.created_at,
            updated_at=video.updated_at
        )

    async def get_all_videos(self) -> List[VideoResponseDTO]:
        videos = await self.video_repository.get_all()

        return [
            VideoResponseDTO(
                id=video.id,
                title=video.title,
                description=video.description,
                file_path=video.file_path,
                thumbnail_path=video.thumbnail_path,
                duration=video.duration,
                created_at=video.created_at,
                updated_at=video.updated_at
            )
            for video in videos
        ]

    async def update_video(self, video_id: str, video_data: VideoUpdateDTO) -> Optional[VideoResponseDTO]:
        video = await self.video_repository.get_by_id(video_id)
        if not video:
            return None

        # Actualizar solo los campos proporcionados
        if video_data.title is not None:
            video.title = video_data.title
        if video_data.description is not None:
            video.description = video_data.description
        if video_data.thumbnail_path is not None:
            video.thumbnail_path = video_data.thumbnail_path
        if video_data.duration is not None:
            video.duration = video_data.duration

        updated_video = await self.video_repository.update(video)

        return VideoResponseDTO(
            id=updated_video.id,
            title=updated_video.title,
            description=updated_video.description,
            file_path=updated_video.file_path,
            thumbnail_path=updated_video.thumbnail_path,
            duration=updated_video.duration,
            created_at=updated_video.created_at,
            updated_at=updated_video.updated_at
        )

    async def delete_video(self, video_id: str) -> bool:
        return await self.video_repository.delete(video_id)