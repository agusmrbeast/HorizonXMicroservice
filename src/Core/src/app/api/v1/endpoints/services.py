"""Service registry endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api import get_current_superuser, get_current_user
from src.app.models import User
from src.app.schemas import Service, ServiceCreate, ServiceUpdate
from src.app.services import ServiceRegistryService
from src.core.db import get_db
from src.core.cache import cached

router = APIRouter()


@router.get("/", response_model=List[Service])
@cached(expire=300)  # Cache for 5 minutes
async def list_services(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Service]:
    """
    List all registered services.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current user

    Returns:
        List of services
    """
    service_registry = ServiceRegistryService(db)
    return await service_registry.get_multi(skip=skip, limit=limit)


@router.get("/{service_name}", response_model=Service)
@cached(expire=300)  # Cache for 5 minutes
async def get_service(
    service_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Service:
    """
    Get service by name.

    Args:
        service_name: Service name
        db: Database session
        current_user: Current user

    Returns:
        Service details

    Raises:
        HTTPException: If service not found
    """
    service_registry = ServiceRegistryService(db)
    service = await service_registry.get_by_name(service_name)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {service_name} not found",
        )
    return service


@router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Service:
    """
    Create new service (admin only).

    Args:
        service_in: Service data
        db: Database session
        current_user: Current superuser

    Returns:
        Created service

    Raises:
        HTTPException: If service with same name already exists
    """
    service_registry = ServiceRegistryService(db)
    existing_service = await service_registry.get_by_name(service_in.name)
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with name {service_in.name} already exists",
        )
    return await service_registry.create_service(service_in)


@router.put("/{service_name}", response_model=Service)
async def update_service(
    service_name: str,
    service_in: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Service:
    """
    Update service (admin only).

    Args:
        service_name: Service name
        service_in: Service data
        db: Database session
        current_user: Current superuser

    Returns:
        Updated service

    Raises:
        HTTPException: If service not found
    """
    service_registry = ServiceRegistryService(db)
    service = await service_registry.get_by_name(service_name)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {service_name} not found",
        )
    return await service_registry.update_service(service, service_in)


@router.delete("/{service_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> None:
    """
    Delete service (admin only).

    Args:
        service_name: Service name
        db: Database session
        current_user: Current superuser

    Raises:
        HTTPException: If service not found
    """
    service_registry = ServiceRegistryService(db)
    service = await service_registry.get_by_name(service_name)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service {service_name} not found",
        )
    await service_registry.delete_service(service)
