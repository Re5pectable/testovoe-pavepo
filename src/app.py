import uvicorn
from fastapi import FastAPI

from .config import DEBUG
from .api import root_router, user_router, LoggingMiddleware

docs = dict(docs_url=None, redoc_url=None, openapi_url=None) if not DEBUG else {}
app = FastAPI(**docs)

app.add_middleware(LoggingMiddleware)
app.include_router(root_router, prefix="", tags=["Root"])
app.include_router(user_router, prefix="/user", tags=["User"])

def start_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=DEBUG)
