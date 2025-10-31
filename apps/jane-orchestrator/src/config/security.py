"""
HTTPS and TLS Security Configuration - T139
Constitutional requirement for secure remote access to 37-tool platform
"""

import datetime
import ipaddress
import os
import ssl
from pathlib import Path
from typing import Any, Dict, List, Optional

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from pydantic import BaseSettings, Field, validator


class TLSConfiguration(BaseSettings):
    """
    TLS/HTTPS configuration for secure remote access
    Executive function accommodation: simplified certificate management
    """

    # Certificate paths
    cert_file: str = Field(
        default="certs/jane-platform.crt",
        description="Path to TLS certificate file"
    )
    key_file: str = Field(
        default="certs/jane-platform.key",
        description="Path to private key file"
    )
    ca_file: Optional[str] = Field(
        default=None,
        description="Path to CA certificate file (for client auth)"
    )

    # Certificate settings
    cert_valid_days: int = Field(
        default=365, description="Certificate validity in days")
    key_size: int = Field(default=2048, description="RSA key size in bits")

    # TLS Protocol settings
    min_tls_version: str = Field(
        default="1.2",
        description="Minimum TLS version (1.2 or 1.3)"
    )
    cipher_suites: List[str] = Field(
        default=[
            "ECDHE+AESGCM",
            "ECDHE+CHACHA20",
            "DHE+AESGCM",
            "DHE+CHACHA20",
            "!aNULL",
            "!MD5",
            "!DSS"
        ],
        description="Allowed cipher suites"
    )

    # Certificate subject information
    cert_country: str = Field(
        default="US", description="Certificate country code")
    cert_state: str = Field(
        default="", description="Certificate state/province")
    cert_city: str = Field(default="", description="Certificate city/locality")
    cert_org: str = Field(
        default="Jane Executive Function Platform",
        description="Organization name"
    )
    cert_org_unit: str = Field(
        default="Mental Prosthetic Infrastructure",
        description="Organizational unit"
    )
    cert_common_name: str = Field(
        default="jane-platform.local",
        description="Certificate common name (domain)"
    )

    # Subject Alternative Names
    cert_san_dns: List[str] = Field(
        default=["jane-platform.local", "localhost", "jane.local"],
        description="DNS names for certificate SAN"
    )
    cert_san_ip: List[str] = Field(
        default=["127.0.0.1", "::1"],
        description="IP addresses for certificate SAN"
    )

    # Security settings
    require_client_cert: bool = Field(
        default=False,
        description="Require client certificate authentication"
    )
    verify_client_cert: bool = Field(
        default=False,
        description="Verify client certificate against CA"
    )

    # HSTS settings
    enable_hsts: bool = Field(
        default=True,
        description="Enable HTTP Strict Transport Security"
    )
    hsts_max_age: int = Field(
        default=31536000,  # 1 year
        description="HSTS max-age in seconds"
    )
    hsts_include_subdomains: bool = Field(
        default=True,
        description="Include subdomains in HSTS"
    )
    hsts_preload: bool = Field(
        default=False,
        description="Enable HSTS preload"
    )

    class Config:
        env_prefix = "JANE_TLS_"
        case_sensitive = False

    @validator('min_tls_version')
    def validate_tls_version(cls, v):
        """Validate TLS version"""
        if v not in ['1.2', '1.3']:
            raise ValueError('TLS version must be 1.2 or 1.3')
        return v

    @validator('cert_san_ip')
    def validate_ip_addresses(cls, v):
        """Validate IP addresses in SAN"""
        for ip in v:
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                raise ValueError(f'Invalid IP address: {ip}')
        return v


