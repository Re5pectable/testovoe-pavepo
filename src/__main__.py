import logging

from .app import start_app
from .config import DEBUG

if __name__ == "__main__":
    logging.warning(f"Running in {'debug' if DEBUG else 'production'} mode...")
    start_app()
