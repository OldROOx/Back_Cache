from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.video import Video

class VideoRepository(ABC):
    @abstractmethod
    async def create(self, video: Video) -> Video:
        pass

    @abstractmethod
    async def get_by_id(self, video_id: str) -> Optional[Video]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Video]:
        pass

    @abstractmethod
    async def update(self, video: Video) -> Video:
        pass

    @abstractmethod
    async def delete(self, video_id: str) -> bool:
        pass