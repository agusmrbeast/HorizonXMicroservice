"""API v1 router."""

from fastapi import APIRouter

from src.app.api.v1.endpoints import posts_router, debug_router

# Create API router
router = APIRouter()

# Include endpoint routers
router.include_router(posts_router, prefix="/posts", tags=["posts"])
router.include_router(debug_router, prefix="/debug", tags=["debug"])
