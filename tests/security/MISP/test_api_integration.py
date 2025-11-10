#!/usr/bin/env python3
"""
MISP API Integration Tests

Purpose: Test MISP API endpoint preservation and compatibility
Requirements: Section 3.2 (API Architecture) from misp-analysis.md
Coverage: REST API endpoints, authentication, request/response validation

This test suite validates API compatibility with original MISP behavior
"""

from libs.service_adapters.security.misp_adapter import MISPAdapter
from api.security import router as security_router
import json
# Import integrated MISP service components
import sys
import time
import uuid
from typing import Any, Dict
from unittest.mock import patch

import pytest
import requests_mock

sys.path.append('/workspaces/modular-monolith-2/apps/jane-orchestrator/src')


class TestMISPAPIIntegration:
    """Test suite for MISP API integration and compatibility"""

    @pytest.fixture
    async def misp_adapter(self):
        """Initialize MISP adapter for API testing"""
        adapter = MISPAdapter()
        await adapter.initialize()
        return adapter

    @pytest.fixture
    def api_client(self):
        """FastAPI test client for MISP endpoints"""
        from api.main import create_app
        from fastapi.testclient import TestClient

        app = create_app()
        return TestClient(app)

    @pytest.fixture
    def mock_misp_response(self):
        """Mock MISP API responses for testing"""
        return {
            'events': [
                {
                    'Event': {
                        'id': '1',
                        'uuid': str(uuid.uuid4()),
                        'info': 'Test Event',
                        'threat_level_id': '2',
                        'published': False,
                        'analysis': '0',
                        'distribution': '0',
                        'Attribute': []
                    }
                }
            ]
        }

    def test_events_list_endpoint_compatibility(self, api_client, mock_misp_response):
        """
        Test: /events endpoint maintains MISP API compatibility
        Coverage: Events listing with pagination and filters
        Requirement: API compatibility preservation Section 3.2
        """
        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/events/index.json',
                json=mock_misp_response
            )

            response = api_client.get('/api/misp/events')

            assert response.status_code == 200
            data = response.json()

            # Validate MISP-compatible response structure
            assert 'response' in data
            assert isinstance(data['response'], list)
            if data['response']:
                event = data['response'][0]
                assert 'Event' in event
                assert 'id' in event['Event']
                assert 'uuid' in event['Event']
                assert 'info' in event['Event']

    def test_events_search_endpoint(self, api_client):
        """
        Test: /events/restSearch endpoint behavior preservation
        Coverage: Advanced search with filters and conditions
        Requirement: Search functionality preservation
        """
        search_payload = {
            'value': 'malicious.com',
            'type': 'domain',
            'category': 'Network activity',
            'eventinfo': 'APT',
            'tags': ['tlp:white'],
            'from': '2024-01-01',
            'to': '2024-12-31'
        }

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/events/restSearch.json',
                json={'response': []}
            )

            response = api_client.post(
                '/api/misp/events/search',
                json=search_payload
            )

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data

    def test_event_creation_endpoint(self, api_client):
        """
        Test: POST /events endpoint for event creation
        Coverage: Event creation with attributes and validation
        Requirement: Event creation workflow preservation
        """
        event_data = {
            'info': 'Test Malware Campaign',
            'distribution': 0,
            'threat_level_id': 2,
            'analysis': 2,
            'Attribute': [
                {
                    'category': 'Network activity',
                    'type': 'domain',
                    'value': 'test.malicious.com',
                    'to_ids': True,
                    'distribution': 0
                }
            ]
        }

        mock_response = {
            'Event': {
                'id': '123',
                'uuid': str(uuid.uuid4()),
                **event_data
            }
        }

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/events/add.json',
                json=mock_response
            )

            response = api_client.post(
                '/api/misp/events',
                json=event_data
            )

            assert response.status_code == 201
            data = response.json()
            assert 'Event' in data
            assert data['Event']['info'] == event_data['info']

    def test_attributes_search_endpoint(self, api_client):
        """
        Test: /attributes/restSearch endpoint compatibility
        Coverage: Attribute search and filtering capabilities
        Requirement: Attribute search preservation Section 3.2
        """
        search_data = {
            'value': 'example.com',
            'type': 'domain',
            'category': 'Network activity',
            'to_ids': True
        }

        mock_response = {
            'response': {
                'Attribute': [
                    {
                        'id': '456',
                        'uuid': str(uuid.uuid4()),
                        'event_id': '123',
                        'category': 'Network activity',
                        'type': 'domain',
                        'value': 'example.com',
                        'to_ids': True
                    }
                ]
            }
        }

        with requests_mock.Mocker() as m:
            m.post(
                'http://localhost:8080/attributes/restSearch.json',
                json=mock_response
            )

            response = api_client.post(
                '/api/misp/attributes/search',
                json=search_data
            )

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data
            assert 'Attribute' in data['response']

    def test_organisations_endpoint(self, api_client):
        """
        Test: /organisations endpoint functionality
        Coverage: Organization management and listing
        Requirement: Organization handling preservation
        """
        mock_orgs = {
            'response': [
                {
                    'Organisation': {
                        'id': '1',
                        'name': 'Test Organization',
                        'uuid': str(uuid.uuid4()),
                        'type': 'Other',
                        'nationality': 'US',
                        'sector': 'Government'
                    }
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/organisations/index.json',
                json=mock_orgs
            )

            response = api_client.get('/api/misp/organisations')

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data
            if data['response']:
                org = data['response'][0]
                assert 'Organisation' in org

    def test_users_endpoint_authentication(self, api_client):
        """
        Test: /users endpoint with authentication
        Coverage: User management and authentication flows
        Requirement: Authentication preservation Section 3.1
        """
        # Test without authentication (should fail)
        response = api_client.get('/api/misp/users')
        assert response.status_code == 401

        # Test with valid authentication
        headers = {'Authorization': 'Bearer valid_test_token'}
        mock_users = {
            'response': [
                {
                    'User': {
                        'id': '1',
                        'email': 'test@example.com',
                        'role_id': '3',
                        'org_id': '1'
                    }
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/users/index.json',
                json=mock_users
            )

            response = api_client.get('/api/misp/users', headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data

    def test_taxonomies_endpoint(self, api_client):
        """
        Test: /taxonomies endpoint for classification systems
        Coverage: Taxonomy and tagging system integration
        Requirement: Classification system preservation
        """
        mock_taxonomies = {
            'response': [
                {
                    'Taxonomy': {
                        'id': '1',
                        'namespace': 'tlp',
                        'description': 'Traffic Light Protocol',
                        'version': '1',
                        'enabled': True
                    }
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/taxonomies/index.json',
                json=mock_taxonomies
            )

            response = api_client.get('/api/misp/taxonomies')

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data
            if data['response']:
                taxonomy = data['response'][0]
                assert 'Taxonomy' in taxonomy

    def test_galaxy_clusters_endpoint(self, api_client):
        """
        Test: /galaxy_clusters endpoint for threat intelligence
        Coverage: MISP Galaxy integration and cluster management
        Requirement: Galaxy system preservation
        """
        mock_clusters = {
            'response': [
                {
                    'GalaxyCluster': {
                        'id': '1',
                        'uuid': str(uuid.uuid4()),
                        'value': 'APT29',
                        'tag_name': 'misp-galaxy:threat-actor="APT29"',
                        'description': 'Advanced Persistent Threat group'
                    }
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/galaxy_clusters/index.json',
                json=mock_clusters
            )

            response = api_client.get('/api/misp/galaxy_clusters')

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data

    def test_feeds_management_endpoint(self, api_client):
        """
        Test: /feeds endpoint for feed management
        Coverage: External feed integration and processing
        Requirement: Feed management preservation Section 5.1
        """
        mock_feeds = {
            'response': [
                {
                    'Feed': {
                        'id': '1',
                        'name': 'Test Threat Feed',
                        'provider': 'Security Vendor',
                        'url': 'https://feeds.example.com/threats.json',
                        'enabled': True,
                        'caching_enabled': True
                    }
                }
            ]
        }

        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/feeds/index.json',
                json=mock_feeds
            )

            response = api_client.get('/api/misp/feeds')

            assert response.status_code == 200
            data = response.json()
            assert 'response' in data

    def test_api_performance_requirements(self, api_client):
        """
        Test: API response time meets security domain requirements
        Coverage: Performance benchmarks Section 8.1
        Requirement: <1s response time for security domain
        """
        endpoints_to_test = [
            '/api/misp/events',
            '/api/misp/organisations',
            '/api/misp/taxonomies'
        ]

        for endpoint in endpoints_to_test:
            with requests_mock.Mocker() as m:
                m.get(
                    f'http://localhost:8080{endpoint.replace("/api/misp", "")}/index.json',
                    json={'response': []}
                )

                start_time = time.time()
                response = api_client.get(endpoint)
                response_time = time.time() - start_time

                assert response.status_code == 200
                assert response_time < 1.0, (
                    f"Endpoint {endpoint} took {response_time:.2f}s, "
                    f"exceeds 1s security domain requirement"
                )

    def test_error_handling_compatibility(self, api_client):
        """
        Test: Error responses match MISP format
        Coverage: Error handling patterns Section 3.1
        Requirement: Error response compatibility
        """
        # Test 404 error format
        with requests_mock.Mocker() as m:
            m.get(
                'http://localhost:8080/events/view/999999.json',
                status_code=404,
                json={'message': 'Invalid event.'}
            )

            response = api_client.get('/api/misp/events/999999')

            assert response.status_code == 404
            data = response.json()
            assert 'message' in data or 'errors' in data

        # Test validation error format
        invalid_event = {
            'info': '',  # Required field empty
            'distribution': 99  # Invalid value
        }

        response = api_client.post('/api/misp/events', json=invalid_event)

        assert response.status_code == 422
        data = response.json()
        assert 'errors' in data or 'detail' in data

    def test_pagination_and_limits(self, api_client):
        """
        Test: Pagination parameters work correctly
        Coverage: Pagination handling in list endpoints
        Requirement: Large dataset handling preservation
        """
        # Test with pagination parameters
        params = {
            'page': 1,
            'limit': 10
        }

        with requests_mock.Mocker() as m:
            mock_response = {
                'response': [{'Event': {'id': str(i)}} for i in range(10)]
            }
            m.get(
                'http://localhost:8080/events/index.json',
                json=mock_response
            )

            response = api_client.get('/api/misp/events', params=params)

            assert response.status_code == 200
            data = response.json()
            assert len(data['response']) <= 10


if __name__ == '__main__':
    # Run API integration tests
    pytest.main([
        __file__,
        '-v',
        '--cov=api.security',
        '--cov=libs.service_adapters.security.misp_adapter',
        '--tb=short'
    ])
