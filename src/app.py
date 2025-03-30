import uvicorn
from fastapi import FastAPI

from .config import DEBUG

docs = dict(docs_url=None, redoc_url=None, openapi_url=None) if not DEBUG else {}
app = FastAPI(**docs)

def start_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=DEBUG)
