"""Compression middleware preserving MISP's compression handling."""

import gzip
import logging
from typing import Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_400_BAD_REQUEST

logger = logging.getLogger(__name__)


class CompressionMiddleware(BaseHTTPMiddleware):
    """
    Compression middleware preserving MISP's compression patterns:
    - Gzip request decompression
    - Brotli request decompression (if available)
    - Content-Encoding header handling
    """

    def __init__(self, app):
        super().__init__(app)
        self.supported_encodings = self._get_supported_encodings()

    async def dispatch(self, request: Request, call_next):
        """Process request through compression middleware."""
        try:
            # Handle compressed request bodies
            content_encoding = request.headers.get("content-encoding")
            if content_encoding:
                await self._decompress_request(request, content_encoding)

            # Process request
            response = await call_next(request)

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"Compression middleware error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Compression error: {str(e)}"
            )

    async def _decompress_request(
        self,
        request: Request,
        content_encoding: str
    ) -> None:
        """Decompress request body based on content encoding."""
        if content_encoding not in self.supported_encodings:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Unsupported content encoding '{content_encoding}'"
            )

        # Get request body
        body = await request.body()
        if not body:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Request data should be compressed, but request is empty"
            )

        # Decompress based on encoding
        try:
            if content_encoding == "gzip":
                decompressed = gzip.decompress(body)
            elif content_encoding == "br":
                decompressed = self._decompress_brotli(body)
            else:
                raise ValueError(f"Unsupported encoding: {content_encoding}")

            # Replace request body with decompressed data
            request._body = decompressed

            # Update content-length header
            request.scope["headers"] = [
                (name, value) for name, value in request.scope["headers"]
                if name != b"content-length"
            ]
            request.scope["headers"].append(
                (b"content-length", str(len(decompressed)).encode())
            )

        except Exception as e:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid compressed data"
            )

    def _decompress_brotli(self, data: bytes) -> bytes:
        """Decompress Brotli data if library is available."""
        try:
            import brotli
            return brotli.decompress(data)
        except ImportError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="This server doesn't support brotli compressed requests"
            )
        except Exception:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid brotli compressed data"
            )

    def _get_supported_encodings(self) -> list[str]:
        """Get list of supported compression encodings."""
        encodings = []

        # Gzip is always supported in Python
        encodings.append("gzip")

        # Check for Brotli support
        try:
            import brotli
            encodings.append("br")
        except ImportError:
            pass

        return encodings

    def get_supported_encodings_header(self) -> str:
        """Get Accept-Encoding header value for supported encodings."""
        return ", ".join(self.supported_encodings)
