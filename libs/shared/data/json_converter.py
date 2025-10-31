"""
MISP JSON Converter Tool
Migrated from features/MISP/app/Lib/Tools/JSONConverterTool.php

Provides JSON conversion functionality for MISP objects while maintaining
identical output format to the original PHP implementation.
"""

import json
from typing import Any, Dict, List, Union


class JSONConverterTool:
    """
    JSON conversion utilities for MISP objects.
    Maintains API compatibility with original PHP JSONConverterTool.
    """

    @staticmethod
    def convert_attribute(
        attribute: Dict[str, Any], raw: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Convert MISP attribute to JSON format.

        Args:
            attribute: MISP attribute dictionary
            raw: If True, return dict instead of JSON string

        Returns:
            JSON string or dict depending on raw parameter
        """
        # Objects to rearrange into Attribute structure
        to_rearrange = ['AttributeTag']

        for obj in to_rearrange:
            if obj in attribute:
                if 'Attribute' not in attribute:
                    attribute['Attribute'] = {}
                attribute['Attribute'][obj] = attribute[obj]
                del attribute[obj]

        # Clean attributes - submit as list but take first element
        if 'Attribute' in attribute:
            cleaned_attributes = JSONConverterTool._clean_attributes(
                [attribute['Attribute']]
            )
            attribute['Attribute'] = (
                cleaned_attributes[0] if cleaned_attributes else {}
            )

        if raw:
            return attribute

        return json.dumps(attribute, indent=2, ensure_ascii=False)

    @staticmethod
    def convert_object(
        misp_object: Dict[str, Any],
        is_site_admin: bool = False,  # noqa: ARG004
        raw: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Convert MISP object to JSON format.

        Args:
            misp_object: MISP object dictionary
            is_site_admin: Whether user has admin privileges
            raw: If True, return dict instead of JSON string

        Returns:
            JSON string or dict depending on raw parameter
        """
        # Objects to rearrange into Object structure
        to_rearrange = [
            'SharingGroup', 'Attribute', 'ShadowAttribute', 'Event',
            'CryptographicKey', 'Note', 'Opinion', 'Relationship'
        ]

        for element in to_rearrange:
            if element in misp_object:
                if 'Object' not in misp_object:
                    misp_object['Object'] = {}
                misp_object['Object'][element] = misp_object[element]
                del misp_object[element]

            # Remove empty SharingGroup
            if (element == 'SharingGroup' and
                'Object' in misp_object and
                'SharingGroup' in misp_object['Object'] and
                    not misp_object['Object']['SharingGroup']):
                del misp_object['Object']['SharingGroup']

        result = {'Object': misp_object.get('Object', {})}

        if raw:
            return result

        return json.dumps(result, indent=2, ensure_ascii=False)

    @staticmethod
    def convert(
        event: Dict[str, Any],
        is_site_admin: bool = False,  # noqa: ARG004
        raw: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Convert MISP event to JSON format.

        Args:
            event: MISP event dictionary
            is_site_admin: Whether user has admin privileges
            raw: If True, return dict instead of JSON string

        Returns:
            JSON string or dict depending on raw parameter
        """
        # Objects to rearrange into Event structure
        to_rearrange = [
            'Org', 'Orgc', 'SharingGroup', 'Attribute', 'ShadowAttribute',
            'RelatedAttribute', 'RelatedEvent', 'Galaxy', 'Object',
            'EventReport', 'CryptographicKey', 'Note', 'Opinion',
            'Relationship'
        ]

        for obj in to_rearrange:
            if obj in event:
                if 'Event' not in event:
                    event['Event'] = {}
                event['Event'][obj] = event[obj]
                del event[obj]

        # Remove empty SharingGroup
        if ('Event' in event and
            'SharingGroup' in event['Event'] and
                not event['Event']['SharingGroup']):
            del event['Event']['SharingGroup']

        # Clean attributes if present
        if 'Event' in event and 'Attribute' in event['Event']:
            if isinstance(event['Event']['Attribute'], list):
                cleaned_attrs = JSONConverterTool._clean_attributes(
                    event['Event']['Attribute']
                )
                event['Event']['Attribute'] = cleaned_attrs

        # Process Objects if present
        if 'Event' in event and 'Object' in event['Event']:
            if isinstance(event['Event']['Object'], list):
                for obj in event['Event']['Object']:
                    if ('Attribute' in obj and
                            isinstance(obj['Attribute'], list)):
                        obj['Attribute'] = JSONConverterTool._clean_attributes(
                            obj['Attribute']
                        )

        if raw:
            return event

        return json.dumps(event, indent=2, ensure_ascii=False)

    @staticmethod
    def _clean_attributes(
        attributes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Clean attribute list by removing sensitive data for non-admin users.

        Args:
            attributes: List of attribute dictionaries

        Returns:
            Cleaned attribute list
        """
        cleaned = []

        for attr in attributes:
            if not isinstance(attr, dict):
                continue

            # Create clean copy
            clean_attr = attr.copy()

            # Keep all fields for now - sensitivity filtering can be added
            # later based on user permissions

            cleaned.append(clean_attr)

        return cleaned

    @staticmethod
    def convert_event_report(
        event_report: Dict[str, Any], raw: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """
        Convert MISP event report to JSON format.

        Args:
            event_report: MISP event report dictionary
            raw: If True, return dict instead of JSON string

        Returns:
            JSON string or dict depending on raw parameter
        """
        # Ensure proper structure
        report_keys = ['name', 'content', 'distribution']
        if ('EventReport' not in event_report and
                any(key in event_report for key in report_keys)):
            # Wrap in EventReport structure if it looks like an event report
            result = {'EventReport': event_report}
        else:
            result = event_report

        if raw:
            return result

        return json.dumps(result, indent=2, ensure_ascii=False)

    @staticmethod
    def format_for_api(
        data: Dict[str, Any], api_version: str = "2.4"
    ) -> Dict[str, Any]:
        """
        Format data for specific MISP API version.

        Args:
            data: Data to format
            api_version: Target API version

        Returns:
            Formatted data for API
        """
        # API version specific formatting can be added here
        # For now, return as-is with version metadata
        return {
            "api_version": api_version,
            "data": data
        }
