from typing import Any
from dataclasses_json import config
from dataclasses import field

is_none: Any = lambda f: f is None

# field(default=None, metadata=config(exclude=utils.is_none)): Any = 
# field(default="", metadata=config(exclude=utils.is_none)): Any = field(default="", metadata=config(exclude=utils.is_none))