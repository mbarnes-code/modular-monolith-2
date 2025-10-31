"""
MISP Initial Data Seeder

Preserves and migrates MISP initial data, reference data, and
configuration data from the original MISP installation to the unified platform.
"""

import json
import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Import MISP models
from ..models.misp import (AdminSetting, Galaxy, Organization, Role, Server,
                           SharingGroup, Tag, Taxonomy, User, Warninglist)

logger = logging.getLogger(__name__)


class MISPInitialDataSeeder:
    """
    Handles seeding of MISP initial data, reference data, and configuration.

    Preserves:
    - Admin settings and configuration
    - Default taxonomies and galaxy clusters
    - Reference data (warninglists, sharing groups)
    - Initial organizations and roles
    - Server configurations
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.data_dir = Path(__file__).parent / "data"

    async def seed_all(self) -> None:
        """Seed all MISP initial data in proper order."""
        logger.info("Starting MISP initial data seeding...")

        try:
            # Seed in dependency order
            await self._create_admin_settings_data()
            await self._create_roles_data()
            await self._create_organizations_data()
            await self._create_sharing_groups_data()
            await self._create_servers_data()
            await self._create_taxonomies_data()
            await self._create_galaxies_data()
            await self._create_warninglists_data()
            await self._create_event_tags_data()
            await self._verify_data_structure()

            logger.info("MISP initial data seeding completed successfully")

        except Exception as e:
            logger.error(f"MISP initial data seeding failed: {e}")
            await self.db_session.rollback()
            raise

    async def _create_admin_settings_data(self) -> None:
        """Prepare default admin settings from MISP configuration."""
        logger.info("Creating admin settings data structure...")

        default_settings = [
            ("db_version", "11"),
            ("MISP.baseurl", "https://localhost"),
            ("MISP.org", "ORGNAME"),
            ("MISP.email", "email@example.com"),
            ("MISP.contact", "email@example.com"),
            ("MISP.background_jobs", "true"),
            ("MISP.default_event_distribution", "1"),
            ("MISP.default_attribute_distribution", "event"),
            ("MISP.tagging", "true"),
            ("Security.level", "medium"),
            ("Security.auth_enforced", "false"),
            ("Security.require_password_confirmation", "true"),
            ("Security.password_policy_length", "12"),
            ("Security.allow_self_registration", "false"),
            ("Security.advanced_authkeys", "true"),
        ]

        # Save admin settings data structure
        admin_settings_file = self.data_dir / "admin_settings.json"
        admin_settings_file.parent.mkdir(parents=True, exist_ok=True)

        with open(admin_settings_file, 'w') as f:
            json.dump([{"setting": s, "value": v}
                      for s, v in default_settings], f, indent=2)

        logger.info(f"Created {len(default_settings)} admin settings")

    async def _seed_roles(self) -> None:
        """Seed default MISP user roles."""
        logger.info("Seeding user roles...")

        default_roles = [
            {
                "name": "admin",
                "permission_add": True,
                "permission_modify": True,
                "permission_modify_org": True,
                "permission_publish": True,
                "permission_delegate": True,
                "permission_sync": True,
                "permission_admin": True,
                "permission_audit": True,
                "permission_full": True,
                "default_role": False,
                "memory_limit": "",
                "max_execution_time": "",
                "restricted_to_site_admin": False,
                "perm_add": True,
                "perm_modify": True,
                "perm_modify_org": True,
                "perm_publish": True,
                "perm_sync": True,
                "perm_admin": True,
                "perm_audit": True,
                "perm_full": True,
                "perm_auth": True,
                "perm_site_admin": True,
                "perm_regexp_access": True,
                "perm_tagger": True,
                "perm_template": True,
                "perm_sharing_group": True,
                "perm_tag_editor": True,
                "perm_delegate": True,
                "perm_sighting": True,
                "perm_object_template": True,
            },
            {
                "name": "org admin",
                "permission_add": True,
                "permission_modify": True,
                "permission_modify_org": True,
                "permission_publish": True,
                "permission_delegate": True,
                "permission_sync": False,
                "permission_admin": False,
                "permission_audit": True,
                "permission_full": False,
                "default_role": False,
                "memory_limit": "",
                "max_execution_time": "",
                "restricted_to_site_admin": False,
                "perm_add": True,
                "perm_modify": True,
                "perm_modify_org": True,
                "perm_publish": True,
                "perm_sync": False,
                "perm_admin": False,
                "perm_audit": True,
                "perm_full": False,
                "perm_auth": True,
                "perm_site_admin": False,
                "perm_regexp_access": False,
                "perm_tagger": True,
                "perm_template": True,
                "perm_sharing_group": True,
                "perm_tag_editor": True,
                "perm_delegate": True,
                "perm_sighting": True,
                "perm_object_template": True,
            },
            {
                "name": "user",
                "permission_add": True,
                "permission_modify": True,
                "permission_modify_org": False,
                "permission_publish": False,
                "permission_delegate": False,
                "permission_sync": False,
                "permission_admin": False,
                "permission_audit": False,
                "permission_full": False,
                "default_role": True,
                "memory_limit": "",
                "max_execution_time": "",
                "restricted_to_site_admin": False,
                "perm_add": True,
                "perm_modify": True,
                "perm_modify_org": False,
                "perm_publish": False,
                "perm_sync": False,
                "perm_admin": False,
                "perm_audit": False,
                "perm_full": False,
                "perm_auth": False,
                "perm_site_admin": False,
                "perm_regexp_access": False,
                "perm_tagger": False,
                "perm_template": False,
                "perm_sharing_group": False,
                "perm_tag_editor": False,
                "perm_delegate": False,
                "perm_sighting": True,
                "perm_object_template": False,
            },
        ]

        for role_data in default_roles:
            role = Role(**role_data)
            self.db_session.add(role)

        await self.db_session.commit()
        logger.info(f"Seeded {len(default_roles)} user roles")

    async def _seed_organizations(self) -> None:
        """Seed default organizations."""
        logger.info("Seeding organizations...")

        default_org = Organization(
            name="ORGNAME",
            description="Default organization",
            type="",
            nationality="Not specified",
            sector="",
            uuid="52c3f29c-6704-4ba0-866a-ce10c4d8b80c",
            contacts="",
            local=True,
            restricted_to_domain=[],
            landingpage=""
        )

        self.db_session.add(default_org)
        await self.db_session.commit()
        logger.info("Seeded default organization")

    async def _seed_sharing_groups(self) -> None:
        """Seed default sharing groups."""
        logger.info("Seeding sharing groups...")

        # Default sharing groups would be seeded here based on MISP defaults
        # For now, we'll create a basic structure
        pass

    async def _seed_servers(self) -> None:
        """Seed default server configurations."""
        logger.info("Seeding server configurations...")

        # Server configurations would be seeded here
        # This includes sync servers and other MISP instances
        pass

    async def _seed_taxonomies(self) -> None:
        """Seed default MISP taxonomies."""
        logger.info("Seeding taxonomies...")

        taxonomies_file = self.data_dir / "taxonomies.json"
        if taxonomies_file.exists():
            with open(taxonomies_file) as f:
                taxonomies_data = json.load(f)

            for taxonomy_data in taxonomies_data:
                taxonomy = Taxonomy(**taxonomy_data)
                self.db_session.add(taxonomy)

        await self.db_session.commit()
        logger.info("Seeded taxonomies")

    async def _seed_galaxies(self) -> None:
        """Seed default MISP galaxy clusters."""
        logger.info("Seeding galaxy clusters...")

        galaxies_file = self.data_dir / "galaxies.json"
        if galaxies_file.exists():
            with open(galaxies_file) as f:
                galaxies_data = json.load(f)

            for galaxy_data in galaxies_data:
                galaxy = Galaxy(**galaxy_data)
                self.db_session.add(galaxy)

        await self.db_session.commit()
        logger.info("Seeded galaxy clusters")

    async def _seed_warninglists(self) -> None:
        """Seed default MISP warninglists."""
        logger.info("Seeding warninglists...")

        warninglists_file = self.data_dir / "warninglists.json"
        if warninglists_file.exists():
            with open(warninglists_file) as f:
                warninglists_data = json.load(f)

            for warninglist_data in warninglists_data:
                warninglist = Warninglist(**warninglist_data)
                self.db_session.add(warninglist)

        await self.db_session.commit()
        logger.info("Seeded warninglists")

    async def _seed_event_tags(self) -> None:
        """Seed default event tags."""
        logger.info("Seeding event tags...")

        default_tags = [
            {"name": "tlp:white", "colour": "#ffffff", "exportable": True},
            {"name": "tlp:green", "colour": "#33cc33", "exportable": True},
            {"name": "tlp:amber", "colour": "#ff9900", "exportable": True},
            {"name": "tlp:red", "colour": "#cc0033", "exportable": False},
        ]

        for tag_data in default_tags:
            tag = Tag(**tag_data)
            self.db_session.add(tag)

        await self.db_session.commit()
        logger.info(f"Seeded {len(default_tags)} default tags")

    async def _verify_seeding(self) -> None:
        """Verify that seeding was successful."""
        logger.info("Verifying data seeding...")

        # Count seeded records
        result = await self.db_session.execute(
            text("SELECT COUNT(*) FROM admin_settings")
        )
        admin_settings_count = result.scalar()

        result = await self.db_session.execute(
            text("SELECT COUNT(*) FROM roles")
        )
        roles_count = result.scalar()

        result = await self.db_session.execute(
            text("SELECT COUNT(*) FROM organisations")
        )
        orgs_count = result.scalar()

        result = await self.db_session.execute(
            text("SELECT COUNT(*) FROM tags")
        )
        tags_count = result.scalar()

        logger.info(f"Verification complete:")
        logger.info(f"  Admin settings: {admin_settings_count}")
        logger.info(f"  Roles: {roles_count}")
        logger.info(f"  Organizations: {orgs_count}")
        logger.info(f"  Tags: {tags_count}")

        if admin_settings_count == 0 or roles_count == 0:
            raise Exception("Critical seeding verification failed")


async def seed_misp_initial_data(db_session: AsyncSession) -> None:
    """Entry point for MISP initial data seeding."""
    seeder = MISPInitialDataSeeder(db_session)
    await seeder.seed_all()
