"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api import get_current_user
from src.app.models import User
from src.app.schemas import Login, RefreshToken, Token
from src.app.services import AuthService
from src.core.utils import create_rate_limiter
from src.core.db import get_db

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    login_data: Login,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(create_rate_limiter(5, 60)),  # 5 requests per minute
) -> Token:
    """
    Login user.

    Args:
        login_data: Login credentials
        db: Database session

    Returns:
        Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    auth_service = AuthService(db)

    # Authenticate user
    user = await auth_service.authenticate(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens using username
    tokens = auth_service.create_tokens(user.username)
    return Token(**tokens)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: RefreshToken,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(create_rate_limiter(5, 60)),  # 5 requests per minute
) -> Token:
    """Refresh tokens."""
    auth_service = AuthService(db)
    tokens = await auth_service.refresh_tokens(refresh_token.refresh_token)
    return Token(**tokens)


@router.post("/validate-token", response_model=dict)
async def validate_token(
    current_user: User = Depends(get_current_user),
):
    """
    Validate JWT token and return user data.

    This endpoint is used by other microservices to validate tokens.

    Args:
        current_user: Current user

    Returns:
        User data if token is valid
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "roles": [{"id": role.id, "name": role.name} for role in current_user.roles],
    }


@router.post("/validate-permission", response_model=dict)
async def validate_permission(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Validate if a user has a specific permission.

    This endpoint is used by other microservices to validate permissions.

    Args:
        data: Dict containing resource and action
        current_user: Current user
        db: Database session

    Returns:
        User data if authorized

    Raises:
        HTTPException: If user does not have permission
    """
    resource = data.get("resource")
    action = data.get("action")

    if not resource or not action:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource and action are required",
        )

    # Superuser has all permissions
    if current_user.is_superuser:
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }

    # Check if user has permission
    for role in current_user.roles:
        for permission in role.permissions:
            if permission.resource == resource and permission.action == action:
                return {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                }

    # User does not have permission
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    )
