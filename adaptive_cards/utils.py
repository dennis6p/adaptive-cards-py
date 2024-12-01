"""
Utility functions for library
"""

from typing import Any

from dataclasses_json import config


def is_none(item: Any) -> bool:
    """
    Check whether a given item is initialized or None

    Args:
        item (Any): Item to be checked

    Returns:
        bool: true if item is None
    """
    return item is None


def get_metadata(min_version: str, field_name: str | None = None) -> dict[str, Any]:
    """
    Get default metadata information for dataclass field

    Args:
        min_version (str): Minimum version number of the field the result will
                           be appliead to.

    Returns:
        dict[str, Any]: Metadata information
    """
    return config(exclude=is_none, field_name=field_name) | {"min_version": min_version}
