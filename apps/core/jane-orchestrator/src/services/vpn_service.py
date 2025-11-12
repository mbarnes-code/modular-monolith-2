"""
VPN/Tunnel Management Service - T142
Secure tunnel management for Jane Executive Function Platform
Executive function accommodation: automated secure connectivity
"""

import asyncio
import json
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseSettings, Field, validator


class TunnelType(Enum):
    """Types of secure tunnels"""
    WIREGUARD = "wireguard"
    OPENVPN = "openvpn"
    SSH_TUNNEL = "ssh_tunnel"
    STUNNEL = "stunnel"
    NGINX_PROXY = "nginx_proxy"


class TunnelState(Enum):
    """Tunnel connection states"""
    STOPPED = "stopped"
    STARTING = "starting"
    CONNECTED = "connected"
    DISCONNECTING = "disconnecting"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class TunnelConfiguration:
    """Tunnel configuration"""

    tunnel_id: str
    name: str
    tunnel_type: TunnelType
    description: str

    # Connection settings
    local_port: int
    remote_host: str
    remote_port: int

    # Security settings
    encryption_enabled: bool = True
    certificate_path: Optional[str] = None
    private_key_path: Optional[str] = None
    ca_cert_path: Optional[str] = None

    # Authentication
    username: Optional[str] = None
    password: Optional[str] = None
    pre_shared_key: Optional[str] = None

    # Advanced settings
    auto_start: bool = True
    reconnect_attempts: int = 3
    health_check_interval: int = 30
    timeout_seconds: int = 60

    # Executive function settings
    status_notifications: bool = True
    performance_monitoring: bool = True


class VPNConfiguration(BaseSettings):
    """VPN service configuration"""

    # Service settings
    enable_wireguard: bool = Field(
        default=True,
        description="Enable WireGuard VPN support"
    )
    enable_openvpn: bool = Field(
        default=True,
        description="Enable OpenVPN support"
    )
    enable_ssh_tunnels: bool = Field(
        default=True,
        description="Enable SSH tunnel support"
    )

    # Directory settings
    config_dir: str = Field(
        default="/etc/jane-platform/vpn",
        description="VPN configuration directory"
    )
    log_dir: str = Field(
        default="/var/log/jane-platform/vpn",
        description="VPN log directory"
    )

    # Security settings
    require_encryption: bool = Field(
        default=True,
        description="Require encryption for all tunnels"
    )
    allowed_cipher_suites: List[str] = Field(
        default=["AES-256-GCM", "ChaCha20-Poly1305"],
        description="Allowed encryption ciphers"
    )

    # Performance settings
    max_concurrent_tunnels: int = Field(
        default=10,
        description="Maximum concurrent tunnel connections"
    )
    health_check_interval: int = Field(
        default=30,
        description="Health check interval in seconds"
    )
    connection_timeout: int = Field(
        default=60,
        description="Connection timeout in seconds"
    )

    # Executive function settings
    status_update_interval: int = Field(
        default=5,
        description="Status update interval in seconds"
    )
    auto_recovery: bool = Field(
        default=True,
        description="Enable automatic tunnel recovery"
    )

    class Config:
        env_prefix = "JANE_VPN_"


@dataclass
class TunnelStatus:
    """Tunnel status information"""

    tunnel_id: str
    state: TunnelState
    connected_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    bytes_sent: int = 0
    bytes_received: int = 0
    error_message: Optional[str] = None
    process_id: Optional[int] = None

    # Performance metrics
    latency_ms: Optional[float] = None
    bandwidth_mbps: Optional[float] = None
    packet_loss_percent: Optional[float] = None


