"""
Remote Access Service - T141  
Secure connectivity management for Jane Executive Function Platform
Executive function accommodation: reliable, low-latency remote access
"""

import asyncio
import ipaddress
import json
import logging
import socket
import ssl
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import httpx
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseSettings, Field, validator

from ..config.security import get_certificate_manager, get_tls_config


class ConnectionState(Enum):
    """Remote connection states"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"


class ConnectionType(Enum):
    """Types of remote connections"""
    WEB_BROWSER = "web_browser"
    MOBILE_APP = "mobile_app"
    API_CLIENT = "api_client"
    WEBSOCKET = "websocket"
    PWA = "pwa"


@dataclass
class RemoteConnection:
    """Remote connection tracking"""

    connection_id: str
    user_id: str
    connection_type: ConnectionType
    remote_ip: str
    user_agent: Optional[str]
    state: ConnectionState
    connected_at: datetime
    last_activity: datetime
    session_token: Optional[str] = None
    websocket: Optional[WebSocket] = None

    # Executive function accommodations
    ui_timeout_ms: int = 200  # <200ms UI response requirement
    domain_preferences: Dict[str, Any] = None
    accessibility_settings: Dict[str, Any] = None

    def __post_init__(self):
        if self.domain_preferences is None:
            self.domain_preferences = {}
        if self.accessibility_settings is None:
            self.accessibility_settings = {
                "reduced_motion": False,
                "high_contrast": False,
                "large_text": False,
                "focus_indicators": True
            }


class RemoteAccessConfiguration(BaseSettings):
    """Remote access service configuration"""

    # Connection limits
    max_connections_per_user: int = Field(
        default=5,
        description="Maximum concurrent connections per user"
    )
    max_total_connections: int = Field(
        default=1000,
        description="Maximum total concurrent connections"
    )

    # Rate limiting
    requests_per_minute: int = Field(
        default=300,  # 5 req/sec average
        description="API requests per minute limit"
    )
    burst_requests: int = Field(
        default=60,  # 1 req/sec burst
        description="Burst request limit"
    )

    # Session management
    session_timeout_minutes: int = Field(
        default=480,  # 8 hours
        description="Session timeout in minutes"
    )
    idle_timeout_minutes: int = Field(
        default=60,  # 1 hour idle
        description="Idle timeout in minutes"
    )

    # Security settings
    allowed_origins: List[str] = Field(
        default=["https://jane-platform.local", "https://localhost:3000"],
        description="Allowed CORS origins"
    )
    blocked_ips: List[str] = Field(
        default=[],
        description="Blocked IP addresses"
    )
    allowed_networks: List[str] = Field(
        default=["127.0.0.0/8", "10.0.0.0/8", "192.168.0.0/16"],
        description="Allowed network ranges"
    )

    # Performance settings
    websocket_ping_interval: int = Field(
        default=30,
        description="WebSocket ping interval in seconds"
    )
    connection_timeout_seconds: int = Field(
        default=30,
        description="Connection timeout in seconds"
    )

    # Executive function settings
    ui_response_threshold_ms: int = Field(
        default=200,  # Constitutional requirement
        description="UI response time threshold (ms)"
    )
    performance_monitoring: bool = Field(
        default=True,
        description="Enable performance monitoring"
    )

    class Config:
        env_prefix = "JANE_REMOTE_"

    @validator('allowed_networks')
    def validate_networks(cls, v):
        """Validate network CIDR ranges"""
        for network in v:
            try:
                ipaddress.ip_network(network)
            except ValueError:
                raise ValueError(f'Invalid network range: {network}')
        return v


class RemoteAccessService:
    """
    Remote Access Service for Jane Executive Function Platform
    Manages secure remote connections with performance monitoring
    """

    def __init__(self, config: RemoteAccessConfiguration):
        self.config = config
        self.connections: Dict[str, RemoteConnection] = {}
        self.user_connections: Dict[str, Set[str]] = {}
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.websockets: Dict[str, WebSocket] = {}

        # Performance monitoring
        self.performance_metrics: Dict[str, Any] = {
            "response_times": [],
            "connection_counts": [],
            "error_rates": [],
            "last_updated": datetime.utcnow()
        }

        # Logging
        self.logger = logging.getLogger(__name__)

    async def start_service(self):
        """Start the remote access service"""
        self.logger.info("🚀 Starting Remote Access Service")

        # Start background tasks
        asyncio.create_task(self._cleanup_expired_connections())
        asyncio.create_task(self._monitor_performance())
        asyncio.create_task(self._reset_rate_limits())

        self.logger.info("✅ Remote Access Service started")

    def validate_connection_request(
        self,
        remote_ip: str,
        user_agent: Optional[str] = None
    ) -> bool:
        """
        Validate incoming connection request
        Executive function accommodation: quick security validation
        """
        # Check if IP is blocked
        if remote_ip in self.config.blocked_ips:
            self.logger.warning(
                f"Blocked IP attempted connection: {remote_ip}")
            return False

        # Check if IP is in allowed networks
        try:
            remote_addr = ipaddress.ip_address(remote_ip)
            allowed = False

            for network_str in self.config.allowed_networks:
                network = ipaddress.ip_network(network_str)
                if remote_addr in network:
                    allowed = True
                    break

            if not allowed:
                self.logger.warning(f"IP not in allowed networks: {remote_ip}")
                return False

        except ValueError:
            self.logger.error(f"Invalid IP address: {remote_ip}")
            return False

        # Check connection limits
        if len(self.connections) >= self.config.max_total_connections:
            self.logger.warning("Maximum total connections reached")
            return False

        return True

    def check_rate_limit(self, user_id: str, remote_ip: str) -> bool:
        """
        Check rate limits for user/IP
        Executive function accommodation: prevent overwhelming
        """
        now = datetime.utcnow()
        key = f"{user_id}:{remote_ip}"

        if key not in self.rate_limits:
            self.rate_limits[key] = {
                "requests": [],
                "last_reset": now
            }

        rate_data = self.rate_limits[key]

        # Remove old requests (older than 1 minute)
        rate_data["requests"] = [
            req_time for req_time in rate_data["requests"]
            if now - req_time < timedelta(minutes=1)
        ]

        # Check if rate limit exceeded
        if len(rate_data["requests"]) >= self.config.requests_per_minute:
            self.logger.warning(f"Rate limit exceeded for {key}")
            return False

        # Add current request
        rate_data["requests"].append(now)
        return True

    async def create_connection(
        self,
        user_id: str,
        connection_type: ConnectionType,
        remote_ip: str,
        user_agent: Optional[str] = None,
        session_token: Optional[str] = None,
        websocket: Optional[WebSocket] = None
    ) -> Optional[RemoteConnection]:
        """
        Create new remote connection
        Executive function accommodation: streamlined connection setup
        """
        # Validate connection
        if not self.validate_connection_request(remote_ip, user_agent):
            return None

        # Check user connection limits
        user_conn_count = len(self.user_connections.get(user_id, set()))
        if user_conn_count >= self.config.max_connections_per_user:
            self.logger.warning(f"User {user_id} exceeded connection limit")
            # Close oldest connection
            await self._close_oldest_user_connection(user_id)

        # Create connection
        connection_id = str(uuid.uuid4())
        connection = RemoteConnection(
            connection_id=connection_id,
            user_id=user_id,
            connection_type=connection_type,
            remote_ip=remote_ip,
            user_agent=user_agent,
            state=ConnectionState.CONNECTING,
            connected_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            session_token=session_token,
            websocket=websocket
        )

        # Store connection
        self.connections[connection_id] = connection

        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)

        if websocket:
            self.websockets[connection_id] = websocket

        self.logger.info(
            f"Created connection {connection_id} for user {user_id}")
        return connection

    async def authenticate_connection(
        self,
        connection_id: str,
        access_token: str
    ) -> bool:
        """
        Authenticate connection with access token
        """
        connection = self.connections.get(connection_id)
        if not connection:
            return False

        # In a real implementation, validate the access token
        # For now, we'll assume it's valid if provided
        if access_token:
            connection.state = ConnectionState.AUTHENTICATED
            connection.last_activity = datetime.utcnow()
            self.logger.info(f"Authenticated connection {connection_id}")
            return True

        return False

    async def update_connection_activity(self, connection_id: str):
        """Update connection last activity timestamp"""
        connection = self.connections.get(connection_id)
        if connection:
            connection.last_activity = datetime.utcnow()

    async def send_websocket_message(
        self,
        connection_id: str,
        message: Dict[str, Any]
    ) -> bool:
        """
        Send message to WebSocket connection
        Executive function accommodation: immediate feedback
        """
        websocket = self.websockets.get(connection_id)
        if not websocket:
            return False

        try:
            start_time = datetime.utcnow()
            await websocket.send_json(message)

            # Track response time for executive function monitoring
            response_time = (datetime.utcnow() -
                             start_time).total_seconds() * 1000
            if response_time > self.config.ui_response_threshold_ms:
                self.logger.warning(
                    f"WebSocket response time {response_time:.1f}ms exceeded threshold"
                )

            await self.update_connection_activity(connection_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to send WebSocket message: {e}")
            await self.close_connection(connection_id)
            return False

    async def broadcast_to_user(
        self,
        user_id: str,
        message: Dict[str, Any],
        connection_types: Optional[List[ConnectionType]] = None
    ):
        """
        Broadcast message to all user connections
        Executive function accommodation: consistent updates
        """
        user_connection_ids = self.user_connections.get(user_id, set())

        for connection_id in user_connection_ids.copy():
            connection = self.connections.get(connection_id)
            if not connection:
                continue

            # Filter by connection type if specified
            if connection_types and connection.connection_type not in connection_types:
                continue

            if connection.connection_type == ConnectionType.WEBSOCKET:
                await self.send_websocket_message(connection_id, message)

    async def close_connection(self, connection_id: str, reason: str = "closed"):
        """Close remote connection"""
        connection = self.connections.get(connection_id)
        if not connection:
            return

        # Close WebSocket if exists
        if connection_id in self.websockets:
            try:
                await self.websockets[connection_id].close()
            except Exception:
                pass
            del self.websockets[connection_id]

        # Remove from user connections
        if connection.user_id in self.user_connections:
            self.user_connections[connection.user_id].discard(connection_id)
            if not self.user_connections[connection.user_id]:
                del self.user_connections[connection.user_id]

        # Remove connection
        del self.connections[connection_id]

        self.logger.info(f"Closed connection {connection_id}: {reason}")

    async def _close_oldest_user_connection(self, user_id: str):
        """Close the oldest connection for a user"""
        user_connection_ids = self.user_connections.get(user_id, set())
        if not user_connection_ids:
            return

        # Find oldest connection
        oldest_connection_id = None
        oldest_time = datetime.utcnow()

        for connection_id in user_connection_ids:
            connection = self.connections.get(connection_id)
            if connection and connection.connected_at < oldest_time:
                oldest_time = connection.connected_at
                oldest_connection_id = connection_id

        if oldest_connection_id:
            await self.close_connection(
                oldest_connection_id,
                "connection limit exceeded"
            )

    async def _cleanup_expired_connections(self):
        """Background task to cleanup expired connections"""
        while True:
            try:
                now = datetime.utcnow()
                expired_connections = []

                for connection_id, connection in self.connections.items():
                    # Check session timeout
                    session_age = now - connection.connected_at
                    if session_age > timedelta(minutes=self.config.session_timeout_minutes):
                        expired_connections.append(
                            (connection_id, "session timeout"))
                        continue

                    # Check idle timeout
                    idle_time = now - connection.last_activity
                    if idle_time > timedelta(minutes=self.config.idle_timeout_minutes):
                        expired_connections.append(
                            (connection_id, "idle timeout"))

                # Close expired connections
                for connection_id, reason in expired_connections:
                    await self.close_connection(connection_id, reason)

                # Sleep for 1 minute before next cleanup
                await asyncio.sleep(60)

            except Exception as e:
                self.logger.error(f"Error in connection cleanup: {e}")
                await asyncio.sleep(60)

    async def _monitor_performance(self):
        """Monitor performance metrics for executive function compliance"""
        while True:
            try:
                # Update performance metrics
                self.performance_metrics.update({
                    "active_connections": len(self.connections),
                    "websocket_connections": len(self.websockets),
                    "users_online": len(self.user_connections),
                    "last_updated": datetime.utcnow()
                })

                # Check for performance issues
                if len(self.connections) > self.config.max_total_connections * 0.8:
                    self.logger.warning("Connection count approaching limit")

                await asyncio.sleep(30)

            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
                await asyncio.sleep(30)

    async def _reset_rate_limits(self):
        """Reset rate limits periodically"""
        while True:
            try:
                await asyncio.sleep(300)  # Reset every 5 minutes

                now = datetime.utcnow()
                expired_keys = []

                for key, data in self.rate_limits.items():
                    if now - data["last_reset"] > timedelta(minutes=5):
                        expired_keys.append(key)

                for key in expired_keys:
                    del self.rate_limits[key]

            except Exception as e:
                self.logger.error(f"Error resetting rate limits: {e}")
                await asyncio.sleep(300)

    def get_connection_status(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """Get connection status"""
        connection = self.connections.get(connection_id)
        if not connection:
            return None

        return {
            "connection_id": connection.connection_id,
            "user_id": connection.user_id,
            "connection_type": connection.connection_type.value,
            "state": connection.state.value,
            "connected_at": connection.connected_at.isoformat(),
            "last_activity": connection.last_activity.isoformat(),
            "remote_ip": connection.remote_ip,
            "session_age_minutes": (
                datetime.utcnow() - connection.connected_at
            ).total_seconds() / 60
        }

    def get_service_status(self) -> Dict[str, Any]:
        """
        Get service status and metrics
        Executive function accommodation: clear system state
        """
        return {
            "status": "running",
            "active_connections": len(self.connections),
            "websocket_connections": len(self.websockets),
            "users_online": len(self.user_connections),
            "performance_metrics": self.performance_metrics,
            "configuration": {
                "max_connections_per_user": self.config.max_connections_per_user,
                "max_total_connections": self.config.max_total_connections,
                "ui_response_threshold_ms": self.config.ui_response_threshold_ms,
                "session_timeout_minutes": self.config.session_timeout_minutes
            }
        }


# Global service instance
remote_access_config = RemoteAccessConfiguration()
remote_access_service = RemoteAccessService(remote_access_config)


def get_remote_access_service() -> RemoteAccessService:
    """Get remote access service instance"""
    return remote_access_service


def get_remote_access_config() -> RemoteAccessConfiguration:
    """Get remote access configuration"""
    return remote_access_config
