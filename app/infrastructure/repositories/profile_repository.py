# Path: fta_profile/app/infrastructure/repositories/profile_repository.py

from fastapi import HTTPException, status, Depends
from graphql import GraphQLError
from google.cloud.firestore_v1.base_query import FieldFilter
from ...domain.interfaces.profile_interface import ProfileInterface
from ...domain.models.profile import Profile, ProfileCreate, ProfileUpdate
from google.cloud.firestore import AsyncCollectionReference


class ProfileRepository(ProfileInterface):
    # Profile Repository constructor
    def __init__(self, collection: AsyncCollectionReference = Depends(), transport: str = "http"):
        ## Firestore collection
        self.collection = collection
        ## Transport
        self.transport = transport

    # firestore
    ## Check the existence of data
    async def isExist(self, id: str) -> bool:
        try:
            ### Get datum from firestore
            datum = await self.collection.document(id).get()
            ### Check if datum exists in firestore
            if datum.exists:
                return True
            else:
                return False
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "msg": "Cannot check if profile datum exists",
                    "reason": str(e),
                },
            )

    ### check datum integrity
    async def isConflict(self, datum: ProfileCreate) -> bool:
        try:
            ### Check if datum email already exists in firestore
            query = self.collection.where(
                filter=FieldFilter(
                    field_path="email", op_string="==", value=datum.email
                )
            )
            existing_docs = [d async for d in query.stream()]
            if existing_docs:
                return True
            else:
                return False
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "msg": "Cannot check profile datum integrity",
                    "reason": str(e),
                },
            )

    ## List data with pagination
    async def list(
        self, order_by: str = "uuid", offset: int = 1, limit: int = 10
    ) -> list[Profile]:
        ## List Data
        try:
            ## ref: https://cloud.google.com/firestore/docs/samples/firestore-query-cursor-pagination-async
            first_query = self.collection.order_by(order_by).limit(offset)
            # Get the last document from the results
            docs = [d async for d in first_query.stream()]
            if not docs:
                return []
            last_doc = list(docs)[-1]
            # Construct a new query starting at this document
            last_pop = last_doc.to_dict()[order_by]
            next_query = (
                self.collection.order_by(order_by)
                .start_at({order_by: last_pop})
                .limit(limit)
            )
            new_docs = [d async for d in next_query.stream()]
            data = [Profile(**d.to_dict()) for d in new_docs]
            return data
        except Exception as e:
            if self.transport == "http":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail={"msg": "Cannot list profile data", "reason": str(e)},
                )
            elif self.transport == "graphql":
                raise GraphQLError(
                    message="Cannot list profile data", extensions={"reason": str(e)}
                )

    ## Get datum by id
    async def get(self, id: str) -> Profile:
        try:
            # Retrieve a document reference asynchronously
            datum = await self.collection.document(id).get()
            if not datum.exists:
                return None
            return Profile(**datum.to_dict())
        except Exception as e:
            ### Raise exception
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"msg": "Cannot get profile datum", "reason": str(e)},
            )

    ## Create datum
    async def create(self, datum: ProfileCreate) -> ProfileCreate:
        try:
            ## create datum in firestore
            await self.collection.document(datum.uuid).set(datum.model_dump())
            return datum
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "msg": "Cannot create profile datum in profile_repository",
                    "reason": str(e),
                },
            )

    ## Update a datum
    async def update(self, id: str, datum: ProfileUpdate) -> ProfileUpdate:
        try:
            # Update the rest of the fields
            await self.collection.document(id).update(
                datum.model_dump(exclude_unset=True)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"msg": "Cannot update profile datum", "reason": str(e)},
            )

    ## Delete a datum
    async def delete(self, id: str):
        try:
            ### delete datum from firestore
            await self.collection.document(id).delete()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"msg": "Cannot delete profile datum", "reason": str(e)},
            )
