# Path: fta_profile/app/infrastructure/lifespan.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
import google.cloud.firestore as firestore

firestores = {}

@asynccontextmanager
async def lifespan(app: FastAPI):

    # await app.state.log.info("Starting the application")
    firestores["database"] = firestore.AsyncClient(
        database=app.state.settings.firestore_database, project=app.state.settings.firestore_project_id
    )
    firestores["collection"] = firestores["database"].collection(app.state.settings.firestore_collection)
    try:
        yield {}
    finally:
        firestores["database"].close()
        # await app.state.log.info("Shutting down the application")
        # await app.state.log.shutdown()
