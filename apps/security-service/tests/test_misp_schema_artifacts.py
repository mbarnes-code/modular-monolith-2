"""MISP Schema Artifacts Tests

Test suite for validating MISP database schema artifacts migration.
Ensures database initialization, triggers, views, and data seeding work correctly.
"""

from unittest.mock import Mock, patch

import pytest
import sqlalchemy as sa
from apps.security_service.src.data.schema.misp_schema import (
    MispDatabaseInitializer, MispSchemaArtifacts)
from apps.security_service.src.data.seeding.misp_initial_data import (
    MispDataSeeder, run_misp_data_seeding)
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def engine():
    """Create test database engine"""
    engine = create_engine("sqlite:///:memory:", echo=False)
    return engine


@pytest.fixture
def session(engine):
    """Create database session"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def db_initializer(engine):
    """Create database initializer"""
    return MispDatabaseInitializer(str(engine.url))


@pytest.fixture
def data_seeder(session):
    """Create data seeder"""
    return MispDataSeeder(session)


class TestMispSchemaArtifacts:
    """Test MISP schema artifacts functionality"""

    def test_initialization_sql_generation(self):
        """Test SQL initialization script generation"""
        sql = MispSchemaArtifacts.get_initialization_sql()

        assert 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"' in sql
        assert 'CREATE EXTENSION IF NOT EXISTS "pgcrypto"' in sql
        assert 'CREATE TYPE misp_threat_level' in sql
        assert 'CREATE TYPE misp_analysis_status' in sql
        assert 'CREATE TYPE misp_distribution_level' in sql
        assert 'SET client_encoding = \'UTF8\'' in sql

    def test_performance_indexes_generation(self):
        """Test performance indexes SQL generation"""
        sql = MispSchemaArtifacts.get_performance_indexes()

        # Critical MISP indexes
        assert 'idx_attributes_event_id' in sql
        assert 'idx_attributes_value1_hash' in sql
        assert 'idx_attributes_fulltext' in sql
        assert 'idx_events_pagination' in sql
        assert 'idx_correlations_value' in sql

        # Ensure concurrent index creation
        assert 'CREATE INDEX CONCURRENTLY' in sql

        # Full-text search optimization
        assert 'USING gin (' in sql
        assert 'to_tsvector(' in sql

    def test_constraints_and_triggers_generation(self):
        """Test constraints and triggers SQL generation"""
        sql = MispSchemaArtifacts.get_constraints_and_triggers()

        # Foreign key constraints
        assert 'fk_events_org_id' in sql
        assert 'fk_attributes_event_id' in sql
        assert 'fk_users_org_id' in sql

        # Trigger functions
        assert 'update_event_attribute_count()' in sql
        assert 'invalidate_correlation_cache()' in sql
        assert 'maintain_correlation_consistency()' in sql

        # Trigger creation
        assert 'CREATE TRIGGER trigger_update_event_attribute_count' in sql
        assert 'CREATE TRIGGER trigger_invalidate_correlation_cache' in sql

    def test_monitoring_views_generation(self):
        """Test monitoring views SQL generation"""
        sql = MispSchemaArtifacts.get_monitoring_views()

        # Performance monitoring views
        assert 'CREATE OR REPLACE VIEW misp_event_statistics' in sql
        assert 'CREATE OR REPLACE VIEW misp_performance_metrics' in sql
        assert 'CREATE OR REPLACE VIEW misp_system_health' in sql

        # Statistics aggregation
        assert 'total_events' in sql
        assert 'published_events' in sql
        assert 'contributing_orgs' in sql

        # Health metrics
        assert 'Database Size' in sql
        assert 'Active Connections' in sql
        assert 'Cache Hit Ratio' in sql

    def test_maintenance_procedures_generation(self):
        """Test maintenance procedures SQL generation"""
        sql = MispSchemaArtifacts.get_maintenance_procedures()

        # Maintenance functions
        assert 'rebuild_correlation_cache(' in sql
        assert 'cleanup_old_data(' in sql
        assert 'update_misp_statistics()' in sql
        assert 'maintain_misp_tables()' in sql

        # Batch processing
        assert 'batch_size INTEGER DEFAULT 1000' in sql
        assert 'days_to_keep INTEGER DEFAULT 365' in sql

        # Vacuum and reindex
        assert 'VACUUM (ANALYZE)' in sql
        assert 'REINDEX INDEX CONCURRENTLY' in sql


class TestMispDatabaseInitializer:
    """Test MISP database initializer"""

    def test_schema_validation_query(self, db_initializer):
        """Test schema validation query generation"""
        query = db_initializer.get_schema_validation_query()

        assert 'table_count' in query
        assert 'view_count' in query
        assert 'index_count' in query
        assert 'trigger_count' in query
        assert 'function_count' in query

        # Check for key MISP tables
        assert 'events' in query
        assert 'attributes' in query
        assert 'organisations' in query

    @patch('apps.security_service.src.data.models.misp.MispBaseModel')
    def test_initialize_schema(self, mock_base_model, db_initializer):
        """Test complete schema initialization"""
        mock_metadata = Mock()
        mock_base_model.metadata = mock_metadata

        # Mock engine connection
        with patch.object(db_initializer.engine, 'connect') as mock_connect:
            mock_conn = Mock()
            mock_connect.return_value.__enter__.return_value = mock_conn

            db_initializer.initialize_schema()

            # Verify SQL execution calls
            assert mock_conn.execute.call_count >= 5
            assert mock_conn.commit.call_count >= 5

            # Verify metadata creation
            mock_metadata.create_all.assert_called_once_with(
                db_initializer.engine)

    @patch('apps.security_service.src.data.models.misp.ThreatLevel')
    @patch('apps.security_service.src.data.models.misp.Role')
    @patch('apps.security_service.src.data.models.misp.AdminSetting')
    def test_seed_initial_data(self, mock_admin_setting, mock_role, mock_threat_level, db_initializer):
        """Test initial data seeding"""
        with patch.object(db_initializer, 'Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session

            # Mock query results (no existing data)
            mock_session.query.return_value.filter_by.return_value.first.return_value = None

            db_initializer.seed_initial_data()

            # Verify threat levels were added
            assert mock_session.add.call_count >= 4  # At least 4 threat levels
            mock_session.commit.assert_called()


class TestMispDataSeeder:
    """Test MISP data seeder functionality"""

    def test_seed_threat_levels(self, data_seeder, session):
        """Test threat levels seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing threat levels
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_threat_levels()

            assert count == 4  # Should seed 4 threat levels
            assert session.add.call_count == 4

    def test_seed_roles(self, data_seeder, session):
        """Test roles seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing roles
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_roles()

            assert count == 6  # Should seed 6 roles
            assert session.add.call_count == 6

    def test_seed_admin_settings(self, data_seeder, session):
        """Test admin settings seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing settings
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_admin_settings()

            assert count > 50  # Should seed many admin settings
            assert session.add.call_count > 50

    def test_seed_default_taxonomies(self, data_seeder, session):
        """Test default taxonomies seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing taxonomies
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_default_taxonomies()

            assert count == 3  # Should seed 3 taxonomies (TLP, Admiralty, PAP)
            # Should add taxonomies, predicates, and entries
            assert session.add.call_count > 10
            assert session.flush.call_count > 0  # For getting IDs

    def test_seed_default_galaxies(self, data_seeder, session):
        """Test default galaxies seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing galaxies
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_default_galaxies()

            assert count == 2  # Should seed 2 galaxies (Threat Actor, Malware)
            # Should add galaxies and clusters
            assert session.add.call_count > 4
            assert session.flush.call_count > 0

    def test_seed_default_warninglists(self, data_seeder, session):
        """Test default warning lists seeding"""
        with patch.object(session, 'query') as mock_query:
            # Mock no existing warning lists
            mock_query.return_value.filter_by.return_value.first.return_value = None

            count = data_seeder.seed_default_warninglists()

            assert count == 3  # Should seed 3 warning lists
            # Should add warning lists and entries
            assert session.add.call_count > 10
            assert session.flush.call_count > 0

    def test_seed_all_initial_data(self, data_seeder, session):
        """Test complete initial data seeding"""
        with patch.object(data_seeder, 'seed_threat_levels', return_value=4), \
                patch.object(data_seeder, 'seed_roles', return_value=6), \
                patch.object(data_seeder, 'seed_admin_settings', return_value=60), \
                patch.object(data_seeder, 'seed_default_taxonomies', return_value=3), \
                patch.object(data_seeder, 'seed_default_galaxies', return_value=2), \
                patch.object(data_seeder, 'seed_default_warninglists', return_value=3), \
                patch.object(data_seeder, 'seed_notice_lists', return_value=0):

            results = data_seeder.seed_all_initial_data()

            assert results['threat_levels'] == 4
            assert results['roles'] == 6
            assert results['admin_settings'] == 60
            assert results['default_taxonomies'] == 3
            assert results['default_galaxies'] == 2
            assert results['warninglists'] == 3
            assert results['notice_lists'] == 0

    def test_verify_seeded_data(self, data_seeder, session):
        """Test seeded data verification"""
        with patch.object(session, 'query') as mock_query:
            # Mock counts for each table
            mock_query.return_value.count.side_effect = [4, 6, 60, 3, 2, 3]

            verification = data_seeder.verify_seeded_data()

            assert verification['threat_levels'] == 4
            assert verification['roles'] == 6
            assert verification['admin_settings'] == 60
            assert verification['taxonomies'] == 3
            assert verification['galaxies'] == 2
            assert verification['warninglists'] == 3
            assert verification['status'] == 'success'

    def test_verify_seeded_data_warnings(self, data_seeder, session):
        """Test seeded data verification with warnings"""
        with patch.object(session, 'query') as mock_query:
            # Mock insufficient counts
            mock_query.return_value.count.side_effect = [2, 3, 5, 1, 1, 1]

            verification = data_seeder.verify_seeded_data()

            assert verification['status'] == 'warning'
            assert 'issues' in verification
            # All three checks should fail
            assert len(verification['issues']) == 3


