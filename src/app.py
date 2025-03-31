import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import admin_router, root_router, user_router, media_router
from .config import DEBUG, ORIGINS

docs = dict(docs_url=None, redoc_url=None, openapi_url=None) if not DEBUG else {}
app = FastAPI(**docs)

app.include_router(root_router, prefix="", tags=["Root"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(media_router, prefix="/media", tags=["Media"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=DEBUG)