class CertificateManager:
    """
    Certificate management for Jane Executive Function Platform
    Handles certificate generation, validation, and renewal
    """

    def __init__(self, config: TLSConfiguration):
        self.config = config
        self.cert_dir = Path("certs")
        self.cert_dir.mkdir(exist_ok=True)

    def generate_self_signed_certificate(self) -> tuple[str, str]:
        """
        Generate self-signed certificate for development/internal use
        Returns: (cert_path, key_path)
        """
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.config.key_size,
        )

        # Create certificate subject
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.config.cert_country),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,
                               self.config.cert_state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.config.cert_city),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME,
                               self.config.cert_org),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME,
                               self.config.cert_org_unit),
            x509.NameAttribute(NameOID.COMMON_NAME,
                               self.config.cert_common_name),
        ])

        # Build SAN extension
        san_list = []

        # Add DNS names
        for dns_name in self.config.cert_san_dns:
            san_list.append(x509.DNSName(dns_name))

        # Add IP addresses
        for ip_str in self.config.cert_san_ip:
            san_list.append(x509.IPAddress(ipaddress.ip_address(ip_str)))

        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            subject  # Self-signed
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=self.config.cert_valid_days)
        ).add_extension(
            x509.SubjectAlternativeName(san_list),
            critical=False,
        ).add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.oid.ExtendedKeyUsageOID.SERVER_AUTH,
            ]),
            critical=True,
        ).sign(private_key, hashes.SHA256())

        # Save certificate
        cert_path = self.cert_dir / Path(self.config.cert_file).name
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        # Save private key
        key_path = self.cert_dir / Path(self.config.key_file).name
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        return str(cert_path), str(key_path)

    def validate_certificate(self, cert_path: str) -> Dict[str, Any]:
        """
        Validate existing certificate
        Returns validation status and certificate info
        """
        try:
            with open(cert_path, "rb") as f:
                cert_data = f.read()

            cert = x509.load_pem_x509_certificate(cert_data)

            # Check validity period
            now = datetime.datetime.utcnow()
            is_valid = cert.not_valid_before <= now <= cert.not_valid_after
            days_until_expiry = (cert.not_valid_after - now).days

            # Extract certificate info
            subject = cert.subject
            issuer = cert.issuer

            # Get SAN extension
            san_extension = None
            try:
                san_extension = cert.extensions.get_extension_for_oid(
                    x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
                ).value
            except x509.ExtensionNotFound:
                pass

            return {
                "valid": is_valid,
                "days_until_expiry": days_until_expiry,
                "subject": str(subject),
                "issuer": str(issuer),
                "serial_number": str(cert.serial_number),
                "not_valid_before": cert.not_valid_before.isoformat(),
                "not_valid_after": cert.not_valid_after.isoformat(),
                "san_dns": [str(name) for name in (san_extension or []) if isinstance(name, x509.DNSName)],
                "san_ip": [str(ip) for ip in (san_extension or []) if isinstance(ip, x509.IPAddress)],
                "key_usage": str(cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.KEY_USAGE).value) if x509.oid.ExtensionOID.KEY_USAGE in [ext.oid for ext in cert.extensions] else None
            }

        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }

    def get_ssl_context(self) -> ssl.SSLContext:
        """
        Create SSL context for secure connections
        Executive function accommodation: pre-configured security
        """
        # Create SSL context
        if self.config.min_tls_version == "1.3":
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_3
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Load certificate and key
        cert_path = Path(self.config.cert_file)
        key_path = Path(self.config.key_file)

        # Generate certificate if it doesn't exist
        if not cert_path.exists() or not key_path.exists():
            print("🔐 Generating self-signed certificate for development...")
            cert_path_str, key_path_str = self.generate_self_signed_certificate()
            cert_path = Path(cert_path_str)
            key_path = Path(key_path_str)

        context.load_cert_chain(str(cert_path), str(key_path))

        # Configure cipher suites
        context.set_ciphers(":".join(self.config.cipher_suites))

        # Client certificate verification
        if self.config.require_client_cert:
            context.verify_mode = ssl.CERT_REQUIRED
            if self.config.ca_file:
                context.load_verify_locations(self.config.ca_file)
        elif self.config.verify_client_cert:
            context.verify_mode = ssl.CERT_OPTIONAL
            if self.config.ca_file:
                context.load_verify_locations(self.config.ca_file)
        else:
            context.verify_mode = ssl.CERT_NONE

        return context

    def get_hsts_header(self) -> Optional[str]:
        """Get HSTS header value if enabled"""
        if not self.config.enable_hsts:
            return None

        header_parts = [f"max-age={self.config.hsts_max_age}"]

        if self.config.hsts_include_subdomains:
            header_parts.append("includeSubDomains")

        if self.config.hsts_preload:
            header_parts.append("preload")

        return "; ".join(header_parts)


# Global configuration instance
tls_config = TLSConfiguration()
certificate_manager = CertificateManager(tls_config)


def get_tls_config() -> TLSConfiguration:
    """Get TLS configuration instance"""
    return tls_config


def get_certificate_manager() -> CertificateManager:
    """Get certificate manager instance"""
    return certificate_manager


def setup_https_middleware():
    """
    Setup HTTPS middleware for FastAPI
    Returns middleware configuration
    """
    from fastapi import Request, Response
    from fastapi.middleware.base import BaseHTTPMiddleware

    class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
        """Redirect HTTP to HTTPS"""

        async def dispatch(self, request: Request, call_next):
            # In production, redirect HTTP to HTTPS
            if (request.url.scheme == "http" and
                    os.getenv("JANE_ENV", "development") == "production"):

                https_url = request.url.replace(scheme="https")
                return Response(
                    status_code=301,
                    headers={"Location": str(https_url)}
                )

            response = await call_next(request)

            # Add HSTS header
            hsts_header = certificate_manager.get_hsts_header()
            if hsts_header:
                response.headers["Strict-Transport-Security"] = hsts_header

            # Add other security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

            return response

    return HTTPSRedirectMiddleware


if __name__ == "__main__":
    """CLI for certificate management"""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Jane Platform Certificate Manager"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate new self-signed certificate"
    )
    parser.add_argument(
        "--validate",
        metavar="CERT_PATH",
        help="Validate existing certificate"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show current TLS configuration"
    )

    args = parser.parse_args()

    manager = get_certificate_manager()

    if args.generate:
        print("🔐 Generating self-signed certificate...")
        cert_path, key_path = manager.generate_self_signed_certificate()
        print(f"✅ Certificate generated:")
        print(f"   Certificate: {cert_path}")
        print(f"   Private Key: {key_path}")

        # Validate generated certificate
        validation = manager.validate_certificate(cert_path)
        print(f"   Valid for: {validation.get('days_until_expiry', 0)} days")

    elif args.validate:
        print(f"🔍 Validating certificate: {args.validate}")
        validation = manager.validate_certificate(args.validate)
        print(json.dumps(validation, indent=2))

    elif args.info:
        print("📋 TLS Configuration:")
        config = get_tls_config()
        print(f"   Certificate: {config.cert_file}")
        print(f"   Private Key: {config.key_file}")
        print(f"   Min TLS Version: {config.min_tls_version}")
        print(f"   HSTS Enabled: {config.enable_hsts}")
        print(f"   Common Name: {config.cert_common_name}")
        print(f"   SAN DNS: {', '.join(config.cert_san_dns)}")

    else:
        parser.print_help()
