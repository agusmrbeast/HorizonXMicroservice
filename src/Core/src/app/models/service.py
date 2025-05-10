"""Service registry model."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from src.core.db import Base


class Service(Base):
    """Service registry model for microservice discovery."""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Service {self.name}>"
