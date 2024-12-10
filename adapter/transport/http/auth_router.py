from fastapi import APIRouter, Depends, Form
from app.application.http.auth_service import AuthService
from app.domain.model.auth import Token

auth_router = APIRouter()

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends()
):
    return await auth_service.login(username, password)
