"""API dependencies."""

import httpx
from typing import Callable, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.config import settings

# HTTP Bearer scheme
security = HTTPBearer()

# Core service URL
CORE_SERVICE_URL = settings.CORE_SERVICE_URL
API_V1_STR = settings.API_V1_STR


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Get current user from token by validating with Core service.

    Args:
        credentials: Bearer token credentials

    Returns:
        Current user data

    Raises:
        HTTPException: If token is invalid or Core service unavailable
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{CORE_SERVICE_URL}{API_V1_STR}/auth/validate-token",
                headers={"Authorization": f"Bearer {credentials.credentials}"},
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json().get("detail", "Invalid token"),
                )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Core service unavailable",
            )


def has_permission(resource: str, action: str) -> Callable:
    """
    Check if user has permission to access a resource.

    Args:
        resource: Resource name
        action: Action name

    Returns:
        Dependency function
    """

    async def check_permission(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> Dict[str, Any]:
        """
        Check if user has permission by validating with Core service.

        Args:
            credentials: Bearer token credentials

        Returns:
            User data if authorized

        Raises:
            HTTPException: If user does not have permission or Core service unavailable
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{CORE_SERVICE_URL}{API_V1_STR}/auth/validate-permission",
                    json={"resource": resource, "action": action},
                    headers={"Authorization": f"Bearer {credentials.credentials}"},
                )

                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.json().get("detail", "Permission denied"),
                    )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Core service unavailable",
                )

    return check_permission
