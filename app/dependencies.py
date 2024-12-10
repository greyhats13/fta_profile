# Path: fta_profile/app/dependencies.py

from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from google.cloud.firestore import AsyncCollectionReference
from .application.http.profile_service import ProfileService
from .infrastructure.repositories.profile_repository import ProfileRepository
from .infrastructure.lifespan import firestores
from .config import Settings

@lru_cache()
def get_settings():
    return Settings()

async def get_firestore_collection() -> AsyncCollectionReference:
    return firestores["collection"]

async def get_profile_repository(collection = Depends(get_firestore_collection)):
    return ProfileRepository(collection=collection)

async def get_profile_service(profile_repo: Annotated[ProfileRepository, Depends(get_profile_repository)]):
    return ProfileService(profile_repo=profile_repo)
