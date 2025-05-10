"""Service schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    """Base service schema."""

    name: str = Field(..., description="Service name", example="academics")
    url: str = Field(..., description="Service URL", example="http://localhost:8020")
    description: Optional[str] = Field(None, description="Service description")
    is_active: bool = Field(default=True, description="Is service active")


class ServiceCreate(ServiceBase):
    """Service creation schema."""

    pass


class ServiceUpdate(BaseModel):
    """Service update schema."""

    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ServiceInDB(ServiceBase):
    """Service in DB schema."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config."""

        from_attributes = True


class Service(ServiceInDB):
    """Service schema."""

    pass
