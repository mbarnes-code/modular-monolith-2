"""Test MISP Model Relationships and Validation

Comprehensive test suite for MISP SQLAlchemy models ensuring:
- All models can be instantiated
- Relationships work correctly
- Indexes are properly defined
- Business logic is preserved
"""

from datetime import datetime

import pytest
from apps.security_service.src.data.models.misp import (AttributeTag, Event,
                                                        EventTag, Galaxy,
                                                        GalaxyCluster,
                                                        GalaxyClusterRelation,
                                                        GalaxyElement,
                                                        MispAttribute,
                                                        MispBaseModel,
                                                        MispObject,
                                                        ObjectReference,
                                                        Organisation, Role,
                                                        SharingGroup,
                                                        SharingGroupOrg,
                                                        SharingGroupServer,
                                                        Tag, ThreatLevel, User)
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def engine():
    """Create in-memory SQLite engine for testing"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    MispBaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create database session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_organisation(session):
    """Create sample organisation"""
    org = Organisation(
        name="Test Organisation",
        description="Test organisation for MISP",
        type="CERT",
        nationality="US",
        sector="Government",
        local=True
    )
    session.add(org)
    session.commit()
    return org


@pytest.fixture
def sample_user(session, sample_organisation):
    """Create sample user"""
    # Create role first
    role = Role(
        name="admin",
        created=datetime.utcnow(),
        modified=datetime.utcnow(),
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=True,
        perm_admin=True,
        perm_audit=True,
        perm_full=True,
        perm_auth=True,
        perm_site_admin=True,
        perm_regexp_access=True,
        perm_tagger=True,
        perm_template=True,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=True,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        perm_galaxy_editor=True,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_domain="",
        enforce_mfa=False
    )
    session.add(role)
    session.commit()

    user = User(
        email="test@example.com",
        org_id=sample_organisation.id,
        server_id=0,
        password="hashed_password",
        confirm_password="hashed_password",
        authkey="test_auth_key",
        invited_by=0,
        gpgkey="",
        certif_public="",
        nids_sid=0,
        terms_accepted=True,
        role_id=role.id,
        change_pw=False,
        contact_alert=False,
        disabled=False,
        expiration="0000-00-00 00:00:00",
        current_login="0000-00-00 00:00:00",
        last_login="0000-00-00 00:00:00",
        force_logout=False,
        date_created="0000-00-00 00:00:00",
        date_modified="0000-00-00 00:00:00"
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def sample_event(session, sample_organisation, sample_user):
    """Create sample event"""
    # Create threat level first
    threat_level = ThreatLevel(
        name="High",
        description="High threat level",
        form_description="High threat level form"
    )
    session.add(threat_level)
    session.commit()

    event = Event(
        org_id=sample_organisation.id,
        orgc_id=sample_organisation.id,
        user_id=sample_user.id,
        date="2024-01-01",
        threat_level_id=threat_level.id,
        info="Test Event",
        published=False,
        analysis=0,
        attribute_count=0,
        proposal_email_lock=False,
        locked=False,
        publish_timestamp=0,
        sharing_group_id=None,
        disable_correlation=False,
        extends_uuid=""
    )
    session.add(event)
    session.commit()
    return event


def test_model_table_creation(engine):
    """Test that all tables are created properly"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = [
        'events', 'attributes', 'organisations', 'users',
        'threat_levels', 'roles', 'tags', 'event_tags', 'attribute_tags',
        'sharing_groups', 'sharing_group_orgs', 'sharing_group_servers',
        'objects', 'object_references',
        'galaxies', 'galaxy_clusters', 'galaxy_elements',
        'galaxy_cluster_relations'
    ]

    for table in expected_tables:
        assert table in tables, f"Table {table} not created"


def test_organisation_creation(session):
    """Test organisation model creation and fields"""
    org = Organisation(
        name="Test Org",
        description="Test Description",
        type="CERT",
        nationality="US",
        sector="Government",
        local=True
    )
    session.add(org)
    session.commit()

    assert org.id is not None
    assert org.uuid is not None
    assert org.name == "Test Org"
    assert org.local is True


def test_event_creation(sample_event):
    """Test event model creation and relationships"""
    assert sample_event.id is not None
    assert sample_event.uuid is not None
    assert sample_event.info == "Test Event"
    assert sample_event.organisation is not None
    assert sample_event.user is not None
    assert sample_event.threat_level is not None


