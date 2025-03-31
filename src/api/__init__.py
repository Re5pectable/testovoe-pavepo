from .routers.admin import router as admin_router
from .routers.root import router as root_router
from .routers.user import router as user_router
from .routers.media import router as media_router

__all__ = ["root_router", "user_router", "admin_router", "media_router"]
