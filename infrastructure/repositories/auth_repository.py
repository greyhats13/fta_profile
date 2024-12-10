from app.domain.interface.auth_interface import AuthInterface
from app.domain.model.auth import UserInDB
from passlib.context import CryptContext
from google.cloud import firestore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthRepository(AuthInterface):
    def __init__(self, collection: firestore.AsyncCollectionReference):
        self.collection = collection

    async def get_user(self, username: str) -> UserInDB | None:
        doc_ref = self.collection.document(username)
        doc = await doc_ref.get()
        if doc.exists:
            return UserInDB(**doc.to_dict())
        return None

    async def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        user = await self.get_user(username)
        if user and pwd_context.verify(password, user.hashed_password):
            return user
        return None

    async def create_access_token(self, data: dict) -> str:
        from jose import jwt
        from datetime import datetime, timedelta
        from app.config import Settings

        settings = Settings()
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