def test_attribute_creation(session, sample_event):
    """Test attribute model creation and relationships"""
    attr = MispAttribute(
        event_id=sample_event.id,
        object_id=None,
        object_relation=None,
        category="Network activity",
        type="ip-dst",
        value1="192.168.1.1",
        value2="",
        to_ids=True,
        uuid=None,  # Will be auto-generated
        timestamp=int(datetime.utcnow().timestamp()),
        distribution=0,
        sharing_group_id=None,
        comment="Test IP attribute",
        deleted=False,
        disable_correlation=False,
        first_seen=None,
        last_seen=None
    )
    session.add(attr)
    session.commit()

    assert attr.id is not None
    assert attr.uuid is not None
    assert attr.event == sample_event
    assert attr.category == "Network activity"
    assert attr.value1 == "192.168.1.1"


def test_misp_object_creation(session, sample_event):
    """Test MISP object model creation"""
    misp_obj = MispObject(
        name="file",
        meta_category="file",
        description="File object",
        template_uuid="688c46fb-5edb-40a3-8273-1af7923e2215",
        template_version=1,
        event_id=sample_event.id,
        comment="Test file object",
        sharing_group_id=None,
        distribution=0,
        deleted=False
    )
    session.add(misp_obj)
    session.commit()

    assert misp_obj.id is not None
    assert misp_obj.uuid is not None
    assert misp_obj.event == sample_event
    assert misp_obj.name == "file"


def test_galaxy_creation(session):
    """Test Galaxy model creation"""
    galaxy = Galaxy(
        name="Threat Actor",
        type="threat-actor",
        description="Known threat actors",
        version="1.0",
        namespace="misp",
        enabled=True
    )
    session.add(galaxy)
    session.commit()

    assert galaxy.id is not None
    assert galaxy.uuid is not None
    assert galaxy.name == "Threat Actor"
    assert galaxy.enabled is True


def test_galaxy_cluster_creation(session, sample_organisation):
    """Test Galaxy Cluster creation"""
    # First create galaxy
    galaxy = Galaxy(
        name="Threat Actor",
        type="threat-actor",
        description="Known threat actors",
        version="1.0",
        namespace="misp",
        enabled=True
    )
    session.add(galaxy)
    session.commit()

    cluster = GalaxyCluster(
        galaxy_id=galaxy.id,
        type="threat-actor",
        value="APT1",
        tag_name="misp-galaxy:threat-actor=\"APT1\"",
        description="APT1 threat actor",
        source="MISP Project",
        org_id=sample_organisation.id,
        orgc_id=sample_organisation.id,
        published=True,
        distribution=0
    )
    session.add(cluster)
    session.commit()

    assert cluster.id is not None
    assert cluster.uuid is not None
    assert cluster.galaxy == galaxy
    assert cluster.value == "APT1"


def test_object_reference_creation(session, sample_event):
    """Test ObjectReference creation"""
    # Create two objects
    obj1 = MispObject(
        name="file",
        meta_category="file",
        description="File object 1",
        template_uuid="688c46fb-5edb-40a3-8273-1af7923e2215",
        template_version=1,
        event_id=sample_event.id,
        sharing_group_id=None,
        distribution=0,
        deleted=False
    )
    obj2 = MispObject(
        name="pe",
        meta_category="file",
        description="PE object 1",
        template_uuid="cf7adecc-d4f0-4e88-9d90-f978ee151a07",
        template_version=1,
        event_id=sample_event.id,
        sharing_group_id=None,
        distribution=0,
        deleted=False
    )
    session.add_all([obj1, obj2])
    session.commit()

    # Create reference between objects
    ref = ObjectReference(
        source_uuid=obj1.uuid,
        referenced_uuid=obj2.uuid,
        relationship_type="analysed-with",
        event_id=sample_event.id,
        comment="File analysed with PE parser",
        deleted=False
    )
    session.add(ref)
    session.commit()

    assert ref.id is not None
    assert ref.uuid is not None
    assert ref.source_object == obj1
    assert ref.target_object == obj2
    assert ref.relationship_type == "analysed-with"


def test_model_indexes(engine):
    """Test that important indexes are created"""
    inspector = inspect(engine)

    # Test event indexes
    event_indexes = inspector.get_indexes('events')
    index_names = [idx['name'] for idx in event_indexes]

    # Should have UUID index
    uuid_indexes = [
        idx for idx in event_indexes if 'uuid' in idx['column_names']]
    assert len(uuid_indexes) > 0, "Events table missing UUID index"

    # Test attributes indexes
    attr_indexes = inspector.get_indexes('attributes')
    event_id_indexes = [
        idx for idx in attr_indexes if 'event_id' in idx['column_names']]
    assert len(event_id_indexes) > 0, "Attributes table missing event_id index"


def test_model_constraints(session, sample_organisation):
    """Test model constraints and validation"""
    # Test required field constraints
    with pytest.raises(IntegrityError):
        # Try to create event without required org_id
        event = Event(
            # Missing org_id - should fail
            date="2024-01-01",
            info="Test Event"
        )
        session.add(event)
        session.commit()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
