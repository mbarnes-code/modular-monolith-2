"""
MISP Configuration Data Migration Scripts

Creates SQL migration scripts to preserve MISP initial data,
reference data, and configuration data in the unified platform.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MISPConfigMigrationScripts:
    """
    Generates SQL migration scripts for MISP configuration data preservation.

    Creates:
    - PostgreSQL migration scripts for initial data
    - Configuration data insertion scripts  
    - Reference data preservation scripts
    - Validation and verification scripts
    """

    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.scripts_dir = Path(__file__).parent / "migration_scripts"
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def generate_all_scripts(self) -> None:
        """Generate all migration scripts for MISP data preservation."""
        logger.info("Generating MISP configuration migration scripts...")

        try:
            self._generate_admin_settings_migration()
            self._generate_reference_data_migration()
            self._generate_configuration_migration()
            self._generate_validation_scripts()
            self._generate_master_migration_script()

            logger.info("MISP migration scripts generated successfully")

        except Exception as e:
            logger.error("Failed to generate migration scripts: %s", e)
            raise

    def _generate_admin_settings_migration(self) -> None:
        """Generate admin settings migration script."""
        logger.info("Generating admin settings migration...")

        admin_settings_file = self.data_dir / "admin_settings.json"
        with open(admin_settings_file, 'r', encoding='utf-8') as f:
            admin_settings = json.load(f)

        script_content = f"""-- MISP Admin Settings Migration
-- Generated: {datetime.now().isoformat()}
-- Task: T1682d - Preserve MISP initial data and configuration

-- Create admin_settings table if not exists
CREATE TABLE IF NOT EXISTS admin_settings (
    id SERIAL PRIMARY KEY,
    setting VARCHAR(255) NOT NULL UNIQUE,
    value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert MISP admin settings
INSERT INTO admin_settings (setting, value) VALUES
"""

        values = []
        for setting in admin_settings:
            setting_name = setting['setting'].replace("'", "''")
            setting_value = setting['value'].replace("'", "''")
            values.append(f"    ('{setting_name}', '{setting_value}')")

        script_content += ",\n".join(values)
        script_content += """
ON CONFLICT (setting) DO UPDATE SET
    value = EXCLUDED.value,
    updated_at = CURRENT_TIMESTAMP;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_admin_settings_setting ON admin_settings(setting);

-- Verify admin settings migration
SELECT COUNT(*) as admin_settings_count FROM admin_settings;
"""

        script_file = self.scripts_dir / "001_admin_settings_migration.sql"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        logger.info(f"Generated admin settings migration: {script_file}")

    def _generate_reference_data_migration(self) -> None:
        """Generate reference data migration script."""
        logger.info("Generating reference data migration...")

        reference_file = self.data_dir / "reference_data.json"
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_data = json.load(f)

        script_content = f"""-- MISP Reference Data Migration
-- Generated: {datetime.now().isoformat()}  
-- Task: T1682d - Preserve MISP reference data

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    permissions JSONB NOT NULL,
    default_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create organizations table
CREATE TABLE IF NOT EXISTS organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    uuid UUID NOT NULL UNIQUE,
    local BOOLEAN DEFAULT TRUE,
    nationality VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tags table  
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    colour VARCHAR(7) NOT NULL,
    exportable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default roles
"""

        for role in reference_data['default_roles']:
            permissions_json = json.dumps(
                role['permissions']).replace("'", "''")
            default_role = 'TRUE' if role.get(
                'default_role', False) else 'FALSE'
            role_name = role['name'].replace("'", "''")

            script_content += f"""
INSERT INTO roles (name, permissions, default_role) VALUES
    ('{role_name}', '{permissions_json}', {default_role})
ON CONFLICT (name) DO UPDATE SET
    permissions = EXCLUDED.permissions,
    default_role = EXCLUDED.default_role,
    updated_at = CURRENT_TIMESTAMP;
"""

        # Insert default organization
        org = reference_data['default_organization']
        org_name = org['name'].replace("'", "''")
        org_desc = org['description'].replace("'", "''")
        org_uuid = org['uuid']
        org_local = 'TRUE' if org['local'] else 'FALSE'
        org_nationality = org['nationality'].replace("'", "''")

        script_content += f"""
-- Insert default organization
INSERT INTO organizations (name, description, uuid, local, nationality) VALUES
    ('{org_name}', '{org_desc}', '{org_uuid}', {org_local}, '{org_nationality}')
ON CONFLICT (uuid) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    local = EXCLUDED.local,
    nationality = EXCLUDED.nationality,
    updated_at = CURRENT_TIMESTAMP;

-- Insert default tags
"""

        for tag in reference_data['default_tags']:
            tag_name = tag['name'].replace("'", "''")
            tag_colour = tag['colour']
            tag_exportable = 'TRUE' if tag['exportable'] else 'FALSE'

            script_content += f"""
INSERT INTO tags (name, colour, exportable) VALUES
    ('{tag_name}', '{tag_colour}', {tag_exportable})
ON CONFLICT (name) DO UPDATE SET
    colour = EXCLUDED.colour,
    exportable = EXCLUDED.exportable,
    updated_at = CURRENT_TIMESTAMP;
"""

        script_content += """
-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);
CREATE INDEX IF NOT EXISTS idx_organizations_uuid ON organizations(uuid);
CREATE INDEX IF NOT EXISTS idx_organizations_name ON organizations(name);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);

