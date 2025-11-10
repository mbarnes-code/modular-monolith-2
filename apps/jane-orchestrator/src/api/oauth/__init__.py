"""
OAuth2 Authentication Module - T140
Secure authentication for Jane Executive Function Platform
"""

from .provider import (OAuth2Configuration, OAuth2Provider, OAuth2Token,
                       OAuth2User, get_current_user, get_oauth_config,
                       get_oauth_provider, require_scopes)
from .routes import oauth_router

__all__ = [
    "OAuth2Provider",
    "OAuth2Configuration",
    "OAuth2User",
    "OAuth2Token",
    "get_oauth_provider",
    "get_oauth_config",
    "get_current_user",
    "require_scopes",
    "oauth_router"
]
