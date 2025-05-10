"""Post model."""

from sqlalchemy import Boolean, Column, Integer, String

# from sqlalchemy.orm import Mapped, relationship
from src.core.db import Base
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     # Import from Core module
#     from src.app.models import User


class Post(Base):
    """Post model."""

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    author_id = Column(Integer, nullable=False)

    # Relationships
    # author: Mapped["User"] = relationship("User", back_populates="posts")  # type: ignore
