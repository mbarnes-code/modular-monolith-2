"""
OAuth2 API Endpoints - T140
FastAPI routes for OAuth2 authentication flow
"""

import secrets
from typing import List, Optional
from urllib.parse import parse_qsl, urlencode

from fastapi import (APIRouter, Depends, Form, HTTPException, Query, Request,
                     status)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from .provider import (OAuth2Token, OAuth2User, get_current_user,
                       get_oauth_config, get_oauth_provider, require_scopes)


class AuthorizeRequest(BaseModel):
    """OAuth2 authorization request parameters"""

    response_type: str = "code"
    client_id: str
    redirect_uri: str
    scope: str = ""
    state: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = "S256"


class TokenRequest(BaseModel):
    """OAuth2 token request parameters"""

    grant_type: str
    code: Optional[str] = None
    refresh_token: Optional[str] = None
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None


# OAuth2 API router
oauth_router = APIRouter(prefix="/oauth", tags=["oauth2"])


@oauth_router.get("/authorize")
async def authorize_endpoint(
    request: Request,
    response_type: str = Query(..., description="Must be 'code'"),
    client_id: str = Query(..., description="OAuth2 client ID"),
    redirect_uri: str = Query(..., description="Redirect URI"),
    scope: str = Query("", description="Requested scopes"),
    state: Optional[str] = Query(None, description="State parameter"),
    code_challenge: Optional[str] = Query(
        None, description="PKCE code challenge"),
    code_challenge_method: Optional[str] = Query(
        "S256", description="PKCE method"),
):
    """
    OAuth2 authorization endpoint
    Executive function accommodation: simplified flow with clear steps
    """
    provider = get_oauth_provider()
    config = get_oauth_config()

    # Validate response type
    if response_type != "code":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only 'code' response type is supported"
        )

    # Validate client
    if not provider.validate_client(client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client_id"
        )

    # Validate and parse scopes
    requested_scopes = scope.split() if scope else []
    valid_scopes = provider.validate_scopes(requested_scopes)

    # Validate PKCE if required
    if config.require_pkce and not code_challenge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code challenge required (PKCE)"
        )

    # In a real implementation, this would show a login/consent form
    # For development, we'll use a simple HTML form

    login_form_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jane Platform - Login</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', roboto, sans-serif;
                max-width: 400px; 
                margin: 100px auto; 
                padding: 20px;
                background: #f5f5f5;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{ 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
            }}
            input {{ 
                width: 100%; 
                padding: 12px; 
                margin: 8px 0; 
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
            }}
            button {{ 
                width: 100%; 
                padding: 12px; 
                background: #007bff; 
                color: white; 
                border: none;
                border-radius: 4px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
            }}
            button:hover {{ background: #0056b3; }}
            .scopes {{
                margin: 20px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 4px;
            }}
            .scope {{ margin: 5px 0; color: #666; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🤖 Jane Platform Login</h1>
            <form method="post" action="/oauth/login">
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri}">
                <input type="hidden" name="scope" value="{scope}">
                <input type="hidden" name="state" value="{state or ''}">
                <input type="hidden" name="code_challenge" value="{code_challenge or ''}">
                <input type="hidden" name="code_challenge_method" value="{code_challenge_method}">
                
                <input type="text" name="username" placeholder="Username" required 
                       value="admin" autocomplete="username">
                <input type="password" name="password" placeholder="Password" required 
                       value="admin" autocomplete="current-password">
                
                <div class="scopes">
                    <strong>Requested Permissions:</strong>
                    {chr(10).join(f'<div class="scope">• {config.available_scopes.get(s, s)}</div>' for s in valid_scopes)}
                </div>
                
                <button type="submit">Login & Authorize</button>
            </form>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=login_form_html)


@oauth_router.post("/login")
async def login_and_authorize(
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    scope: str = Form(""),
    state: Optional[str] = Form(None),
    code_challenge: Optional[str] = Form(None),
    code_challenge_method: str = Form("S256"),
    username: str = Form(...),
    password: str = Form(...)
):
    """
    Process login and generate authorization code
    Executive function accommodation: streamlined authentication
    """
    provider = get_oauth_provider()

    # Authenticate user
    user = provider.authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    # Parse and validate scopes
    requested_scopes = scope.split() if scope else []
    valid_scopes = provider.validate_scopes(requested_scopes)

    # Filter scopes based on user permissions
    user_allowed_scopes = [s for s in valid_scopes if s in user.scopes]

    # Generate authorization code
    auth_code = provider.generate_authorization_code(
        client_id=client_id,
        user_id=user.user_id,
        scopes=user_allowed_scopes,
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method
    )

    # Build redirect URL
    params = {"code": auth_code}
    if state:
        params["state"] = state

    redirect_url = f"{redirect_uri}?{urlencode(params)}"

    return RedirectResponse(url=redirect_url)


@oauth_router.post("/token", response_model=OAuth2Token)
async def token_endpoint(
    grant_type: str = Form(...),
    code: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
    client_id: str = Form(...),
    client_secret: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    code_verifier: Optional[str] = Form(None)
):
    """
    OAuth2 token endpoint
    Exchange authorization code or refresh token for access token
    """
    provider = get_oauth_provider()

    if grant_type == "authorization_code":
        if not code or not redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters for authorization_code grant"
            )

        return provider.exchange_authorization_code(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier
        )

    elif grant_type == "refresh_token":
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing refresh_token"
            )

        # Validate client
        if not provider.validate_client(client_id, client_secret):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials"
            )

        return provider.refresh_access_token(refresh_token)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported grant_type"
        )