class VPNService:
    """
    VPN/Tunnel Management Service
    Manages secure tunnels with executive function accommodations
    """

    def __init__(self, config: VPNConfiguration):
        self.config = config
        self.tunnels: Dict[str, TunnelConfiguration] = {}
        self.tunnel_status: Dict[str, TunnelStatus] = {}
        self.tunnel_processes: Dict[str, subprocess.Popen] = {}

        # Setup directories
        self.config_dir = Path(config.config_dir)
        self.log_dir = Path(config.log_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Logging
        self.logger = logging.getLogger(__name__)

        # Load existing configurations
        self._load_tunnel_configurations()

    async def start_service(self):
        """Start the VPN service"""
        self.logger.info("🚀 Starting VPN/Tunnel Management Service")

        # Start background tasks
        asyncio.create_task(self._monitor_tunnels())
        asyncio.create_task(self._auto_recovery_task())
        asyncio.create_task(self._update_performance_metrics())

        # Auto-start tunnels
        for tunnel_id, tunnel_config in self.tunnels.items():
            if tunnel_config.auto_start:
                await self.start_tunnel(tunnel_id)

        self.logger.info("✅ VPN/Tunnel Management Service started")

    def _load_tunnel_configurations(self):
        """Load tunnel configurations from disk"""
        config_file = self.config_dir / "tunnels.yaml"

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    data = yaml.safe_load(f)

                for tunnel_data in data.get('tunnels', []):
                    tunnel_config = TunnelConfiguration(**tunnel_data)
                    self.tunnels[tunnel_config.tunnel_id] = tunnel_config

                    # Initialize status
                    self.tunnel_status[tunnel_config.tunnel_id] = TunnelStatus(
                        tunnel_id=tunnel_config.tunnel_id,
                        state=TunnelState.STOPPED
                    )

                self.logger.info(
                    f"Loaded {len(self.tunnels)} tunnel configurations")

            except Exception as e:
                self.logger.error(f"Failed to load tunnel configurations: {e}")

    def _save_tunnel_configurations(self):
        """Save tunnel configurations to disk"""
        config_file = self.config_dir / "tunnels.yaml"

        try:
            tunnel_data = []
            for tunnel_config in self.tunnels.values():
                tunnel_dict = {
                    'tunnel_id': tunnel_config.tunnel_id,
                    'name': tunnel_config.name,
                    'tunnel_type': tunnel_config.tunnel_type.value,
                    'description': tunnel_config.description,
                    'local_port': tunnel_config.local_port,
                    'remote_host': tunnel_config.remote_host,
                    'remote_port': tunnel_config.remote_port,
                    'encryption_enabled': tunnel_config.encryption_enabled,
                    'auto_start': tunnel_config.auto_start,
                    'reconnect_attempts': tunnel_config.reconnect_attempts,
                    'health_check_interval': tunnel_config.health_check_interval,
                    'timeout_seconds': tunnel_config.timeout_seconds,
                    'status_notifications': tunnel_config.status_notifications,
                    'performance_monitoring': tunnel_config.performance_monitoring
                }
                tunnel_data.append(tunnel_dict)

            config_data = {'tunnels': tunnel_data}

            with open(config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)

            self.logger.info("Saved tunnel configurations")

        except Exception as e:
            self.logger.error(f"Failed to save tunnel configurations: {e}")

    async def create_tunnel(
        self,
        name: str,
        tunnel_type: TunnelType,
        local_port: int,
        remote_host: str,
        remote_port: int,
        **kwargs
    ) -> str:
        """
        Create new tunnel configuration
        Executive function accommodation: simplified tunnel creation
        """
        tunnel_id = f"tunnel_{len(self.tunnels) + 1}_{tunnel_type.value}"

        tunnel_config = TunnelConfiguration(
            tunnel_id=tunnel_id,
            name=name,
            tunnel_type=tunnel_type,
            description=kwargs.get('description', f"{name} tunnel"),
            local_port=local_port,
            remote_host=remote_host,
            remote_port=remote_port,
            **kwargs
        )

        # Validate configuration
        if not await self._validate_tunnel_config(tunnel_config):
            raise ValueError("Invalid tunnel configuration")

        # Store configuration
        self.tunnels[tunnel_id] = tunnel_config
        self.tunnel_status[tunnel_id] = TunnelStatus(
            tunnel_id=tunnel_id,
            state=TunnelState.STOPPED
        )

        # Save to disk
        self._save_tunnel_configurations()

        self.logger.info(f"Created tunnel {tunnel_id}: {name}")
        return tunnel_id

    async def _validate_tunnel_config(self, config: TunnelConfiguration) -> bool:
        """Validate tunnel configuration"""
        # Check port availability
        if not self._is_port_available(config.local_port):
            self.logger.error(
                f"Local port {config.local_port} is not available")
            return False

        # Check if we exceed concurrent tunnel limit
        active_tunnels = len([
            status for status in self.tunnel_status.values()
            if status.state == TunnelState.CONNECTED
        ])

        if active_tunnels >= self.config.max_concurrent_tunnels:
            self.logger.error("Maximum concurrent tunnels limit reached")
            return False

        # Validate encryption requirements
        if self.config.require_encryption and not config.encryption_enabled:
            self.logger.error("Encryption is required but not enabled")
            return False

        return True

    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return True
        except socket.error:
            return False

    async def start_tunnel(self, tunnel_id: str) -> bool:
        """
        Start tunnel connection
        Executive function accommodation: automatic setup
        """
        tunnel_config = self.tunnels.get(tunnel_id)
        if not tunnel_config:
            self.logger.error(f"Tunnel {tunnel_id} not found")
            return False

        status = self.tunnel_status[tunnel_id]
        if status.state == TunnelState.CONNECTED:
            self.logger.info(f"Tunnel {tunnel_id} is already connected")
            return True

        status.state = TunnelState.STARTING

        try:
            # Start tunnel based on type
            if tunnel_config.tunnel_type == TunnelType.SSH_TUNNEL:
                success = await self._start_ssh_tunnel(tunnel_config)
            elif tunnel_config.tunnel_type == TunnelType.NGINX_PROXY:
                success = await self._start_nginx_proxy(tunnel_config)
            elif tunnel_config.tunnel_type == TunnelType.STUNNEL:
                success = await self._start_stunnel(tunnel_config)
            else:
                self.logger.error(
                    f"Unsupported tunnel type: {tunnel_config.tunnel_type}")
                success = False

            if success:
                status.state = TunnelState.CONNECTED
                status.connected_at = datetime.utcnow()
                status.last_activity = datetime.utcnow()
                self.logger.info(f"Started tunnel {tunnel_id}")
            else:
                status.state = TunnelState.ERROR
                status.error_message = "Failed to start tunnel"

            return success

        except Exception as e:
            status.state = TunnelState.ERROR
            status.error_message = str(e)
            self.logger.error(f"Failed to start tunnel {tunnel_id}: {e}")
            return False

    async def _start_ssh_tunnel(self, config: TunnelConfiguration) -> bool:
        """Start SSH tunnel"""
        try:
            cmd = [
                'ssh',
                '-N',  # No command
                '-L', f'{config.local_port}:{config.remote_host}:{config.remote_port}',
                '-o', 'StrictHostKeyChecking=no',
                '-o', f'ConnectTimeout={config.timeout_seconds}',
                config.remote_host
            ]

            if config.username:
                cmd.append(f'{config.username}@{config.remote_host}')

            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )

            self.tunnel_processes[config.tunnel_id] = process

            # Wait a moment to check if process started successfully
            await asyncio.sleep(2)

            if process.poll() is None:  # Process is still running
                return True
            else:
                stderr = process.stderr.read().decode() if process.stderr else ""
                self.logger.error(f"SSH tunnel failed: {stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to start SSH tunnel: {e}")
            return False

    async def _start_nginx_proxy(self, config: TunnelConfiguration) -> bool:
        """Start nginx reverse proxy tunnel"""
        try:
            # Create nginx config
            nginx_config = self._generate_nginx_config(config)
            config_path = self.config_dir / f"nginx_{config.tunnel_id}.conf"

            with open(config_path, 'w') as f:
                f.write(nginx_config)

            # Start nginx with custom config
            cmd = [
                'nginx',
                '-c', str(config_path),
                '-g', 'daemon off;'
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.tunnel_processes[config.tunnel_id] = process

            # Wait to verify startup
            await asyncio.sleep(2)
            return process.poll() is None

        except Exception as e:
            self.logger.error(f"Failed to start nginx proxy: {e}")
            return False

    def _generate_nginx_config(self, config: TunnelConfiguration) -> str:
        """Generate nginx configuration for reverse proxy"""
        return f"""
events {{
    worker_connections 1024;
}}

http {{
    upstream backend {{
        server {config.remote_host}:{config.remote_port};
    }}
    
    server {{
        listen {config.local_port};
        
        location / {{
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Executive function: fast responses
            proxy_connect_timeout 5s;
            proxy_send_timeout 10s;
            proxy_read_timeout 10s;
        }}
    }}
}}
"""

    async def _start_stunnel(self, config: TunnelConfiguration) -> bool:
        """Start stunnel for TLS tunneling"""
        try:
            # Create stunnel config
            stunnel_config = self._generate_stunnel_config(config)
            config_path = self.config_dir / f"stunnel_{config.tunnel_id}.conf"

            with open(config_path, 'w') as f:
                f.write(stunnel_config)

            cmd = ['stunnel', str(config_path)]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            self.tunnel_processes[config.tunnel_id] = process

            await asyncio.sleep(2)
            return process.poll() is None

        except Exception as e:
            self.logger.error(f"Failed to start stunnel: {e}")
            return False

    def _generate_stunnel_config(self, config: TunnelConfiguration) -> str:
        """Generate stunnel configuration"""
        return f"""
[{config.name}]
accept = {config.local_port}
connect = {config.remote_host}:{config.remote_port}
"""

    async def stop_tunnel(self, tunnel_id: str) -> bool:
        """Stop tunnel connection"""
        tunnel_config = self.tunnels.get(tunnel_id)
        if not tunnel_config:
            return False

        status = self.tunnel_status[tunnel_id]
        status.state = TunnelState.DISCONNECTING

        try:
            # Stop process if exists
            process = self.tunnel_processes.get(tunnel_id)
            if process:
                process.terminate()

                # Wait for graceful shutdown
                try:
                    await asyncio.wait_for(
                        asyncio.create_task(asyncio.to_thread(process.wait)),
                        timeout=10
                    )
                except asyncio.TimeoutError:
                    process.kill()

                del self.tunnel_processes[tunnel_id]

            status.state = TunnelState.STOPPED
            status.connected_at = None
            status.error_message = None

            self.logger.info(f"Stopped tunnel {tunnel_id}")
            return True

        except Exception as e:
            status.state = TunnelState.ERROR
            status.error_message = str(e)
            self.logger.error(f"Failed to stop tunnel {tunnel_id}: {e}")
            return False

    async def _monitor_tunnels(self):
        """Monitor tunnel health and status"""
        while True:
            try:
                for tunnel_id, status in self.tunnel_status.items():
                    if status.state == TunnelState.CONNECTED:
                        # Check if process is still running
                        process = self.tunnel_processes.get(tunnel_id)
                        if process and process.poll() is not None:
                            # Process died
                            status.state = TunnelState.ERROR
                            status.error_message = "Process terminated unexpectedly"
                            self.logger.warning(
                                f"Tunnel {tunnel_id} process died")

                        # Update last activity
                        status.last_activity = datetime.utcnow()

                await asyncio.sleep(self.config.health_check_interval)

            except Exception as e:
                self.logger.error(f"Error in tunnel monitoring: {e}")
                await asyncio.sleep(self.config.health_check_interval)

    async def _auto_recovery_task(self):
        """Automatic tunnel recovery"""
        if not self.config.auto_recovery:
            return

        while True:
            try:
                for tunnel_id, status in list(self.tunnel_status.items()):
                    tunnel_config = self.tunnels.get(tunnel_id)

                    if (status.state == TunnelState.ERROR and
                        tunnel_config and
                            tunnel_config.auto_start):

                        self.logger.info(
                            f"Attempting to recover tunnel {tunnel_id}")
                        await self.start_tunnel(tunnel_id)

                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                self.logger.error(f"Error in auto recovery: {e}")
                await asyncio.sleep(60)

    async def _update_performance_metrics(self):
        """Update performance metrics for tunnels"""
        while True:
            try:
                # This would typically query system metrics
                # For now, we'll simulate basic metrics

                for tunnel_id, status in self.tunnel_status.items():
                    if status.state == TunnelState.CONNECTED:
                        # Simulate metrics (in production, get real metrics)
                        status.latency_ms = 10.0
                        status.bandwidth_mbps = 100.0
                        status.packet_loss_percent = 0.0

                await asyncio.sleep(self.config.status_update_interval)

            except Exception as e:
                self.logger.error(f"Error updating performance metrics: {e}")
                await asyncio.sleep(self.config.status_update_interval)

    def get_tunnel_status(self, tunnel_id: str) -> Optional[Dict[str, Any]]:
        """Get tunnel status"""
        status = self.tunnel_status.get(tunnel_id)
        tunnel_config = self.tunnels.get(tunnel_id)

        if not status or not tunnel_config:
            return None

        return {
            "tunnel_id": tunnel_id,
            "name": tunnel_config.name,
            "tunnel_type": tunnel_config.tunnel_type.value,
            "state": status.state.value,
            "local_port": tunnel_config.local_port,
            "remote_host": tunnel_config.remote_host,
            "remote_port": tunnel_config.remote_port,
            "connected_at": status.connected_at.isoformat() if status.connected_at else None,
            "last_activity": status.last_activity.isoformat() if status.last_activity else None,
            "error_message": status.error_message,
            "performance_metrics": {
                "latency_ms": status.latency_ms,
                "bandwidth_mbps": status.bandwidth_mbps,
                "packet_loss_percent": status.packet_loss_percent
            }
        }

    def get_service_status(self) -> Dict[str, Any]:
        """Get VPN service status"""
        active_tunnels = len([
            status for status in self.tunnel_status.values()
            if status.state == TunnelState.CONNECTED
        ])

        return {
            "status": "running",
            "total_tunnels": len(self.tunnels),
            "active_tunnels": active_tunnels,
            "max_concurrent_tunnels": self.config.max_concurrent_tunnels,
            "auto_recovery_enabled": self.config.auto_recovery,
            "supported_types": [t.value for t in TunnelType],
            "tunnel_status": {
                tunnel_id: status.state.value
                for tunnel_id, status in self.tunnel_status.items()
            }
        }


# Global service instance
vpn_config = VPNConfiguration()
vpn_service = VPNService(vpn_config)


def get_vpn_service() -> VPNService:
    """Get VPN service instance"""
    return vpn_service


def get_vpn_config() -> VPNConfiguration:
    """Get VPN configuration"""
    return vpn_config
