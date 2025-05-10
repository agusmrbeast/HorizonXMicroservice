"""Schemas package."""

from typing import Any, Dict
from src.app.schemas.post import Post, PostCreate, PostInDB, PostUpdate

# Type alias for user data returned from Core service
UserDict = Dict[str, Any]

__all__ = [
    "Post",
    "PostCreate",
    "PostUpdate",
    "PostInDB",
    "UserDict",
]
