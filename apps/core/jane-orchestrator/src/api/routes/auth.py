"""
Authentication routes for Jane Orchestrator.

Integrates with the central authentication service for unified SSO
while maintaining backward compatibility with existing auth patterns.
"""

import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import httpx
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ..config.auth_config import AuthConfigManager, get_auth_config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str
    remember_me: bool = False


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user_info: Optional[Dict[str, Any]] = None


class UserInfo(BaseModel):
    """User information model."""
    user_id: str
    username: str
    email: str
    name: Optional[str] = None
    roles: list[str] = []
    permissions: list[str] = []


@router.get("/login")
async def login_page(
    request: Request,
    redirect_to: Optional[str] = None,
    auth_config: AuthConfigManager = Depends(get_auth_config)
):
    """
    Initiate OAuth2 login flow with central auth service.

    Redirects to the central authentication service for login.
    """
    try:
        oauth2_config = auth_config.get_oauth2_config()
        auth_service_url = auth_config.get_auth_service_url()

        # Build OAuth2 authorization URL
        params = {
            "response_type": "code",
            "client_id": oauth2_config["client_id"],
            "redirect_uri": oauth2_config["redirect_uris"][0],
            "scope": " ".join(oauth2_config["scopes"]),
            "state": redirect_to or "/",  # Include redirect URL in state
        }

        authorization_url = f"{auth_service_url}/oauth2/authorize?{urlencode(params)}"

        logger.info(
            "Redirecting to central auth service: %s",
            authorization_url
        )

        return RedirectResponse(url=authorization_url)

    except Exception as e:
        logger.error("Failed to initiate login: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate login"
        )


@router.get("/callback")
async def oauth_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    auth_config: AuthConfigManager = Depends(get_auth_config)
):
    """
    Handle OAuth2 callback from central auth service.

    Exchanges authorization code for access token and user information.
    """
    if error:
        logger.error("OAuth2 error: %s", error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {error}"
        )

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not provided"
        )

    try:
        oauth2_config = auth_config.get_oauth2_config()
        auth_service_url = auth_config.get_auth_service_url()

        # Exchange code for token
        token_data = await exchange_code_for_token(
            code=code,
            client_id=oauth2_config["client_id"],
            client_secret=oauth2_config["client_secret"],
            redirect_uri=oauth2_config["redirect_uris"][0],
            auth_service_url=auth_service_url
        )

        # Get user information
        user_info = await get_user_info_from_token(
            access_token=token_data["access_token"],
            auth_service_url=auth_service_url
        )

        # Store session/token information
        response = RedirectResponse(url=state or "/")

        # Set session cookie
        response.set_cookie(
            key="access_token",
            value=token_data["access_token"],
            max_age=token_data.get("expires_in", 3600),
            httponly=True,
            secure=not auth_config.is_development_mode(),
            samesite="lax"
        )

        if token_data.get("refresh_token"):
            response.set_cookie(
                key="refresh_token",
                value=token_data["refresh_token"],
                max_age=7 * 24 * 3600,  # 7 days
                httponly=True,
                secure=not auth_config.is_development_mode(),
                samesite="lax"
            )

        logger.info(
            "User authenticated successfully: %s",
            user_info.get("username", "unknown")
        )

        return response

    except Exception as e:
        logger.error("OAuth callback failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/login/direct")
async def direct_login(
    login_request: LoginRequest,
    auth_config: AuthConfigManager = Depends(get_auth_config)
) -> TokenResponse:
    """
    Direct login with username/password (development/API use).

    For API clients that cannot use OAuth2 redirect flow.
    """
    try:
        auth_service_url = auth_config.get_auth_service_url()

        # Authenticate with central auth service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{auth_service_url}/auth/login",
                json={
                    "username": login_request.username,
                    "password": login_request.password,
                    "remember_me": login_request.remember_me
                },
                timeout=10.0
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

            token_data = response.json()

        # Get user information
        user_info = await get_user_info_from_token(
            access_token=token_data["access_token"],
            auth_service_url=auth_service_url
        )

        return TokenResponse(
            access_token=token_data["access_token"],
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token"),
            user_info=user_info
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Direct login failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/refresh")
async def refresh_token(
    request: Request,
    auth_config: AuthConfigManager = Depends(get_auth_config)
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    """
    refresh_token_value = request.cookies.get("refresh_token")

    if not refresh_token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    try:
        auth_service_url = auth_config.get_auth_service_url()
        oauth2_config = auth_config.get_oauth2_config()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{auth_service_url}/oauth2/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token_value,
                    "client_id": oauth2_config["client_id"],
                    "client_secret": oauth2_config["client_secret"]
                },
                timeout=10.0
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )

            token_data = response.json()

        return TokenResponse(
            access_token=token_data["access_token"],
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(
    request: Request,
    auth_config: AuthConfigManager = Depends(get_auth_config)
):
    """
    Logout user and invalidate tokens.
    """
    access_token = request.cookies.get("access_token")

    try:
        if access_token:
            auth_service_url = auth_config.get_auth_service_url()

            # Notify central auth service of logout
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{auth_service_url}/auth/logout",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=5.0
                )

        # Clear cookies
        response = Response(
            status_code=200, content='"Logged out successfully"')
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

    except Exception as e:
        logger.error("Logout failed: %s", str(e))
        # Still clear cookies even if central logout fails
        response = Response(status_code=200, content='"Logged out"')
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


@router.get("/me")
async def get_current_user(
    request: Request,
    auth_config: AuthConfigManager = Depends(get_auth_config)
) -> UserInfo:
    """
    Get current user information.
    """
    # This will be handled by the auth middleware
    # The user should be available in request.state.user
    if not hasattr(request.state, 'user') or not request.state.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    user_data = request.state.user

    return UserInfo(
        user_id=user_data.get("user_id", ""),
        username=user_data.get("username", ""),
        email=user_data.get("email", ""),
        name=user_data.get("name"),
        roles=user_data.get("roles", []),
        permissions=user_data.get("scopes", [])
    )


# Helper functions

async def exchange_code_for_token(
    code: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    auth_service_url: str
) -> Dict[str, Any]:
    """Exchange authorization code for access token."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{auth_service_url}/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri
            },
            timeout=10.0
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange code for token"
            )

        return response.json()


async def get_user_info_from_token(
    access_token: str,
    auth_service_url: str
) -> Dict[str, Any]:
    """Get user information using access token."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{auth_service_url}/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to get user information"
            )

        return response.json()