-- Verify reference data migration
SELECT 'Roles' as table_name, COUNT(*) as record_count FROM roles
UNION ALL
SELECT 'Organizations' as table_name, COUNT(*) as record_count FROM organizations  
UNION ALL
SELECT 'Tags' as table_name, COUNT(*) as record_count FROM tags;
"""

        script_file = self.scripts_dir / "002_reference_data_migration.sql"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        logger.info(f"Generated reference data migration: {script_file}")

    def _generate_configuration_migration(self) -> None:
        """Generate configuration mapping migration script."""
        logger.info("Generating configuration migration...")

        config_file = self.data_dir / "configuration_files.json"
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        script_content = f"""-- MISP Configuration Migration Mapping
-- Generated: {datetime.now().isoformat()}
-- Task: T1682d - Preserve MISP configuration data

-- Create configuration mapping table
CREATE TABLE IF NOT EXISTS misp_config_mapping (
    id SERIAL PRIMARY KEY,
    misp_setting VARCHAR(255) NOT NULL,
    jane_setting VARCHAR(255) NOT NULL,
    description TEXT,
    required BOOLEAN DEFAULT FALSE,
    security_sensitive BOOLEAN DEFAULT FALSE,
    migrated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert configuration mappings
"""

        for setting, details in config_data['critical_settings'].items():
            misp_setting = f"MISP.{setting}"
            jane_setting = details['migration_target']
            description = details['description'].replace("'", "''")
            required = 'TRUE' if details['required'] else 'FALSE'
            security_sensitive = 'TRUE' if details.get(
                'security_sensitive', False) else 'FALSE'

            script_content += f"""
INSERT INTO misp_config_mapping (misp_setting, jane_setting, description, required, security_sensitive) VALUES
    ('{misp_setting}', '{jane_setting}', '{description}', {required}, {security_sensitive})
ON CONFLICT (misp_setting) DO UPDATE SET
    jane_setting = EXCLUDED.jane_setting,
    description = EXCLUDED.description,
    required = EXCLUDED.required,
    security_sensitive = EXCLUDED.security_sensitive,
    updated_at = CURRENT_TIMESTAMP;
"""

        script_content += """
-- Create migration status tracking
CREATE TABLE IF NOT EXISTS migration_status (
    id SERIAL PRIMARY KEY,
    component VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    details JSONB,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert migration status tracking
INSERT INTO migration_status (component, status, details) VALUES
    ('misp_admin_settings', 'PENDING', '{"task": "T1682d", "description": "Admin settings migration"}'),
    ('misp_reference_data', 'PENDING', '{"task": "T1682d", "description": "Reference data migration"}'),
    ('misp_configuration', 'PENDING', '{"task": "T1682d", "description": "Configuration mapping"}')
ON CONFLICT (component) DO NOTHING;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_misp_config_mapping_misp_setting ON misp_config_mapping(misp_setting);
CREATE INDEX IF NOT EXISTS idx_misp_config_mapping_jane_setting ON misp_config_mapping(jane_setting);
CREATE INDEX IF NOT EXISTS idx_migration_status_component ON migration_status(component);

-- Verify configuration migration  
SELECT COUNT(*) as config_mappings_count FROM misp_config_mapping;
"""

        script_file = self.scripts_dir / "003_configuration_migration.sql"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        logger.info(f"Generated configuration migration: {script_file}")

    def _generate_validation_scripts(self) -> None:
        """Generate validation and verification scripts."""
        logger.info("Generating validation scripts...")

        script_content = f"""-- MISP Data Migration Validation
-- Generated: {datetime.now().isoformat()}
-- Task: T1682d - Validate MISP data preservation

-- Validation function for admin settings
CREATE OR REPLACE FUNCTION validate_misp_admin_settings()
RETURNS TABLE(check_name TEXT, status TEXT, expected TEXT, actual TEXT) AS $$
BEGIN
    -- Check admin settings count
    RETURN QUERY
    SELECT 
        'admin_settings_count'::TEXT as check_name,
        CASE WHEN COUNT(*) > 30 THEN 'PASS' ELSE 'FAIL' END as status,
        '> 30'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM admin_settings;
    
    -- Check critical settings exist
    RETURN QUERY
    SELECT 
        'critical_settings_exist'::TEXT as check_name,
        CASE WHEN COUNT(*) >= 8 THEN 'PASS' ELSE 'FAIL' END as status,
        '>= 8'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM admin_settings 
    WHERE setting IN (
        'MISP.baseurl', 'MISP.org', 'MISP.email', 'MISP.contact',
        'MISP.background_jobs', 'Security.level', 'Security.auth_enforced',
        'Security.require_password_confirmation'
    );
END;
$$ LANGUAGE plpgsql;

-- Validation function for reference data
CREATE OR REPLACE FUNCTION validate_misp_reference_data()
RETURNS TABLE(check_name TEXT, status TEXT, expected TEXT, actual TEXT) AS $$
BEGIN
    -- Check roles count
    RETURN QUERY
    SELECT 
        'roles_count'::TEXT as check_name,
        CASE WHEN COUNT(*) = 3 THEN 'PASS' ELSE 'FAIL' END as status,
        '= 3'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM roles;
    
    -- Check default tags count  
    RETURN QUERY
    SELECT 
        'default_tags_count'::TEXT as check_name,
        CASE WHEN COUNT(*) = 4 THEN 'PASS' ELSE 'FAIL' END as status,
        '= 4'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM tags
    WHERE name IN ('tlp:white', 'tlp:green', 'tlp:amber', 'tlp:red');
    
    -- Check default organization exists
    RETURN QUERY
    SELECT 
        'default_organization_exists'::TEXT as check_name,
        CASE WHEN COUNT(*) = 1 THEN 'PASS' ELSE 'FAIL' END as status,
        '= 1'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM organizations
    WHERE uuid = '52c3f29c-6704-4ba0-866a-ce10c4d8b80c';
END;
$$ LANGUAGE plpgsql;

-- Validation function for configuration mapping
CREATE OR REPLACE FUNCTION validate_misp_configuration()
RETURNS TABLE(check_name TEXT, status TEXT, expected TEXT, actual TEXT) AS $$
BEGIN
    -- Check configuration mappings count
    RETURN QUERY
    SELECT 
        'config_mappings_count'::TEXT as check_name,
        CASE WHEN COUNT(*) >= 8 THEN 'PASS' ELSE 'FAIL' END as status,
        '>= 8'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM misp_config_mapping;
    
    -- Check critical mappings exist
    RETURN QUERY
    SELECT 
        'critical_mappings_exist'::TEXT as check_name,
        CASE WHEN COUNT(*) >= 6 THEN 'PASS' ELSE 'FAIL' END as status,
        '>= 6'::TEXT as expected,
        COUNT(*)::TEXT as actual
    FROM misp_config_mapping
    WHERE required = TRUE;
END;
$$ LANGUAGE plpgsql;

-- Master validation function
CREATE OR REPLACE FUNCTION validate_misp_migration()
RETURNS TABLE(check_name TEXT, status TEXT, expected TEXT, actual TEXT) AS $$
BEGIN
    -- Run all validation checks
    RETURN QUERY SELECT * FROM validate_misp_admin_settings();
    RETURN QUERY SELECT * FROM validate_misp_reference_data();
    RETURN QUERY SELECT * FROM validate_misp_configuration();
END;
$$ LANGUAGE plpgsql;

-- Execute validation and show results
SELECT * FROM validate_misp_migration();

-- Update migration status on successful validation
UPDATE migration_status 
SET status = 'COMPLETED', completed_at = CURRENT_TIMESTAMP
WHERE component IN ('misp_admin_settings', 'misp_reference_data', 'misp_configuration')
AND NOT EXISTS (
    SELECT 1 FROM validate_misp_migration() WHERE status = 'FAIL'
);
"""

        script_file = self.scripts_dir / "004_validation_scripts.sql"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        logger.info(f"Generated validation scripts: {script_file}")

    def _generate_master_migration_script(self) -> None:
        """Generate master migration script that runs all migrations."""
        logger.info("Generating master migration script...")

        script_content = f"""#!/bin/bash
# MISP Data Migration Master Script
# Generated: {datetime.now().isoformat()}
# Task: T1682d - Execute all MISP data preservation migrations

set -e  # Exit on any error

echo "Starting MISP data migration..."
echo "Task: T1682d - Preserve initial data, reference data, and configuration data"

# Database connection settings (to be configured)
DB_HOST="${{POSTGRES_HOST:-localhost}}"
DB_PORT="${{POSTGRES_PORT:-5432}}"  
DB_NAME="${{POSTGRES_DB:-jane_orchestrator}}"
DB_USER="${{POSTGRES_USER:-postgres}}"

# Function to run SQL script
run_sql_script() {{
    local script_file="$1"
    local description="$2"
    
    echo "Running $description..."
    echo "Script: $script_file"
    
    if [ ! -f "$script_file" ]; then
        echo "ERROR: Script file not found: $script_file"
        exit 1
    fi
    
    psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" -f "$script_file"
    
    if [ $? -eq 0 ]; then
        echo "SUCCESS: $description completed"
    else
        echo "ERROR: $description failed"
        exit 1
    fi
    
    echo ""
}}

# Run migrations in order
echo "=== MISP Data Migration Execution ==="
echo ""

run_sql_script "001_admin_settings_migration.sql" "Admin Settings Migration"
run_sql_script "002_reference_data_migration.sql" "Reference Data Migration"  
run_sql_script "003_configuration_migration.sql" "Configuration Mapping Migration"
run_sql_script "004_validation_scripts.sql" "Validation and Verification"

echo "=== Migration Summary ==="
psql -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -U "$DB_USER" -c "
SELECT 
    component,
    status,
    completed_at,
    details->>'description' as description
FROM migration_status 
WHERE component LIKE 'misp_%'
ORDER BY component;
"

echo ""
echo "MISP data migration completed successfully!"
echo "Task T1682d: Data seeding preservation - COMPLETED"
"""

        script_file = self.scripts_dir / "run_misp_migration.sh"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Make script executable
        script_file.chmod(0o755)

        logger.info(f"Generated master migration script: {script_file}")


def generate_misp_migration_scripts() -> None:
    """Entry point for generating MISP migration scripts."""
    generator = MISPConfigMigrationScripts()
    generator.generate_all_scripts()


if __name__ == "__main__":
    generate_misp_migration_scripts()
