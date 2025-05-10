from src.app.api.v1.endpoints.posts import router as posts_router
from src.app.api.v1.endpoints.debug import router as debug_router

__all__ = ["posts_router", "debug_router"]
