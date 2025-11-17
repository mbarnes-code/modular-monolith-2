"""
Object Storage Abstraction - Core Interfaces

Provides unified interface for object storage (MinIO, S3, Local filesystem).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Dict, List, Optional


class StorageClass(Enum):
    """Storage class for objects"""
    STANDARD = "standard"
    INFREQUENT_ACCESS = "ia"
    GLACIER = "glacier"
    REDUCED_REDUNDANCY = "rr"


@dataclass
class ObjectMetadata:
    """
    Object metadata information.

    Attributes:
        key: Object key/path
        size_bytes: Object size in bytes
        content_type: MIME content type
        last_modified: Last modification timestamp
        etag: Entity tag (hash)
        storage_class: Storage tier
        metadata: Custom metadata key-value pairs
    """
    key: str
    size_bytes: int
    content_type: str = "application/octet-stream"
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: StorageClass = StorageClass.STANDARD
    metadata: Dict[str, str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class IObjectStorage(ABC):
    """
    Abstract interface for object storage systems.

    Supports:
    - Bucket/container management
    - Object CRUD operations
    - Multipart uploads
    - Presigned URLs
    - Object listing/search
    """

    @abstractmethod
    async def start(self) -> None:
        """Initialize storage connection"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Shutdown storage connection"""
        pass

    @abstractmethod
    async def create_bucket(
        self,
        bucket: str,
        region: Optional[str] = None,
    ) -> None:
        """
        Create a storage bucket/container.

        Args:
            bucket: Bucket name
            region: Storage region (if applicable)

        Raises:
            StorageError: If bucket creation fails
        """
        pass

    @abstractmethod
    async def delete_bucket(
        self,
        bucket: str,
        force: bool = False,
    ) -> None:
        """
        Delete a storage bucket.

        Args:
            bucket: Bucket name
            force: Delete even if not empty
        """
        pass

    @abstractmethod
    async def list_buckets(self) -> List[str]:
        """
        List all buckets.

        Returns:
            List of bucket names
        """
        pass

    @abstractmethod
    async def put_object(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
        storage_class: StorageClass = StorageClass.STANDARD,
    ) -> str:
        """
        Upload an object.

        Args:
            bucket: Bucket name
            key: Object key/path
            data: Object data
            content_type: MIME type
            metadata: Custom metadata
            storage_class: Storage tier

        Returns:
            Object ETag
        """
        pass

    @abstractmethod
    async def get_object(
        self,
        bucket: str,
        key: str,
    ) -> bytes:
        """
        Download an object.

        Args:
            bucket: Bucket name
            key: Object key

        Returns:
            Object data

        Raises:
            ObjectNotFoundError: If object doesn't exist
        """
        pass

    @abstractmethod
    async def delete_object(
        self,
        bucket: str,
        key: str,
    ) -> None:
        """
        Delete an object.

        Args:
            bucket: Bucket name
            key: Object key
        """
        pass

    @abstractmethod
    async def get_object_metadata(
        self,
        bucket: str,
        key: str,
    ) -> ObjectMetadata:
        """
        Get object metadata without downloading.

        Args:
            bucket: Bucket name
            key: Object key

        Returns:
            Object metadata
        """
        pass

    @abstractmethod
    async def list_objects(
        self,
        bucket: str,
        prefix: Optional[str] = None,
        recursive: bool = False,
        max_keys: int = 1000,
    ) -> AsyncIterator[ObjectMetadata]:
        """
        List objects in a bucket.

        Args:
            bucket: Bucket name
            prefix: Filter by key prefix
            recursive: List all objects recursively
            max_keys: Maximum number of results

        Yields:
            Object metadata for each object
        """
        pass

    @abstractmethod
    async def copy_object(
        self,
        source_bucket: str,
        source_key: str,
        dest_bucket: str,
        dest_key: str,
    ) -> None:
        """
        Copy an object.

        Args:
            source_bucket: Source bucket name
            source_key: Source object key
            dest_bucket: Destination bucket name
            dest_key: Destination object key
        """
        pass

    @abstractmethod
    async def generate_presigned_url(
        self,
        bucket: str,
        key: str,
        expires_seconds: int = 3600,
        method: str = "GET",
    ) -> str:
        """
        Generate a presigned URL for temporary access.

        Args:
            bucket: Bucket name
            key: Object key
            expires_seconds: URL expiration time
            method: HTTP method (GET, PUT, DELETE)

        Returns:
            Presigned URL
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check storage health.

        Returns:
            True if healthy, False otherwise
        """
        pass


class IObjectStorageFactory(ABC):
    """Factory interface for creating object storage instances"""

    @staticmethod
    @abstractmethod
    def create(
        storage_type: str,
        config: Dict[str, Any],
    ) -> IObjectStorage:
        """
        Create an object storage adapter instance.

        Args:
            storage_type: Type (minio, s3, local)
            config: Storage-specific configuration

        Returns:
            Configured object storage instance
        """
        pass


class StorageError(Exception):
    """Base exception for storage errors"""
    pass


class ObjectNotFoundError(StorageError):
    """Object not found in storage"""
    pass


class BucketNotFoundError(StorageError):
    """Bucket not found"""
    pass
