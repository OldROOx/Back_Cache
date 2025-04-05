import uuid
import os
from typing import Dict, List, Optional
from app.domain.entities.video import Video
from app.domain.repositories.video_repository import VideoRepository

class InMemoryVideoRepository(VideoRepository):
    def __init__(self):
        self.videos: Dict[str, Video] = {}

        # Inicializar con algunos videos predeterminados
        videos_dir = "videos"
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                if filename.endswith((".mp4", ".webm", ".mov")):
                    video_id = str(uuid.uuid4())
                    title = os.path.splitext(filename)[0].replace("_", " ").title()
                    self.videos[video_id] = Video(
                        id=video_id,
                        title=title,
                        description=f"Descripción de {title}",
                        file_path=os.path.join(videos_dir, filename)
                    )

    async def create(self, video: Video) -> Video:
        # Generar ID si no existe
        if not video.id:
            video.id = str(uuid.uuid4())

        self.videos[video.id] = video
        return video

    async def get_by_id(self, video_id: str) -> Optional[Video]:
        return self.videos.get(video_id)

    async def get_all(self) -> List[Video]:
        return list(self.videos.values())

    async def update(self, video: Video) -> Video:
        if video.id not in self.videos:
            raise ValueError(f"Video with ID {video.id} not found")

        self.videos[video.id] = video
        return video

    async def delete(self, video_id: str) -> bool:
        if video_id not in self.videos:
            return False

        del self.videos[video_id]
        return True