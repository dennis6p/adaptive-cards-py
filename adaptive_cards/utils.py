"""
Utility functions for library
"""

from typing import Any
from dataclasses_json import config

is_none: Any = lambda f: f is None


def get_metadata(min_version: str) -> dict[str, Any]:
    """
    Get default metadata information for dataclass field

    Args:
        min_version (str): Minimum version number of the field the result will
                           be appliead to.

    Returns:
        dict[str, Any]: Metadata information
    """
    return config(exclude=is_none) | {"min_version": min_version}
