"""
Search Engine Abstraction - Core Interfaces

Provides unified interface for search (Elasticsearch, PostgreSQL full-text).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class SearchOperator(Enum):
    """Search query operators"""
    AND = "and"
    OR = "or"
    NOT = "not"
    PHRASE = "phrase"
    WILDCARD = "wildcard"
    FUZZY = "fuzzy"


@dataclass
class SearchQuery:
    """
    Search query definition.

    Attributes:
        query_string: Search query text
        fields: Fields to search in
        operator: Query operator (AND, OR, etc.)
        filters: Additional filter conditions
        sort_by: Sort field
        sort_order: Sort direction (asc, desc)
        offset: Result offset for pagination
        limit: Maximum number of results
        highlight: Enable result highlighting
    """
    query_string: str
    fields: List[str] = field(default_factory=lambda: ["*"])
    operator: SearchOperator = SearchOperator.AND
    filters: Dict[str, Any] = field(default_factory=dict)
    sort_by: Optional[str] = None
    sort_order: str = "desc"
    offset: int = 0
    limit: int = 100
    highlight: bool = False


@dataclass
class SearchResult:
    """
    Search result entry.

    Attributes:
        id: Document ID
        source: Document source data
        score: Relevance score
        highlights: Highlighted text snippets
        metadata: Additional result metadata
    """
    id: str
    source: Dict[str, Any]
    score: float
    highlights: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResponse:
    """
    Search response with results.

    Attributes:
        query: Original query
        total: Total number of matching documents
        results: List of search results
        aggregations: Aggregation results
        took_ms: Query execution time
    """
    query: SearchQuery
    total: int
    results: List[SearchResult]
    aggregations: Dict[str, Any] = field(default_factory=dict)
    took_ms: float = 0.0


@dataclass
class IndexDefinition:
    """
    Search index definition.

    Attributes:
        index_name: Index name
        mappings: Field mappings and types
        settings: Index settings
    """
    index_name: str
    mappings: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)


class ISearchEngine(ABC):
    """
    Abstract interface for search engines.

    Supports:
    - Full-text search
    - Filtering and faceting
    - Aggregations
    - Index management
    - Bulk operations
    """

    @abstractmethod
    async def start(self) -> None:
        """Initialize search engine connection"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Shutdown search engine connection"""
        pass

    @abstractmethod
    async def create_index(
        self,
        definition: IndexDefinition,
    ) -> None:
        """
        Create a search index.

        Args:
            definition: Index definition

        Raises:
            SearchError: If index creation fails
        """
        pass

    @abstractmethod
    async def delete_index(
        self,
        index_name: str,
    ) -> None:
        """
        Delete a search index.

        Args:
            index_name: Index name
        """
        pass

    @abstractmethod
    async def index_document(
        self,
        index_name: str,
        document_id: str,
        document: Dict[str, Any],
    ) -> None:
        """
        Index a document.

        Args:
            index_name: Index name
            document_id: Document ID
            document: Document data
        """
        pass

    @abstractmethod
    async def index_bulk(
        self,
        index_name: str,
        documents: List[Dict[str, Any]],
    ) -> int:
        """
        Bulk index documents.

        Args:
            index_name: Index name
            documents: List of documents (must include 'id' field)

        Returns:
            Number of documents indexed
        """
        pass

    @abstractmethod
    async def delete_document(
        self,
        index_name: str,
        document_id: str,
    ) -> None:
        """
        Delete a document.

        Args:
            index_name: Index name
            document_id: Document ID
        """
        pass

    @abstractmethod
    async def search(
        self,
        index_name: str,
        query: SearchQuery,
    ) -> SearchResponse:
        """
        Execute a search query.

        Args:
            index_name: Index name
            query: Search query

        Returns:
            Search response with results
        """
        pass

    @abstractmethod
    async def suggest(
        self,
        index_name: str,
        field: str,
        text: str,
        size: int = 5,
    ) -> List[str]:
        """
        Get autocomplete suggestions.

        Args:
            index_name: Index name
            field: Field to get suggestions from
            text: Partial text
            size: Maximum number of suggestions

        Returns:
            List of suggested completions
        """
        pass

    @abstractmethod
    async def aggregate(
        self,
        index_name: str,
        aggregation: Dict[str, Any],
        query: Optional[SearchQuery] = None,
    ) -> Dict[str, Any]:
        """
        Perform aggregation query.

        Args:
            index_name: Index name
            aggregation: Aggregation definition
            query: Optional filter query

        Returns:
            Aggregation results
        """
        pass

    @abstractmethod
    async def refresh_index(
        self,
        index_name: str,
    ) -> None:
        """
        Refresh index to make recent changes visible.

        Args:
            index_name: Index name
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check search engine health.

        Returns:
            True if healthy, False otherwise
        """
        pass


class ISearchEngineFactory(ABC):
    """Factory interface for creating search engine instances"""

    @staticmethod
    @abstractmethod
    def create(
        engine_type: str,
        config: Dict[str, Any],
    ) -> ISearchEngine:
        """
        Create a search engine adapter instance.

        Args:
            engine_type: Type (elasticsearch, postgresql)
            config: Engine-specific configuration

        Returns:
            Configured search engine instance
        """
        pass


class SearchError(Exception):
    """Base exception for search errors"""
    pass


class IndexNotFoundError(SearchError):
    """Index not found"""
    pass