@oauth_router.post("/revoke")
async def revoke_token(
    token: str = Form(...),
    token_type_hint: Optional[str] = Form(None),
    client_id: str = Form(...),
    client_secret: Optional[str] = Form(None)
):
    """
    OAuth2 token revocation endpoint
    Executive function accommodation: easy token management
    """
    provider = get_oauth_provider()

    # Validate client
    if not provider.validate_client(client_id, client_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )

    # Remove refresh token if it exists
    if token in provider.refresh_tokens:
        del provider.refresh_tokens[token]

    # Note: Access tokens (JWTs) can't be truly revoked without a blacklist
    # In production, implement token blacklist or short-lived tokens

    return {"message": "Token revoked successfully"}


@oauth_router.get("/userinfo", response_model=OAuth2User)
async def userinfo_endpoint(
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    OAuth2 userinfo endpoint
    Returns user information for executive function customization
    """
    return current_user


@oauth_router.get("/scopes")
async def available_scopes():
    """
    Get available OAuth2 scopes
    Executive function accommodation: clear permission descriptions
    """
    config = get_oauth_config()
    return {
        "scopes": config.available_scopes,
        "domains": {
            "security": [s for s in config.available_scopes.keys() if s.startswith("security:")],
            "productivity": [s for s in config.available_scopes.keys() if s.startswith("productivity:")],
            "mtg": [s for s in config.available_scopes.keys() if s.startswith("mtg:")],
            "infrastructure": [s for s in config.available_scopes.keys() if s.startswith("infrastructure:")]
        }
    }


# Protected API endpoints for testing
@oauth_router.get("/protected/profile")
async def protected_profile(
    current_user: OAuth2User = Depends(require_scopes("profile"))
):
    """Protected endpoint requiring 'profile' scope"""
    return {
        "message": "This is a protected endpoint",
        "user": current_user.username,
        "scopes": current_user.scopes,
        "preferences": current_user.preferences
    }


@oauth_router.get("/protected/security")
async def protected_security(
    current_user: OAuth2User = Depends(require_scopes("security:read"))
):
    """Protected endpoint requiring security domain access"""
    return {
        "message": "Security domain access granted",
        "user": current_user.username,
        "domain": "security",
        "tools": ["MISP", "HELK", "SecurityOnion", "Maltrail", "YARA-X"]
    }


@oauth_router.get("/protected/productivity")
async def protected_productivity(
    current_user: OAuth2User = Depends(require_scopes("productivity:read"))
):
    """Protected endpoint requiring productivity domain access"""
    return {
        "message": "Productivity domain access granted",
        "user": current_user.username,
        "domain": "productivity",
        "tools": ["n8n", "Mealie", "Dispatch", "Actual Budget", "Firecrawl"]
    }


# Development helper endpoints
@oauth_router.get("/dev/users")
async def list_users():
    """Development endpoint to list users"""
    provider = get_oauth_provider()
    return {
        "users": [
            {"user_id": u.user_id, "username": u.username, "scopes": u.scopes}
            for u in provider.users.values()
        ]
    }


@oauth_router.get("/dev/tokens")
async def list_active_tokens():
    """Development endpoint to list active tokens"""
    provider = get_oauth_provider()
    return {
        "active_refresh_tokens": len(provider.refresh_tokens),
        "active_auth_codes": len([c for c in provider.auth_codes.values() if not c.used])
    }
