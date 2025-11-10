"""
MISP External Integrations Manager

This module handles external integrations for MISP as required by T1895b.
Maintains service contracts while integrating with the unified monolith stack.

External integrations include:
- STIX/TAXII feeds
- CVE vulnerability databases
- Threat intelligence feeds
- External MISP instances
- Third-party security tools
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import aiohttp
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class ExternalIntegrationManager:
    """
    Manages external integrations for MISP while maintaining service contracts.

    This class preserves MISP's external integration patterns while providing
    unified interface for the Jane security domain.
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize external integration manager."""
        self.config = config

        # Integration endpoints
        self.integrations = {
            'cve_lookup': {
                'url': config.get('cve_url', 'https://vulnerability.circl.lu/vuln/'),
                'enabled': config.get('cve_lookup_enabled', True),
                'timeout': 10,
                'cache_ttl': 3600
            },
            'stix_feeds': {
                'enabled': config.get('stix_enabled', True),
                'supported_versions': ['2.0', '2.1'],
                'export_timeout': 30
            },
            'threat_feeds': {
                'enabled': config.get('threat_feeds_enabled', True),
                'feed_urls': config.get('feed_urls', []),
                'update_interval': config.get('feed_update_interval', 3600)
            },
            'external_misp': {
                'enabled': config.get('external_misp_enabled', False),
                'instances': config.get('external_misp_instances', []),
                'sync_interval': config.get('misp_sync_interval', 86400)
            },
            'taxii_feeds': {
                'enabled': config.get('taxii_enabled', False),
                'servers': config.get('taxii_servers', []),
                'poll_interval': config.get('taxii_poll_interval', 3600)
            }
        }

        # HTTP session with retry strategy
        self._session = self._create_http_session()

        # Cache for external data
        self._cache = {}

        logger.info(
            f"External integration manager initialized with "
            f"{len([i for i in self.integrations.values() if i.get('enabled')])} "
            f"active integrations"
        )

    def _create_http_session(self) -> requests.Session:
        """Create HTTP session with retry strategy."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'User-Agent': 'Jane-MISP-Integration/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        return session

    async def initialize_integrations(self) -> None:
        """Initialize all enabled external integrations."""
        try:
            initialization_results = {}

            for integration_name, integration_config in self.integrations.items():
                if integration_config.get('enabled', False):
                    try:
                        result = await self._initialize_integration(
                            integration_name, integration_config
                        )
                        initialization_results[integration_name] = result
                        logger.info(
                            f"Integration {integration_name}: initialized")
                    except Exception as e:
                        initialization_results[integration_name] = {
                            'success': False,
                            'error': str(e)
                        }
                        logger.error(
                            f"Integration {integration_name} failed: {e}")

            self._integration_status = initialization_results
            logger.info("External integrations initialization completed")

        except Exception as e:
            logger.error(f"Integration initialization failed: {e}")
            raise

    async def _initialize_integration(
        self,
        name: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Initialize specific integration."""
        if name == 'cve_lookup':
            return await self._init_cve_lookup(config)
        elif name == 'stix_feeds':
            return await self._init_stix_feeds(config)
        elif name == 'threat_feeds':
            return await self._init_threat_feeds(config)
        elif name == 'external_misp':
            return await self._init_external_misp(config)
        elif name == 'taxii_feeds':
            return await self._init_taxii_feeds(config)
        else:
            return {'success': False, 'error': f'Unknown integration: {name}'}

    # CVE Lookup Integration

    async def _init_cve_lookup(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize CVE vulnerability lookup integration."""
        try:
            # Test CVE service connectivity
            test_url = f"{config['url']}CVE-2021-44228"  # Log4j vulnerability

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._session.get(test_url, timeout=config['timeout'])
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'service_url': config['url'],
                    'response_time_ms': response.elapsed.total_seconds() * 1000
                }
            else:
                return {
                    'success': False,
                    'error': f'CVE service returned {response.status_code}'
                }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def lookup_cve(self, cve_id: str) -> Optional[Dict[str, Any]]:
        """
        Lookup CVE vulnerability information.

        Maintains MISP's CVE lookup service contract.
        """
        if not self.integrations['cve_lookup']['enabled']:
            return None

        try:
            # Check cache first
            cache_key = f"cve:{cve_id}"
            if cache_key in self._cache:
                cached_data = self._cache[cache_key]
                if datetime.now().timestamp() - cached_data['timestamp'] < 3600:
                    return cached_data['data']

            # Fetch from external service
            url = f"{self.integrations['cve_lookup']['url']}{cve_id}"

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._session.get(
                    url,
                    timeout=self.integrations['cve_lookup']['timeout']
                )
            )

            if response.status_code == 200:
                cve_data = response.json()

                # Normalize CVE data to MISP format
                normalized_data = await self._normalize_cve_data(cve_data)

                # Cache the result
                self._cache[cache_key] = {
                    'data': normalized_data,
                    'timestamp': datetime.now().timestamp()
                }

                return normalized_data

        except Exception as e:
            logger.error(f"CVE lookup failed for {cve_id}: {e}")

        return None

    async def _normalize_cve_data(self, cve_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize CVE data to MISP attribute format."""
        return {
            'cve_id': cve_data.get('id', ''),
            'description': cve_data.get('summary', ''),
            'cvss_score': cve_data.get('cvss', 0.0),
            'published_date': cve_data.get('Published', ''),
            'modified_date': cve_data.get('Modified', ''),
            'references': cve_data.get('references', []),
            'cwe_id': cve_data.get('cwe', ''),
            'source': 'circl_cve_lookup'
        }

    # STIX Export Integration

    async def _init_stix_feeds(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize STIX format support."""
        try:
            # Check STIX library availability
            import stix2

            return {
                'success': True,
                'supported_versions': config['supported_versions'],
                'library_version': stix2.__version__
            }

        except ImportError:
            return {
                'success': False,
                'error': 'STIX2 library not available'
            }

    async def export_stix(
        self,
        misp_events: List[Dict[str, Any]],
        version: str = "2.1"
    ) -> Dict[str, Any]:
        """
        Export MISP events to STIX format.

        Maintains MISP's STIX export service contract.
        """
        if not self.integrations['stix_feeds']['enabled']:
            raise RuntimeError("STIX integration not enabled")

        try:
            import stix2

            stix_objects = []

            for event in misp_events:
                # Convert MISP event to STIX indicator
                stix_indicator = await self._convert_misp_to_stix(event, version)
                if stix_indicator:
                    stix_objects.extend(stix_indicator)

            # Create STIX bundle
            bundle = stix2.Bundle(*stix_objects)

            return {
                'success': True,
                'stix_bundle': bundle.serialize(pretty=True),
                'version': version,
                'object_count': len(stix_objects),
                'export_timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"STIX export failed: {e}")
            raise

    async def _convert_misp_to_stix(
        self,
        misp_event: Dict[str, Any],
        version: str
    ) -> List[Any]:
        """Convert MISP event to STIX objects."""
        try:
            import stix2

            stix_objects = []

            # Create STIX indicator from MISP attributes
            attributes = misp_event.get('attributes', [])

            for attribute in attributes:
                if attribute.get('to_ids', False):  # Only IDS-enabled attributes
                    pattern = await self._create_stix_pattern(attribute)
                    if pattern:
                        indicator = stix2.Indicator(
                            pattern=pattern,
                            labels=["malicious-activity"],
                            created=datetime.now(),
                            modified=datetime.now()
                        )
                        stix_objects.append(indicator)

            return stix_objects

        except Exception as e:
            logger.error(f"MISP to STIX conversion failed: {e}")
            return []

    async def _create_stix_pattern(self, attribute: Dict[str, Any]) -> Optional[str]:
        """Create STIX pattern from MISP attribute."""
        attr_type = attribute.get('type', '')
        attr_value = attribute.get('value', '')

        # Map MISP attribute types to STIX patterns
        pattern_mappings = {
            'md5': f"[file:hashes.MD5 = '{attr_value}']",
            'sha1': f"[file:hashes.SHA-1 = '{attr_value}']",
            'sha256': f"[file:hashes.SHA-256 = '{attr_value}']",
            'ip-src': f"[network-traffic:src_ref.value = '{attr_value}']",
            'ip-dst': f"[network-traffic:dst_ref.value = '{attr_value}']",
            'domain': f"[domain-name:value = '{attr_value}']",
            'url': f"[url:value = '{attr_value}']",
            'hostname': f"[domain-name:value = '{attr_value}']"
        }

        return pattern_mappings.get(attr_type)

    # Threat Feed Integration

    async def _init_threat_feeds(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize threat feed integration."""
        try:
            feed_urls = config.get('feed_urls', [])

            if not feed_urls:
                return {
                    'success': True,
                    'message': 'No threat feeds configured',
                    'feed_count': 0
                }

            # Test connectivity to feeds
            active_feeds = 0
            for feed_url in feed_urls:
                try:
                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(
                        None,
                        lambda: self._session.head(feed_url, timeout=10)
                    )
                    if response.status_code == 200:
                        active_feeds += 1
                except Exception:
                    pass

            return {
                'success': True,
                'configured_feeds': len(feed_urls),
                'active_feeds': active_feeds,
                'update_interval': config.get('update_interval', 3600)
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def fetch_threat_feeds(self) -> List[Dict[str, Any]]:
        """Fetch data from configured threat feeds."""
        if not self.integrations['threat_feeds']['enabled']:
            return []

        feed_data = []
        feed_urls = self.integrations['threat_feeds'].get('feed_urls', [])

        for feed_url in feed_urls:
            try:
                data = await self._fetch_single_feed(feed_url)
                if data:
                    feed_data.append({
                        'source': feed_url,
                        'data': data,
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                logger.error(f"Failed to fetch feed {feed_url}: {e}")

        return feed_data

    async def _fetch_single_feed(self, feed_url: str) -> Optional[Dict[str, Any]]:
        """Fetch data from a single threat feed."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._session.get(feed_url, timeout=30)
            )

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')

                if 'json' in content_type:
                    return response.json()
                elif 'xml' in content_type:
                    # Handle XML feeds (would need XML parsing)
                    return {'xml_content': response.text}
                else:
                    return {'text_content': response.text}

        except Exception as e:
            logger.error(f"Feed fetch failed: {e}")

        return None

    # External MISP Instance Integration

    async def _init_external_misp(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize external MISP instance integration."""
        try:
            instances = config.get('instances', [])

            if not instances:
                return {
                    'success': True,
                    'message': 'No external MISP instances configured',
                    'instance_count': 0
                }

            # Test connectivity to external instances
            active_instances = 0
            for instance in instances:
                try:
                    # Test connection to external MISP
                    url = f"{instance['url']}/servers/getPyMISPVersion.json"
                    headers = {'Authorization': instance['api_key']}

                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(
                        None,
                        lambda: self._session.get(
                            url,
                            headers=headers,
                            timeout=10,
                            verify=instance.get('verify_ssl', True)
                        )
                    )

                    if response.status_code == 200:
                        active_instances += 1

                except Exception:
                    pass

            return {
                'success': True,
                'configured_instances': len(instances),
                'active_instances': active_instances,
                'sync_interval': config.get('sync_interval', 86400)
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    # TAXII Feed Integration

    async def _init_taxii_feeds(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize TAXII feed integration."""
        try:
            servers = config.get('servers', [])

            if not servers:
                return {
                    'success': True,
                    'message': 'No TAXII servers configured',
                    'server_count': 0
                }

            # Would implement TAXII client integration here
            # For now, return basic configuration status

            return {
                'success': True,
                'configured_servers': len(servers),
                'poll_interval': config.get('poll_interval', 3600),
                'implementation_status': 'basic_support'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    async def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all external integrations."""
        status = {
            'integration_manager': 'active',
            'timestamp': datetime.now().isoformat(),
            'integrations': {}
        }

        for name, config in self.integrations.items():
            status['integrations'][name] = {
                'enabled': config.get('enabled', False),
                'status': self._integration_status.get(name, {})
            }

        return status

    async def cleanup(self) -> None:
        """Cleanup external integration resources."""
        try:
            if self._session:
                self._session.close()

            logger.info("External integration manager cleanup completed")

        except Exception as e:
            logger.error(f"External integration cleanup failed: {e}")
