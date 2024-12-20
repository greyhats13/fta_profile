# Path: fta_profile/app/domain/models/profile.py
from enum import Enum
from datetime import date, datetime
from pydantic import BaseModel, EmailStr

# http
# Enums
class Gender(str, Enum):
    male = 'male'
    female = 'female'

## Image
class Image(BaseModel):
    name: str | None = None
    url: str | None = None

class Address(BaseModel):
    type: str | None = None
    address: str | None = None
    subdistrict: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    country: str | None = None
    postalCode: int | None = None

## Profile
class Profile(BaseModel):
    uuid: str | None = None
    email: EmailStr | None
    firstname: str | None = None
    lastname: str | None = None
    birthdate: date | None = None
    gender: Gender | None = None
    addresses: list[Address] | None = None
    image: Image | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

## ProfileCreate
class ProfileCreate(BaseModel):
    uuid: str | None = None
    email: EmailStr
    firstname: str | None = None
    lastname: str | None = None
    birthdate: date | None = None
    gender: Gender | None = None
    addresses: list[Address] | None = None
    image: Image | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

## ProfileUpdate
class ProfileUpdate(BaseModel):
    uuid: str  | None = None
    email: EmailStr | None = None
    firstname: str | None = None
    lastname: str | None = None
    birthdate: date | None = None
    gender: Gender | None = None
    addresses: list[Address] | None = None
    image: Image | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None