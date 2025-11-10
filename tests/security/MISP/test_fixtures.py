#!/usr/bin/env python3
"""
MISP Test Data Fixtures and Factory

Purpose: Comprehensive test data management for MISP integration testing
Requirements: Section 8.1 Test Data Management from misp-analysis.md
Coverage: Users, events, attributes, organizations with complete relationships

This module provides test fixtures matching original MISP test structure
"""

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import IntEnum
from typing import Any, Dict, List, Optional


class Distribution(IntEnum):
    """MISP distribution levels"""
    YOUR_ORGANISATION_ONLY = 0
    THIS_COMMUNITY_ONLY = 1
    CONNECTED_COMMUNITIES = 2
    ALL_COMMUNITIES = 3
    SHARING_GROUP = 4


class ThreatLevel(IntEnum):
    """MISP threat levels"""
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    UNDEFINED = 4


class Analysis(IntEnum):
    """MISP analysis levels"""
    INITIAL = 0
    ONGOING = 1
    COMPLETED = 2


@dataclass
class MISPTestOrganisation:
    """Test organization fixture"""
    id: Optional[int] = None
    uuid: Optional[str] = None
    name: str = "Test Organization"
    type: str = "Other"
    nationality: str = "US"
    sector: str = "Government"
    created_by: int = 1
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    description: str = "Test organization for MISP integration testing"
    contacts: str = "admin@test.org"
    local: bool = True
    restricted_to_domain: List[str] = None

    def __post_init__(self):
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())
        if self.date_created is None:
            self.date_created = datetime.utcnow().isoformat()
        if self.date_modified is None:
            self.date_modified = self.date_created
        if self.restricted_to_domain is None:
            self.restricted_to_domain = []


@dataclass
class MISPTestUser:
    """Test user fixture"""
    id: Optional[int] = None
    email: str = "test@example.com"
    org_id: int = 1
    role_id: int = 3  # User role
    password: str = "hashed_password"
    confirm_password: str = "hashed_password"
    authkey: Optional[str] = None
    invited_by: int = 1
    gpgkey: str = ""
    certif_public: str = ""
    autoalert: bool = True
    contactalert: bool = True
    disabled: bool = False
    change_pw: int = 0
    termsaccepted: bool = True
    date_created: Optional[str] = None
    date_modified: Optional[str] = None

    def __post_init__(self):
        if self.authkey is None:
            self.authkey = str(uuid.uuid4()).replace('-', '')
        if self.date_created is None:
            self.date_created = datetime.utcnow().isoformat()
        if self.date_modified is None:
            self.date_modified = self.date_created


@dataclass
class MISPTestAttribute:
    """Test attribute fixture"""
    id: Optional[int] = None
    uuid: Optional[str] = None
    event_id: Optional[int] = None
    object_id: int = 0
    object_relation: Optional[str] = None
    category: str = "Network activity"
    type: str = "domain"
    value: str = "malicious.example.com"
    to_ids: bool = True
    distribution: int = Distribution.YOUR_ORGANISATION_ONLY
    sharing_group_id: Optional[int] = None
    timestamp: Optional[int] = None
    comment: str = ""
    deleted: bool = False
    disable_correlation: bool = False
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None

    def __post_init__(self):
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = int(datetime.utcnow().timestamp())


@dataclass
class MISPTestEvent:
    """Test event fixture"""
    id: Optional[int] = None
    uuid: Optional[str] = None
    org_id: int = 1
    orgc_id: int = 1
    user_id: int = 1
    info: str = "Test Malware Campaign"
    date: Optional[str] = None
    threat_level_id: int = ThreatLevel.MEDIUM
    analysis: int = Analysis.COMPLETED
    distribution: int = Distribution.YOUR_ORGANISATION_ONLY
    sharing_group_id: Optional[int] = None
    published: bool = False
    timestamp: Optional[int] = None
    publish_timestamp: Optional[int] = None
    disable_correlation: bool = False
    locked: bool = False
    extends_uuid: str = ""
    event_creator_email: str = "test@example.com"
    protected: Optional[bool] = None
    attributes: List[MISPTestAttribute] = None
    tags: List[Dict[str, Any]] = None
    galaxy_clusters: List[Dict[str, Any]] = None

    def __post_init__(self):
        if self.uuid is None:
            self.uuid = str(uuid.uuid4())
        if self.date is None:
            self.date = datetime.utcnow().strftime('%Y-%m-%d')
        if self.timestamp is None:
            self.timestamp = int(datetime.utcnow().timestamp())
        if self.attributes is None:
            self.attributes = []
        if self.tags is None:
            self.tags = []
        if self.galaxy_clusters is None:
            self.galaxy_clusters = []


