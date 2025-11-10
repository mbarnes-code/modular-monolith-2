"""
MISP Feed Parser Module

Feed parsing utilities preserving original MISP feed parsing functionality
from Feed.php with support for MISP JSON, freetext, and CSV formats.
"""

import csv
import json
import logging
import re
from datetime import datetime
from io import StringIO
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class FeedParser:
    """
    Feed parser preserving original MISP feed parsing behavior.

    Supports multiple feed formats with validation and error handling.
    """

    # IOC type patterns for freetext parsing
    IOC_PATTERNS = {
        'ip-src': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'ip-dst': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'domain': r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'url': r'https?://[^\s<>"\']+',
        'md5': r'\b[a-fA-F0-9]{32}\b',
        'sha1': r'\b[a-fA-F0-9]{40}\b',
        'sha256': r'\b[a-fA-F0-9]{64}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    }

    @staticmethod
    async def parse_misp_feed(data: str) -> Optional[List[Dict]]:
        """
        Parse MISP JSON feed format.

        Preserves original MISP feed parsing from Feed.php parseMispFeed().
        """
        try:
            # Parse JSON data
            if data.strip().startswith('['):
                # Array of events
                events = json.loads(data)
            else:
                # Single event
                event = json.loads(data)
                events = [event] if isinstance(event, dict) else []

            parsed_events = []

            for event_data in events:
                if not isinstance(event_data, dict):
                    continue

                # Validate MISP event structure
                if 'Event' in event_data:
                    event = event_data['Event']
                elif 'uuid' in event_data and 'info' in event_data:
                    event = event_data
                else:
                    logger.warning("Invalid MISP event structure, skipping")
                    continue

                # Basic validation
                if not all(key in event for key in ['uuid', 'info']):
                    logger.warning(
                        f"Missing required fields in event: {event}")
                    continue

                # Validate and normalize event
                normalized_event = await FeedParser._normalize_misp_event(event)
                if normalized_event:
                    parsed_events.append(normalized_event)

            logger.info(f"Parsed {len(parsed_events)} MISP events from feed")
            return parsed_events

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MISP feed JSON: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing MISP feed: {str(e)}")
            return None

    @staticmethod
    async def parse_freetext_feed(data: str, rules: Dict[str, Any]) -> Optional[List[Dict]]:
        """
        Parse freetext feed using IOC extraction patterns.

        Preserves original MISP freetext parsing from Feed.php parseFreetextFeed().
        """
        try:
            extracted_iocs = []
            lines = data.strip().split('\n')

            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Extract IOCs from line using patterns
                for ioc_type, pattern in FeedParser.IOC_PATTERNS.items():
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        ioc_value = match.group(0)

                        # Apply filtering rules if configured
                        if rules and not FeedParser._apply_freetext_rules(
                            ioc_type, ioc_value, rules
                        ):
                            continue

                        # Create attribute structure
                        attribute = {
                            'type': ioc_type,
                            'value': ioc_value,
                            'to_ids': True,
                            'distribution': 5,  # Inherit event
                            'comment': f'Extracted from line {line_num}',
                            'uuid': FeedParser._generate_uuid()
                        }

                        extracted_iocs.append(attribute)

            if not extracted_iocs:
                logger.warning("No IOCs extracted from freetext feed")
                return None

            # Create single event with all extracted IOCs
            event = {
                'uuid': FeedParser._generate_uuid(),
                'info': f'Freetext feed import - {datetime.utcnow().isoformat()}',
                'analysis': 1,  # Ongoing
                'threat_level_id': 4,  # Undefined
                'published': False,
                'distribution': 1,  # This community only
                'Attribute': extracted_iocs
            }

            logger.info(
                f"Extracted {len(extracted_iocs)} IOCs from freetext feed")
            return [event]

        except Exception as e:
            logger.error(f"Error parsing freetext feed: {str(e)}")
            return None

    @staticmethod
    async def parse_csv_feed(data: str, rules: Dict[str, Any]) -> Optional[List[Dict]]:
        """
        Parse CSV feed format with configurable column mapping.

        Preserves original MISP CSV parsing from Feed.php parseCSVFeed().
        """
        try:
            csv_reader = csv.DictReader(StringIO(data))

            # Get column mapping from rules
            column_mapping = rules.get('column_mapping', {})
            if not column_mapping:
                logger.error("CSV feed requires column_mapping in rules")
                return None

            extracted_data = []

            for row_num, row in enumerate(csv_reader, 1):
                try:
                    # Map CSV columns to MISP attributes
                    attributes = []

                    for csv_column, misp_field in column_mapping.items():
                        if csv_column not in row:
                            continue

                        value = row[csv_column].strip()
                        if not value:
                            continue

                        # Parse MISP field specification (type|category)
                        if '|' in misp_field:
                            attr_type, category = misp_field.split('|', 1)
                        else:
                            attr_type = misp_field
                            category = 'Network activity'  # Default category

                        # Create attribute
                        attribute = {
                            'type': attr_type,
                            'category': category,
                            'value': value,
                            'to_ids': True,
                            'distribution': 5,  # Inherit event
                            'comment': f'CSV import row {row_num}',
                            'uuid': FeedParser._generate_uuid()
                        }

                        attributes.append(attribute)

                    if attributes:
                        # Create event for this row
                        event = {
                            'uuid': FeedParser._generate_uuid(),
                            'info': f'CSV feed import row {row_num}',
                            'analysis': 1,  # Ongoing
                            'threat_level_id': 4,  # Undefined
                            'published': False,
                            'distribution': 1,  # This community only
                            'Attribute': attributes
                        }

                        extracted_data.append(event)

                except Exception as e:
                    logger.warning(
                        f"Error processing CSV row {row_num}: {str(e)}")
                    continue

            logger.info(f"Parsed {len(extracted_data)} events from CSV feed")
            return extracted_data if extracted_data else None

        except Exception as e:
            logger.error(f"Error parsing CSV feed: {str(e)}")
            return None

    @staticmethod
    async def _normalize_misp_event(event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize MISP event structure and validate required fields."""
        try:
            normalized = {
                'uuid': event['uuid'],
                'info': event['info'],
                'analysis': event.get('analysis', 1),
                'threat_level_id': event.get('threat_level_id', 4),
                'published': event.get('published', False),
                'distribution': event.get('distribution', 1)
            }

            # Handle attributes
            if 'Attribute' in event:
                normalized['Attribute'] = event['Attribute']
            elif 'attributes' in event:
                normalized['Attribute'] = event['attributes']
            else:
                normalized['Attribute'] = []

            # Handle objects
            if 'Object' in event:
                normalized['Object'] = event['Object']
            elif 'objects' in event:
                normalized['Object'] = event['objects']

            # Handle tags
            if 'Tag' in event:
                normalized['Tag'] = event['Tag']
            elif 'tags' in event:
                normalized['Tag'] = event['tags']

            return normalized

        except Exception as e:
            logger.error(f"Error normalizing MISP event: {str(e)}")
            return None

    @staticmethod
    def _apply_freetext_rules(
        ioc_type: str,
        ioc_value: str,
        rules: Dict[str, Any]
    ) -> bool:
        """Apply filtering rules to extracted IOCs."""
        try:
            # Whitelist check
            if 'whitelist' in rules:
                whitelist = rules['whitelist']
                if isinstance(whitelist, list):
                    if ioc_value.lower() in [item.lower() for item in whitelist]:
                        return False
                elif isinstance(whitelist, dict):
                    type_whitelist = whitelist.get(ioc_type, [])
                    if ioc_value.lower() in [item.lower() for item in type_whitelist]:
                        return False

            # Blacklist check
            if 'blacklist' in rules:
                blacklist = rules['blacklist']
                if isinstance(blacklist, list):
                    if ioc_value.lower() in [item.lower() for item in blacklist]:
                        return False
                elif isinstance(blacklist, dict):
                    type_blacklist = blacklist.get(ioc_type, [])
                    if ioc_value.lower() in [item.lower() for item in type_blacklist]:
                        return False

            # Type filter check
            if 'types' in rules:
                allowed_types = rules['types']
                if isinstance(allowed_types, list) and ioc_type not in allowed_types:
                    return False

            return True

        except Exception as e:
            logger.warning(f"Error applying freetext rules: {str(e)}")
            return True  # Default to allowing the IOC

    @staticmethod
    def _generate_uuid() -> str:
        """Generate UUID for MISP objects."""
        import uuid
        return str(uuid.uuid4())
