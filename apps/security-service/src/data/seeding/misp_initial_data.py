"""MISP Initial Data Seeding

Data seeding scripts for MISP initial configuration and reference data.
Preserves initial taxonomies, galaxies, threat levels, and system configuration.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class MispDataSeeder:
    """Handles seeding of initial MISP data"""

    def __init__(self, session: Session):
        self.session = session

    def seed_all_initial_data(self) -> Dict[str, int]:
        """Seed all initial MISP data and return counts"""
        results = {}

        try:
            results['threat_levels'] = self.seed_threat_levels()
            results['roles'] = self.seed_roles()
            results['admin_settings'] = self.seed_admin_settings()
            results['default_taxonomies'] = self.seed_default_taxonomies()
            results['default_galaxies'] = self.seed_default_galaxies()
            results['warninglists'] = self.seed_default_warninglists()
            results['notice_lists'] = self.seed_notice_lists()

            self.session.commit()
            logger.info(f"Successfully seeded initial MISP data: {results}")

        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to seed initial MISP data: {e}")
            raise

        return results

    def seed_threat_levels(self) -> int:
        """Seed default threat levels"""
        from apps.security_service.src.data.models.misp import ThreatLevel

        threat_levels_data = [
            {
                'id': 1,
                'name': 'High',
                'description': 'High threat level - immediate attention required',
                'form_description': 'High'
            },
            {
                'id': 2,
                'name': 'Medium',
                'description': 'Medium threat level - attention required',
                'form_description': 'Medium'
            },
            {
                'id': 3,
                'name': 'Low',
                'description': 'Low threat level - minimal risk',
                'form_description': 'Low'
            },
            {
                'id': 4,
                'name': 'Undefined',
                'description': 'Undefined threat level - risk assessment pending',
                'form_description': 'Undefined'
            }
        ]

        count = 0
        for tl_data in threat_levels_data:
            existing = self.session.query(ThreatLevel).filter_by(
                id=tl_data['id']
            ).first()

            if not existing:
                threat_level = ThreatLevel(**tl_data)
                self.session.add(threat_level)
                count += 1

        return count

    def seed_roles(self) -> int:
        """Seed default user roles"""
        from apps.security_service.src.data.models.misp import Role

        roles_data = [
            {
                'id': 1,
                'name': 'admin',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': True,
                'perm_modify': True,
                'perm_modify_org': True,
                'perm_publish': True,
                'perm_delegate': True,
                'perm_sync': True,
                'perm_admin': True,
                'perm_audit': True,
                'perm_auth': True,
                'perm_site_admin': True,
                'perm_regexp_access': True,
                'perm_tagger': True,
                'perm_template': True,
                'perm_sharing_group': True,
                'perm_tag_editor': True,
                'perm_sighting': True,
                'perm_object_template': True,
                'default_role': False,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': True,
                'perm_publish_kafka': True,
                'perm_decaying': True
            },
            {
                'id': 2,
                'name': 'Org Admin',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': True,
                'perm_modify': True,
                'perm_modify_org': True,
                'perm_publish': True,
                'perm_delegate': True,
                'perm_sync': True,
                'perm_admin': False,
                'perm_audit': True,
                'perm_auth': True,
                'perm_site_admin': False,
                'perm_regexp_access': False,
                'perm_tagger': True,
                'perm_template': True,
                'perm_sharing_group': True,
                'perm_tag_editor': True,
                'perm_sighting': True,
                'perm_object_template': True,
                'default_role': False,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': False,
                'perm_publish_kafka': False,
                'perm_decaying': True
            },
            {
                'id': 3,
                'name': 'User',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': True,
                'perm_modify': True,
                'perm_modify_org': False,
                'perm_publish': False,
                'perm_delegate': False,
                'perm_sync': False,
                'perm_admin': False,
                'perm_audit': False,
                'perm_auth': False,
                'perm_site_admin': False,
                'perm_regexp_access': False,
                'perm_tagger': True,
                'perm_template': False,
                'perm_sharing_group': False,
                'perm_tag_editor': False,
                'perm_sighting': True,
                'perm_object_template': False,
                'default_role': True,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': False,
                'perm_publish_kafka': False,
                'perm_decaying': False
            },
            {
                'id': 4,
                'name': 'Publisher',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': True,
                'perm_modify': True,
                'perm_modify_org': False,
                'perm_publish': True,
                'perm_delegate': False,
                'perm_sync': False,
                'perm_admin': False,
                'perm_audit': False,
                'perm_auth': False,
                'perm_site_admin': False,
                'perm_regexp_access': False,
                'perm_tagger': True,
                'perm_template': False,
                'perm_sharing_group': False,
                'perm_tag_editor': False,
                'perm_sighting': True,
                'perm_object_template': False,
                'default_role': False,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': False,
                'perm_publish_kafka': False,
                'perm_decaying': False
            },
            {
                'id': 5,
                'name': 'Sync user',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': False,
                'perm_modify': False,
                'perm_modify_org': False,
                'perm_publish': False,
                'perm_delegate': False,
                'perm_sync': True,
                'perm_admin': False,
                'perm_audit': False,
                'perm_auth': True,
                'perm_site_admin': False,
                'perm_regexp_access': False,
                'perm_tagger': False,
                'perm_template': False,
                'perm_sharing_group': False,
                'perm_tag_editor': False,
                'perm_sighting': True,
                'perm_object_template': False,
                'default_role': False,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': False,
                'perm_publish_kafka': False,
                'perm_decaying': False
            },
            {
                'id': 6,
                'name': 'Read Only',
                'created': datetime.utcnow(),
                'modified': datetime.utcnow(),
                'perm_add': False,
                'perm_modify': False,
                'perm_modify_org': False,
                'perm_publish': False,
                'perm_delegate': False,
                'perm_sync': False,
                'perm_admin': False,
                'perm_audit': False,
                'perm_auth': False,
                'perm_site_admin': False,
                'perm_regexp_access': False,
                'perm_tagger': False,
                'perm_template': False,
                'perm_sharing_group': False,
                'perm_tag_editor': False,
                'perm_sighting': True,
                'perm_object_template': False,
                'default_role': False,
                'memory_limit': '',
                'max_execution_time': '',
                'restricted_to_site_admin': False,
                'perm_publish_zmq': False,
                'perm_publish_kafka': False,
                'perm_decaying': False
            }
        ]

        count = 0
        for role_data in roles_data:
            existing = self.session.query(Role).filter_by(
                id=role_data['id']
            ).first()

            if not existing:
                role = Role(**role_data)
                self.session.add(role)
                count += 1

        return count

    def seed_admin_settings(self) -> int:
        """Seed default admin settings"""
        from apps.security_service.src.data.models.misp import AdminSetting

        admin_settings_data = [
            ('MISP.baseurl', 'https://localhost'),
            ('MISP.live', 'true'),
            ('MISP.language', 'eng'),
            ('MISP.default_event_distribution', '0'),
            ('MISP.default_attribute_distribution', '5'),
            ('MISP.tagging', 'true'),
            ('MISP.full_tags_on_event_index', '2'),
            ('MISP.redis_host', '127.0.0.1'),
            ('MISP.redis_port', '6379'),
            ('MISP.redis_password', ''),
            ('MISP.redis_database', '13'),
            ('MISP.redis_namespace', 'misp'),
            ('MISP.log_client_ip', 'true'),
            ('MISP.log_auth', 'false'),
            ('MISP.disable_emailing', 'false'),
            ('MISP.contact', 'admin@admin.test'),
            ('MISP.email', 'admin@admin.test'),
            ('MISP.disable_cached_exports', 'false'),
            ('MISP.header', 'MISP'),
            ('MISP.footermidleft', 'This is an initial install'),
            ('MISP.footermidright', 'Please configure and harden accordingly'),
            ('MISP.welcome_text_top', 'Initial Install, please configure'),
            ('MISP.welcome_text_bottom', 'Welcome to MISP'),
            ('MISP.attachments_dir', '/var/www/MISP/app/files'),
            ('MISP.download_attachments_on_load', 'true'),
            ('MISP.title_text', 'MISP'),
            ('MISP.terms_download', 'false'),
            ('MISP.showorgalternate', 'false'),
            ('MISP.event_view_filter_fields',
             'id, uuid, value, comment, type, category, Tag.name'),
            ('MISP.homepage', '{"mispinfo":{"enabled":"true","pos":"1"},"threat_summary":{"enabled":"true","pos":"2"},"trends":{"enabled":"true","cutoff":"365","pos":"3"},"discussion":{"enabled":"true","pos":"4"},"dashboard":{"enabled":"false","pos":"5"},"alert":{"enabled":"true","pos":"0"}}'),
            ('MISP.threatlevel_in_email_subject', 'true'),
            ('MISP.email_subject_TLP_string', 'TLP:'),
            ('MISP.email_subject_tag', 'false'),
            ('MISP.email_subject_include_tag_name', 'true'),
            ('MISP.log_skip_db_logs_completely', 'false'),
            ('MISP.log_paranoid', 'false'),
            ('MISP.log_paranoid_skip_db', 'false'),
            ('MISP.tmpdir', '/tmp'),
            ('MISP.custom_css', ''),
            ('MISP.max_correlation_value_length', '256'),
            ('MISP.enable_advanced_correlations', 'false'),
            ('MISP.server_settings_skip_backup_rotate', 'false'),
            ('MISP.disable_network_logs', 'false'),
            ('MISP.enable_restlog', 'false'),
            ('MISP.rest_client_baseurl', ''),
            ('MISP.rest_client_timeout', '300'),
            ('MISP.rest_client_enable_arbitrary_urls', 'false'),
            ('MISP.auth_enforced', 'false'),
            ('MISP.auth_method', 'password'),
            ('MISP.auth_method_override', ''),
            ('MISP.enable_event_blocklisting', 'false'),
            ('MISP.enable_org_blocklisting', 'false'),
            ('MISP.log_new_audit', 'false'),
            ('MISP.proposal_block_attributes', 'false'),
            ('MISP.correlation_cache_timeout', '600'),
            ('MISP.disable_auto_logout', 'false'),
            ('MISP.ssdeep_correlation_threshold', '40'),
            ('MISP.extended_alert_subject', 'false'),
            ('MISP.default_attribute_memory_coefficient', '80'),
            ('MISP.python_bin', '/usr/bin/python3'),
            ('MISP.disable_correlation', 'false'),
            ('MISP.disable_correlation_for_objects', 'false'),
            ('MISP.max_attempts', '3'),
            ('MISP.block_event_alert', 'false'),
            ('MISP.block_event_alert_tag', 'no-alerts="true"'),
            ('MISP.block_old_event_alert', 'false'),
            ('MISP.block_old_event_alert_age', ''),
            ('MISP.block_old_event_alert_by_date', ''),
            ('MISP.incoming_tags_disabled_by_default', 'false'),
            ('MISP.maintenance_message', ''),
            ('MISP.disable_cached_exports', 'false'),
            ('MISP.disable_threat_level', 'false'),
            ('MISP.custom_auth_header', 'AUTHORIZATION'),
            ('MISP.disable_browser_cache', 'false'),
            ('MISP.check_sec_fetch_site_header', 'true'),
            ('MISP.auth_enforced', 'false'),
            ('db_version', '11')
        ]

        count = 0
        for setting, value in admin_settings_data:
            existing = self.session.query(AdminSetting).filter_by(
                setting=setting
            ).first()

            if not existing:
                admin_setting = AdminSetting(setting=setting, value=value)
                self.session.add(admin_setting)
                count += 1

        return count

    def seed_default_taxonomies(self) -> int:
        """Seed default taxonomies"""
        from apps.security_service.src.data.models.misp import (
            Taxonomy, TaxonomyEntry, TaxonomyPredicate)

        # Core MISP taxonomies
        taxonomies_data = [
            {
                'namespace': 'tlp',
                'description': 'The Traffic Light Protocol (TLP) classification',
                'version': '4',
                'enabled': True,
                'predicates': [
                    {
                        'value': 'white',
                        'description': 'Information can be shared publicly',
                        'entries': [
                            {'value': 'TLP:WHITE', 'description': 'Sources may use TLP:WHITE when information carries minimal or no foreseeable risk of misuse'}
                        ]
                    },
                    {
                        'value': 'green',
                        'description': 'Information can be shared within a community',
                        'entries': [
                            {'value': 'TLP:GREEN', 'description': 'Sources may use TLP:GREEN when information is useful for the awareness of all participating organizations'}
                        ]
                    },
                    {
                        'value': 'amber',
                        'description': 'Limited disclosure, restricted to participants organizations',
                        'entries': [
                            {'value': 'TLP:AMBER', 'description': 'Sources may use TLP:AMBER when information requires support to be effectively acted upon'},
                            {'value': 'TLP:AMBER+STRICT',
                                'description': 'TLP:AMBER information with limited disclosure restriction'}
                        ]
                    },
                    {
                        'value': 'red',
                        'description': 'Not for disclosure, restricted to participants only',
                        'entries': [
                            {'value': 'TLP:RED', 'description': 'Sources may use TLP:RED when information cannot be effectively acted upon by additional parties'}
                        ]
                    }
                ]
            },
            {
                'namespace': 'admiralty-scale',
                'description': 'The Admiralty Scale (also called the NATO System) is used to rank the reliability of a source and the credibility of an information',
                'version': '1',
                'enabled': True,
                'predicates': [
                    {
                        'value': 'source-reliability',
                        'description': 'Source Reliability',
                        'entries': [
                            {'value': 'a', 'description': 'Completely reliable'},
                            {'value': 'b', 'description': 'Usually reliable'},
                            {'value': 'c', 'description': 'Fairly reliable'},
                            {'value': 'd', 'description': 'Not usually reliable'},
                            {'value': 'e', 'description': 'Unreliable'},
                            {'value': 'f', 'description': 'Reliability cannot be judged'}
                        ]
                    },
                    {
                        'value': 'information-credibility',
                        'description': 'Information Credibility',
                        'entries': [
                            {'value': '1', 'description': 'Confirmed by other sources'},
                            {'value': '2', 'description': 'Probably true'},
                            {'value': '3', 'description': 'Possibly true'},
                            {'value': '4', 'description': 'Doubtful'},
                            {'value': '5', 'description': 'Improbable'},
                            {'value': '6', 'description': 'Truth cannot be judged'}
                        ]
                    }
                ]
            },
            {
                'namespace': 'PAP',
                'description': 'The Permissible Actions Protocol - or short: PAP - was designed to indicate how the received information can be used',
                'version': '2',
                'enabled': True,
                'predicates': [
                    {
                        'value': 'WHITE',
                        'description': 'No restrictions in using this information',
                        'entries': [
                            {'value': 'PAP:WHITE',
                                'description': 'No restrictions apply, information can be used for any purpose'}
                        ]
                    },
                    {
                        'value': 'GREEN',
                        'description': 'Usable for security countermeasures',
                        'entries': [
                            {'value': 'PAP:GREEN',
                                'description': 'Information can be used for automatic countermeasures'}
                        ]
                    },
                    {
                        'value': 'AMBER',
                        'description': 'Usable for manual countermeasures',
                        'entries': [
                            {'value': 'PAP:AMBER', 'description': 'Information can be used for manual countermeasures after human validation'}
                        ]
                    },
                    {
                        'value': 'RED',
                        'description': 'Not usable for countermeasures',
                        'entries': [
                            {'value': 'PAP:RED',
                                'description': 'Information cannot be used for countermeasures'}
                        ]
                    }
                ]
            }
        ]

        count = 0
        for tax_data in taxonomies_data:
            existing = self.session.query(Taxonomy).filter_by(
                namespace=tax_data['namespace']
            ).first()

            if not existing:
                taxonomy = Taxonomy(
                    namespace=tax_data['namespace'],
                    description=tax_data['description'],
                    version=tax_data['version'],
                    enabled=tax_data['enabled']
                )
                self.session.add(taxonomy)
                self.session.flush()  # Get taxonomy ID

                # Add predicates
                for pred_data in tax_data['predicates']:
                    predicate = TaxonomyPredicate(
                        taxonomy_id=taxonomy.id,
                        value=pred_data['value'],
                        description=pred_data['description']
                    )
                    self.session.add(predicate)
                    self.session.flush()  # Get predicate ID

                    # Add entries
                    for entry_data in pred_data['entries']:
                        entry = TaxonomyEntry(
                            taxonomy_predicate_id=predicate.id,
                            value=entry_data['value'],
                            description=entry_data['description']
                        )
                        self.session.add(entry)

                count += 1

        return count

    def seed_default_galaxies(self) -> int:
        """Seed default galaxy clusters"""
        from apps.security_service.src.data.models.misp import (Galaxy,
                                                                GalaxyCluster)

        galaxies_data = [
            {
                'uuid': '698774c7-8022-42c4-917f-8d6e4f06ada3',
                'name': 'Threat Actor',
                'type': 'threat-actor',
                'description': 'Threat actors are characteristics of malicious actors (or adversaries) representing a cyber attack threat',
                'version': '8',
                'namespace': 'misp',
                'enabled': True,
                'clusters': [
                    {
                        'uuid': '7cdff317-a673-4474-84ec-4f1754947823',
                        'type': 'threat-actor',
                        'value': 'APT1',
                        'tag_name': 'misp-galaxy:threat-actor="APT1"',
                        'description': 'APT1 is a Chinese threat group that has been attributed to the 2nd Bureau of the People\'s Liberation Army (PLA) General Staff Department\'s (GSD) 3rd Department',
                        'source': 'https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/mandiant-apt1-report.pdf'
                    },
                    {
                        'uuid': 'f047ee18-7985-4946-8bfb-4ed754d3a0dd',
                        'type': 'threat-actor',
                        'value': 'Lazarus Group',
                        'tag_name': 'misp-galaxy:threat-actor="Lazarus Group"',
                        'description': 'Lazarus Group is a threat group that has been attributed to the North Korean government',
                        'source': 'https://www.operationblockbuster.com/wp-content/uploads/2016/02/Operation-Blockbuster-Report.pdf'
                    }
                ]
            },
            {
                'uuid': 'd752161c-78f6-11e7-a0ea-bfa79b407ce4',
                'name': 'Malware',
                'type': 'malware',
                'description': 'Malware galaxy based on MISP events',
                'version': '4',
                'namespace': 'misp',
                'enabled': True,
                'clusters': [
                    {
                        'uuid': 'b8eb28e4-48a6-40ae-951a-328714f75eda',
                        'type': 'malware',
                        'value': 'Zeus',
                        'tag_name': 'misp-galaxy:malware="Zeus"',
                        'description': 'Zeus is a Trojan horse malware package that runs on versions of Microsoft Windows',
                        'source': 'https://en.wikipedia.org/wiki/Zeus_(malware)'
                    },
                    {
                        'uuid': '54a649ff-439a-41a4-9856-8d144a9bd068',
                        'type': 'malware',
                        'value': 'Stuxnet',
                        'tag_name': 'misp-galaxy:malware="Stuxnet"',
                        'description': 'Stuxnet is a malicious computer worm believed to be a jointly built American-Israeli cyberweapon',
                        'source': 'https://en.wikipedia.org/wiki/Stuxnet'
                    }
                ]
            }
        ]

        count = 0
        for galaxy_data in galaxies_data:
            existing = self.session.query(Galaxy).filter_by(
                uuid=galaxy_data['uuid']
            ).first()

            if not existing:
                galaxy = Galaxy(
                    uuid=galaxy_data['uuid'],
                    name=galaxy_data['name'],
                    type=galaxy_data['type'],
                    description=galaxy_data['description'],
                    version=galaxy_data['version'],
                    namespace=galaxy_data['namespace'],
                    enabled=galaxy_data['enabled']
                )
                self.session.add(galaxy)
                self.session.flush()  # Get galaxy ID

                # Add clusters
                for cluster_data in galaxy_data['clusters']:
                    cluster = GalaxyCluster(
                        uuid=cluster_data['uuid'],
                        galaxy_id=galaxy.id,
                        type=cluster_data['type'],
                        value=cluster_data['value'],
                        tag_name=cluster_data['tag_name'],
                        description=cluster_data['description'],
                        source=cluster_data['source']
                    )
                    self.session.add(cluster)

                count += 1

        return count

    def seed_default_warninglists(self) -> int:
        """Seed default warning lists"""
        from apps.security_service.src.data.models.misp import (
            Warninglist, WarninglistEntry)

        warninglists_data = [
            {
                'name': 'List of known public DNS resolvers',
                'type': 'hostname',
                'description': 'Event contains one or more entries of known public DNS resolvers',
                'version': '1',
                'enabled': True,
                'entries': [
                    '8.8.8.8', '8.8.4.4',  # Google
                    '1.1.1.1', '1.0.0.1',  # Cloudflare
                    '208.67.222.222', '208.67.220.220',  # OpenDNS
                    '9.9.9.9', '149.112.112.112',  # Quad9
                ]
            },
            {
                'name': 'List of known IPv4 public IP addresses used by multicast',
                'type': 'cidr',
                'description': 'Event contains one or more entries part of the IPv4 multicast address space',
                'version': '1',
                'enabled': True,
                'entries': [
                    '224.0.0.0/4'  # IPv4 multicast
                ]
            },
            {
                'name': 'List of RFC 1918 CIDR blocks',
                'type': 'cidr',
                'description': 'Event contains one or more entries part of the RFC 1918 private address space',
                'version': '1',
                'enabled': True,
                'entries': [
                    '10.0.0.0/8',
                    '172.16.0.0/12',
                    '192.168.0.0/16'
                ]
            }
        ]

        count = 0
        for wl_data in warninglists_data:
            existing = self.session.query(Warninglist).filter_by(
                name=wl_data['name']
            ).first()

            if not existing:
                warninglist = Warninglist(
                    name=wl_data['name'],
                    type=wl_data['type'],
                    description=wl_data['description'],
                    version=wl_data['version'],
                    enabled=wl_data['enabled']
                )
                self.session.add(warninglist)
                self.session.flush()  # Get warninglist ID

                # Add entries
                for entry_value in wl_data['entries']:
                    entry = WarninglistEntry(
                        warninglist_id=warninglist.id,
                        value=entry_value
                    )
                    self.session.add(entry)

                count += 1

        return count

    def seed_notice_lists(self) -> int:
        """Seed default notice lists"""
        # Notice lists would be implemented similarly to warning lists
        # For now, return 0 as this is less critical
        return 0

    def verify_seeded_data(self) -> Dict[str, Any]:
        """Verify that all initial data was seeded correctly"""
        from apps.security_service.src.data.models.misp import (AdminSetting,
                                                                Galaxy, Role,
                                                                Taxonomy,
                                                                ThreatLevel,
                                                                Warninglist)

        verification = {
            'threat_levels': self.session.query(ThreatLevel).count(),
            'roles': self.session.query(Role).count(),
            'admin_settings': self.session.query(AdminSetting).count(),
            'taxonomies': self.session.query(Taxonomy).count(),
            'galaxies': self.session.query(Galaxy).count(),
            'warninglists': self.session.query(Warninglist).count(),
            'status': 'success'
        }

        # Verify critical data exists
        required_threat_levels = 4
        required_roles = 6
        min_admin_settings = 10

        if verification['threat_levels'] < required_threat_levels:
            verification['status'] = 'warning'
            verification['issues'] = verification.get('issues', [])
            verification['issues'].append(
                f"Expected {required_threat_levels} threat levels, found {verification['threat_levels']}")

        if verification['roles'] < required_roles:
            verification['status'] = 'warning'
            verification['issues'] = verification.get('issues', [])
            verification['issues'].append(
                f"Expected {required_roles} roles, found {verification['roles']}")

        if verification['admin_settings'] < min_admin_settings:
            verification['status'] = 'warning'
            verification['issues'] = verification.get('issues', [])
            verification['issues'].append(
                f"Expected at least {min_admin_settings} admin settings, found {verification['admin_settings']}")

        return verification


def run_misp_data_seeding(database_url: str) -> Dict[str, Any]:
    """Run MISP data seeding from database URL"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        seeder = MispDataSeeder(session)
        results = seeder.seed_all_initial_data()
        verification = seeder.verify_seeded_data()

        return {
            'seeding_results': results,
            'verification': verification
        }