class TestDataSeedingIntegration:
    """Integration tests for MISP data seeding"""

    def test_run_misp_data_seeding(self):
        """Test complete data seeding workflow"""
        with patch('apps.security_service.src.data.seeding.misp_initial_data.create_engine') as mock_create_engine, \
                patch('apps.security_service.src.data.seeding.misp_initial_data.sessionmaker') as mock_session_maker:

            # Mock database components
            mock_engine = Mock()
            mock_create_engine.return_value = mock_engine

            mock_session_class = Mock()
            mock_session_maker.return_value = mock_session_class

            mock_session = Mock()
            mock_session_class.return_value.__enter__.return_value = mock_session

            # Mock seeder methods
            with patch('apps.security_service.src.data.seeding.misp_initial_data.MispDataSeeder') as mock_seeder_class:
                mock_seeder = Mock()
                mock_seeder_class.return_value = mock_seeder

                mock_seeder.seed_all_initial_data.return_value = {
                    'threat_levels': 4,
                    'roles': 6,
                    'admin_settings': 60
                }

                mock_seeder.verify_seeded_data.return_value = {
                    'threat_levels': 4,
                    'roles': 6,
                    'admin_settings': 60,
                    'status': 'success'
                }

                result = run_misp_data_seeding(
                    'postgresql://test:test@localhost/test')

                assert 'seeding_results' in result
                assert 'verification' in result
                assert result['seeding_results']['threat_levels'] == 4
                assert result['verification']['status'] == 'success'


