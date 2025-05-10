from src.app.api.v1.endpoints.auth import router as auth_router
from src.app.api.v1.endpoints.posts import router as posts_router
from src.app.api.v1.endpoints.rbac import router as rbac_router
from src.app.api.v1.endpoints.users import router as users_router
from src.app.api.v1.endpoints.services import router as services_router
from src.app.api.v1.endpoints.debug import router as debug_router

__all__ = [
    "auth_router",
    "posts_router",
    "rbac_router",
    "users_router",
    "services_router",
    "debug_router",
]