class MISPTestDataFactory:
    """Factory for creating comprehensive MISP test data"""

    @staticmethod
    def create_organisation(name: str = None, **kwargs) -> MISPTestOrganisation:
        """Create test organisation with optional customization"""
        defaults = {
            'name': name or f"Test Org {uuid.uuid4().hex[:8]}"
        }
        defaults.update(kwargs)
        return MISPTestOrganisation(**defaults)

    @staticmethod
    def create_user(email: str = None, org_id: int = 1, **kwargs) -> MISPTestUser:
        """Create test user with optional customization"""
        defaults = {
            'email': email or f"test_{uuid.uuid4().hex[:8]}@example.com",
            'org_id': org_id
        }
        defaults.update(kwargs)
        return MISPTestUser(**defaults)

    @staticmethod
    def create_attribute(category: str = None, attr_type: str = None,
                         value: str = None, **kwargs) -> MISPTestAttribute:
        """Create test attribute with optional customization"""
        defaults = {}
        if category:
            defaults['category'] = category
        if attr_type:
            defaults['type'] = attr_type
        if value:
            defaults['value'] = value
        defaults.update(kwargs)
        return MISPTestAttribute(**defaults)

    @staticmethod
    def create_event(info: str = None, **kwargs) -> MISPTestEvent:
        """Create test event with optional customization"""
        defaults = {}
        if info:
            defaults['info'] = info
        defaults.update(kwargs)
        return MISPTestEvent(**defaults)

    @staticmethod
    def create_complete_event(event_info: str = None,
                              num_attributes: int = 3) -> MISPTestEvent:
        """Create complete event with attributes and tags"""
        event = MISPTestDataFactory.create_event(
            info=event_info or f"Complete Test Event {uuid.uuid4().hex[:8]}"
        )

        # Add sample attributes
        sample_attributes = [
            {'category': 'Network activity', 'type': 'domain',
                'value': 'malicious1.example.com'},
            {'category': 'Payload delivery', 'type': 'md5',
                'value': 'd41d8cd98f00b204e9800998ecf8427e'},
            {'category': 'Artifacts dropped',
                'type': 'filename', 'value': 'malware.exe'},
            {'category': 'Network activity',
                'type': 'ip-src', 'value': '192.168.1.100'},
            {'category': 'Payload delivery', 'type': 'sha256',
                'value': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'}
        ]

        for i in range(min(num_attributes, len(sample_attributes))):
            attr_data = sample_attributes[i]
            attribute = MISPTestDataFactory.create_attribute(**attr_data)
            event.attributes.append(attribute)

        # Add sample tags
        event.tags = [
            {'name': 'tlp:white', 'colour': '#ffffff'},
            {'name': 'misp-galaxy:threat-actor="APT29"', 'colour': '#ff0000'},
            {'name': 'admiralty-scale:source-reliability="b"', 'colour': '#ffaa00'}
        ]

        return event

    @staticmethod
    def create_correlation_test_events() -> List[MISPTestEvent]:
        """Create events specifically for correlation testing"""
        events = []

        # Event 1: Initial compromise
        event1 = MISPTestDataFactory.create_event(
            info="Initial Compromise - APT Campaign"
        )
        event1.attributes = [
            MISPTestDataFactory.create_attribute(
                category='Network activity',
                type='domain',
                value='common-malicious.com'
            ),
            MISPTestDataFactory.create_attribute(
                category='Payload delivery',
                type='md5',
                value='abc123def456789012345678901234567'
            )
        ]
        events.append(event1)

        # Event 2: Lateral movement (shares domain)
        event2 = MISPTestDataFactory.create_event(
            info="Lateral Movement - Same Campaign"
        )
        event2.attributes = [
            MISPTestDataFactory.create_attribute(
                category='Network activity',
                type='domain',
                value='common-malicious.com'  # Same domain for correlation
            ),
            MISPTestDataFactory.create_attribute(
                category='Network activity',
                type='ip-src',
                value='10.0.0.50'
            )
        ]
        events.append(event2)

        # Event 3: Data exfiltration (shares IP)
        event3 = MISPTestDataFactory.create_event(
            info="Data Exfiltration - Final Stage"
        )
        event3.attributes = [
            MISPTestDataFactory.create_attribute(
                category='Network activity',
                type='ip-src',
                value='10.0.0.50'  # Same IP for correlation
            ),
            MISPTestDataFactory.create_attribute(
                category='Artifacts dropped',
                type='filename',
                value='stolen_data.zip'
            )
        ]
        events.append(event3)

        return events

    @staticmethod
    def create_performance_test_dataset(num_events: int = 100) -> List[MISPTestEvent]:
        """Create large dataset for performance testing"""
        events = []

        for i in range(num_events):
            event = MISPTestDataFactory.create_event(
                info=f"Performance Test Event {i+1}"
            )

            # Add 2-5 attributes per event
            num_attrs = (i % 4) + 2
            for j in range(num_attrs):
                attr_type = ['domain', 'ip-src',
                             'md5', 'filename', 'url'][j % 5]
                category = {
                    'domain': 'Network activity',
                    'ip-src': 'Network activity',
                    'md5': 'Payload delivery',
                    'filename': 'Artifacts dropped',
                    'url': 'Network activity'
                }[attr_type]

                value = {
                    'domain': f'perf-test-{i}-{j}.com',
                    'ip-src': f'192.168.{i % 255}.{j + 1}',
                    'md5': f'{str(uuid.uuid4()).replace("-", "")[:32]}',
                    'filename': f'test_file_{i}_{j}.exe',
                    'url': f'https://perf-test-{i}-{j}.com/malware'
                }[attr_type]

                attribute = MISPTestDataFactory.create_attribute(
                    category=category,
                    type=attr_type,
                    value=value
                )
                event.attributes.append(attribute)

            events.append(event)

        return events

    @staticmethod
    def create_taxonomy_test_data() -> Dict[str, Any]:
        """Create taxonomy and galaxy test data"""
        return {
            'taxonomies': [
                {
                    'id': 1,
                    'namespace': 'tlp',
                    'description': 'Traffic Light Protocol',
                    'version': '1',
                    'enabled': True,
                    'predicates': [
                        {'value': 'white', 'expanded': 'TLP:WHITE'},
                        {'value': 'green', 'expanded': 'TLP:GREEN'},
                        {'value': 'amber', 'expanded': 'TLP:AMBER'},
                        {'value': 'red', 'expanded': 'TLP:RED'}
                    ]
                },
                {
                    'id': 2,
                    'namespace': 'admiralty-scale',
                    'description': 'Admiralty Scale for reliability and credibility',
                    'version': '1',
                    'enabled': True,
                    'predicates': [
                        {'value': 'source-reliability',
                            'expanded': 'Source Reliability'},
                        {'value': 'information-credibility',
                            'expanded': 'Information Credibility'}
                    ]
                }
            ],
            'galaxy_clusters': [
                {
                    'id': 1,
                    'uuid': str(uuid.uuid4()),
                    'value': 'APT29',
                    'tag_name': 'misp-galaxy:threat-actor="APT29"',
                    'description': 'Advanced Persistent Threat group',
                    'galaxy_id': 1,
                    'source': 'MISP Galaxy',
                    'authors': ['MISP Project'],
                    'version': '1',
                    'published': True
                },
                {
                    'id': 2,
                    'uuid': str(uuid.uuid4()),
                    'value': 'Emotet',
                    'tag_name': 'misp-galaxy:malware="Emotet"',
                    'description': 'Banking Trojan and malware loader',
                    'galaxy_id': 2,
                    'source': 'MISP Galaxy',
                    'authors': ['MISP Project'],
                    'version': '1',
                    'published': True
                }
            ]
        }

    @staticmethod
    def create_feed_test_data() -> Dict[str, Any]:
        """Create feed configuration and content for testing"""
        return {
            'feed_config': {
                'id': 1,
                'name': 'Test Threat Intelligence Feed',
                'provider': 'Security Research Lab',
                'url': 'https://feeds.securitylab.com/misp-format.json',
                'rules': json.dumps({
                    'tags': ['feed:test', 'tlp:white'],
                    'default_event_distribution': 0,
                    'default_attribute_distribution': 0
                }),
                'enabled': True,
                'caching_enabled': True,
                'lookup_visible': True,
                'headers': json.dumps({
                    'Authorization': 'Bearer test-token',
                    'User-Agent': 'MISP-Feed-Client/1.0'
                }),
                'format': 'misp'
            },
            'feed_content': [
                {
                    'uuid': str(uuid.uuid4()),
                    'info': 'Malicious Domain Feed Entry',
                    'threat_level_id': ThreatLevel.MEDIUM,
                    'analysis': Analysis.COMPLETED,
                    'distribution': Distribution.YOUR_ORGANISATION_ONLY,
                    'Attribute': [
                        {
                            'category': 'Network activity',
                            'type': 'domain',
                            'value': 'feed-malicious.com',
                            'to_ids': True,
                            'distribution': Distribution.YOUR_ORGANISATION_ONLY
                        }
                    ]
                },
                {
                    'uuid': str(uuid.uuid4()),
                    'info': 'IP Blacklist Feed Entry',
                    'threat_level_id': ThreatLevel.HIGH,
                    'analysis': Analysis.COMPLETED,
                    'distribution': Distribution.YOUR_ORGANISATION_ONLY,
                    'Attribute': [
                        {
                            'category': 'Network activity',
                            'type': 'ip-src',
                            'value': '203.0.113.100',
                            'to_ids': True,
                            'distribution': Distribution.YOUR_ORGANISATION_ONLY
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def create_sharing_group_test_data() -> Dict[str, Any]:
        """Create sharing group test configuration"""
        return {
            'sharing_group': {
                'id': 1,
                'uuid': str(uuid.uuid4()),
                'name': 'Test Sharing Group',
                'description': 'Test sharing group for integration testing',
                'releasability': 'Test partners only',
                'created': datetime.utcnow().isoformat(),
                'modified': datetime.utcnow().isoformat(),
                'local': True,
                'active': True,
                'sync_user_id': 1,
                'organisation_uuid': str(uuid.uuid4()),
                'roaming': False
            },
            'sharing_group_orgs': [
                {
                    'id': 1,
                    'sharing_group_id': 1,
                    'org_id': 1,
                    'extend': True
                },
                {
                    'id': 2,
                    'sharing_group_id': 1,
                    'org_id': 2,
                    'extend': False
                }
            ]
        }

    @staticmethod
    def export_fixtures_to_json(output_dir: str = "./fixtures") -> None:
        """Export all test fixtures to JSON files for use in tests"""
        import json
        import os

        os.makedirs(output_dir, exist_ok=True)

        # Export organizations
        orgs = [
            asdict(MISPTestDataFactory.create_organisation("Test Org 1")),
            asdict(MISPTestDataFactory.create_organisation(
                "Test Org 2", sector="Private")),
            asdict(MISPTestDataFactory.create_organisation(
                "Test Org 3", nationality="UK"))
        ]
        with open(f"{output_dir}/organisations.json", 'w') as f:
            json.dump(orgs, f, indent=2)

        # Export users
        users = [
            asdict(MISPTestDataFactory.create_user(
                "admin@test.com", role_id=1)),
            asdict(MISPTestDataFactory.create_user(
                "orgadmin@test.com", role_id=2)),
            asdict(MISPTestDataFactory.create_user("user@test.com", role_id=3))
        ]
        with open(f"{output_dir}/users.json", 'w') as f:
            json.dump(users, f, indent=2, default=str)

        # Export events with attributes
        events = [
            asdict(MISPTestDataFactory.create_complete_event("Test Event 1", 3)),
            asdict(MISPTestDataFactory.create_complete_event("Test Event 2", 4)),
            asdict(MISPTestDataFactory.create_complete_event("Test Event 3", 2))
        ]
        with open(f"{output_dir}/events.json", 'w') as f:
            json.dump(events, f, indent=2, default=str)

        # Export correlation test data
        correlation_events = [
            asdict(event) for event in MISPTestDataFactory.create_correlation_test_events()]
        with open(f"{output_dir}/correlation_events.json", 'w') as f:
            json.dump(correlation_events, f, indent=2, default=str)

        # Export taxonomy and galaxy data
        taxonomy_data = MISPTestDataFactory.create_taxonomy_test_data()
        with open(f"{output_dir}/taxonomy_data.json", 'w') as f:
            json.dump(taxonomy_data, f, indent=2, default=str)

        # Export feed test data
        feed_data = MISPTestDataFactory.create_feed_test_data()
        with open(f"{output_dir}/feed_data.json", 'w') as f:
            json.dump(feed_data, f, indent=2, default=str)

        # Export sharing group data
        sharing_data = MISPTestDataFactory.create_sharing_group_test_data()
        with open(f"{output_dir}/sharing_group_data.json", 'w') as f:
            json.dump(sharing_data, f, indent=2, default=str)


if __name__ == '__main__':
    # Generate all test fixtures
    factory = MISPTestDataFactory()

    # Create fixture directory
    fixture_dir = "/workspaces/modular-monolith-2/tests/security/MISP/fixtures"
    factory.export_fixtures_to_json(fixture_dir)

    print(f"MISP test fixtures exported to {fixture_dir}")
    print("Fixtures include:")
    print("- organisations.json (3 test organizations)")
    print("- users.json (3 test users with different roles)")
    print("- events.json (3 complete test events with attributes)")
    print("- correlation_events.json (3 events for correlation testing)")
    print("- taxonomy_data.json (taxonomies and galaxy clusters)")
    print("- feed_data.json (feed configuration and content)")
    print("- sharing_group_data.json (sharing group configuration)")
