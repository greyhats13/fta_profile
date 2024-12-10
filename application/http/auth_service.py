from fastapi import Depends, HTTPException, status
from app.domain.interface.auth_interface import AuthInterface
from app.domain.model.auth import Token, TokenData, User
from app.dependencies import get_auth_repository
from jose import JWTError, jwt
from app.config import Settings

class AuthService:
    def __init__(self, auth_repo: AuthInterface = Depends(get_auth_repository)):
        self.auth_repo = auth_repo
        self.settings = Settings()

    async def login(self, username: str, password: str) -> Token:
        user = await self.auth_repo.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token = await self.auth_repo.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )
        try:
            payload = jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.auth_repo.get_user(token_data.username)
        if user is None:
            raise credentials_exception
        return user
