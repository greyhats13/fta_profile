from abc import ABC, abstractmethod
from ..model.auth import UserInDB

class AuthInterface(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> UserInDB | None:
        pass

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        pass

    @abstractmethod
    async def create_access_token(self, data: dict) -> str:
        pass