class TestSchemaArtifactsValidation:
    """Test schema artifacts validation and compliance"""

    def test_sql_syntax_validation(self):
        """Test that generated SQL has valid syntax"""
        sql_blocks = [
            MispSchemaArtifacts.get_initialization_sql(),
            MispSchemaArtifacts.get_performance_indexes(),
            MispSchemaArtifacts.get_constraints_and_triggers(),
            MispSchemaArtifacts.get_monitoring_views(),
            MispSchemaArtifacts.get_maintenance_procedures()
        ]

        for sql in sql_blocks:
            # Basic SQL syntax checks
            assert sql.strip()  # Not empty
            assert 'CREATE' in sql.upper()
            assert sql.count('(') == sql.count(')')  # Balanced parentheses

            # PostgreSQL specific features
            if 'CREATE INDEX' in sql:
                assert 'CONCURRENTLY' in sql  # Non-blocking index creation

            if 'CREATE FUNCTION' in sql:
                assert 'LANGUAGE plpgsql' in sql  # PostgreSQL functions

    def test_performance_requirements_coverage(self):
        """Test that performance requirements are covered"""
        indexes_sql = MispSchemaArtifacts.get_performance_indexes()

        # Critical MISP performance indexes
        critical_indexes = [
            'idx_attributes_value1_hash',  # Correlation performance
            'idx_attributes_fulltext',     # Search performance
            'idx_events_pagination',       # Event listing performance
            'idx_correlations_value',      # Correlation lookup performance
        ]

        for index in critical_indexes:
            assert index in indexes_sql, f"Missing critical index: {index}"

        # Full-text search optimization
        assert 'USING gin' in indexes_sql
        assert 'to_tsvector' in indexes_sql

    def test_constitutional_compliance(self):
        """Test compliance with constitutional requirements"""
        # Security domain <1s performance requirement
        indexes_sql = MispSchemaArtifacts.get_performance_indexes()

        # Performance-critical indexes for <1s response
        security_performance_indexes = [
            'idx_attributes_event_id',      # Event attribute lookup
            'idx_events_threat_level_id',   # Threat level filtering
            'idx_correlations_value',       # Correlation queries
            'idx_sightings_attribute_id',   # Sighting lookup
        ]

        for index in security_performance_indexes:
            assert index in indexes_sql

        # Monitoring for constitutional compliance
        monitoring_sql = MispSchemaArtifacts.get_monitoring_views()
        assert 'misp_performance_metrics' in monitoring_sql
        assert 'misp_system_health' in monitoring_sql

    def test_data_integrity_preservation(self):
        """Test that data integrity is preserved"""
        constraints_sql = MispSchemaArtifacts.get_constraints_and_triggers()

        # Critical foreign key constraints
        critical_constraints = [
            'fk_attributes_event_id',      # Attribute-Event relationship
            'fk_events_org_id',           # Event-Organization relationship
            'fk_users_org_id',            # User-Organization relationship
            'fk_correlations_attribute_id'  # Correlation-Attribute relationship
        ]

        for constraint in critical_constraints:
            assert constraint in constraints_sql

        # Automatic maintenance triggers
        critical_triggers = [
            'trigger_update_event_attribute_count',
            'trigger_invalidate_correlation_cache',
            'trigger_maintain_correlation_consistency'
        ]

        for trigger in critical_triggers:
            assert trigger in constraints_sql


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
