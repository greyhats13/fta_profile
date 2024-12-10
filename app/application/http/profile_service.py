from uuid import uuid4
from datetime import datetime
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from ...domain.models.profile import ProfileCreate, ProfileUpdate
from ...infrastructure.repositories.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository = Depends()):
        self.profile_repo = profile_repo

    async def list(self, order_by: str = "uuid", offset: int = 1, limit: int = 10) -> APIRouter:
        
        profiles = await self.profile_repo.list(
            order_by=order_by, offset=offset, limit=limit
        )
        # Check if offset is less than 1
        if offset < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Offset must be greater than 0",
            )
        # Check if no profiles data
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile data not found"
            )
        return profiles

    # Get a profile data for http
    async def get(self, uuid: str) -> APIRouter:
        profile = await self.profile_repo.get(uuid)
        ## check if profile exists
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        return profile

    # Create a profile data
    async def post(self, profile: ProfileCreate) -> APIRouter:
        ## check data integrity
        if await self.profile_repo.isConflict(profile):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Profile email already exist",
            )
        profile.uuid = str(uuid4())
        if profile.birthdate:
            profile.birthdate = profile.birthdate.isoformat()
        profile.updatedAt = datetime.now().isoformat()
        profile.createdAt = datetime.now().isoformat()
        profile = await self.profile_repo.create(profile)
        return profile

    # Update a profile data
    async def put(self, uuid: str, profile: ProfileUpdate) -> APIRouter:
        ## check if profile exists
        if not await self.profile_repo.isExist(uuid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        ## convert birthdate to isoformat
        if profile.birthdate:
            profile.birthdate = profile.birthdate.isoformat()
        profile.updatedAt = datetime.now().isoformat()
        ## update profile
        await self.profile_repo.update(uuid, profile)
        profile = await self.profile_repo.get(uuid)
        return profile

    # Delete a profile data
    async def delete(self, uuid: str):
        ## check if profile exists
        if not await self.profile_repo.isExist(uuid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
            )
        await self.profile_repo.delete(uuid)

    # health check
    async def health(self):
        # return 200
        return JSONResponse(content={"status": "ok"})
