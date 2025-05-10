"""API v1 router."""

from fastapi import APIRouter

from src.app.api.v1.endpoints import (
    auth_router,
    posts_router,
    rbac_router,
    users_router,
    services_router,
    debug_router,
)

# Create API router
router = APIRouter()

# Include endpoint routers
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(rbac_router, prefix="/rbac", tags=["rbac"])
router.include_router(posts_router, prefix="/posts", tags=["posts"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(debug_router, prefix="/debug", tags=["debug"])
