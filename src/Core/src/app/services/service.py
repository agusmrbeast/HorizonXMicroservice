"""Service registry service."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.service import Service
from src.app.schemas.service import ServiceCreate, ServiceUpdate
from src.app.services.base import BaseService


class ServiceRegistryService(BaseService[Service]):
    """Service for managing service registry."""

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        super().__init__(db, Service)

    async def get_by_name(self, name: str) -> Optional[Service]:
        """Get service by name."""
        query = select(Service).where(Service.name == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_active_services(self) -> List[Service]:
        """Get all active services."""
        query = select(Service).where(Service.is_active.is_(True))
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_service(self, service_in: ServiceCreate) -> Service:
        """Create new service."""
        service = Service(**service_in.model_dump())
        self.db.add(service)
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def update_service(
        self, service: Service, service_in: ServiceUpdate
    ) -> Service:
        """Update service."""
        update_data = service_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)

        self.db.add(service)
        await self.db.commit()
        await self.db.refresh(service)
        return service

    async def delete_service(self, service: Service) -> None:
        """Delete service."""
        await self.db.delete(service)
        await self.db.commit()
