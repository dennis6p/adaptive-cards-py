from typing import Any
from dataclasses_json import config

is_none: Any = lambda f: f is None

def get_metadata(min_version: str) -> dict[str, Any]:
    return config(exclude=is_none) | dict(min_version=min_version)