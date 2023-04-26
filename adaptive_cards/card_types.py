from dataclasses import dataclass, field
from typing import Optional
from dataclasses_json import config, dataclass_json, LetterCase
from enum import auto
from strenum import LowercaseStrEnum
import adaptive_cards.utils as utils

class ImageFillMode(LowercaseStrEnum):
    COVER = auto()
    REPEAT_HORIZONTALLY = "repeatHorizontally"
    REPEAT_VERTICALLY = "repeatVertically" 
    REPEAT = auto()
      
class HorizontalAlignment(LowercaseStrEnum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()   

class VerticalAlignment(LowercaseStrEnum):
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()  

class Colors(LowercaseStrEnum):
    DEFAULT = auto()
    DARK = auto()
    LIGHT = auto()
    ACCENT = auto()
    GOOD = auto()
    WARNING = auto()
    ATTENTION = auto()
    
class FontType(LowercaseStrEnum):
    DEFAULT = auto()
    MONOSPACE = auto()
    
class FontSize(LowercaseStrEnum):
    DEFAULT = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    EXTRA_LARGE = "extraLarge"

class FontWeight(LowercaseStrEnum):
    DEFAULT = auto()
    LIGHTER = auto()
    BOLDER = auto()
    
class TextBlockStyle(LowercaseStrEnum):
    DEFAULT = auto()
    HEADING = auto()
    
class BlockElementHeight(LowercaseStrEnum):
    AUTO = auto()
    STRETCH = auto()

class ImageSize(LowercaseStrEnum):
    AUTO = auto()
    STRETCH = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    
class ImageStyle(LowercaseStrEnum):
    DEFAULT = auto()
    PERSON = auto()

class ContainerStyle(LowercaseStrEnum):
    DEFAULT = auto()
    EMPHASIS = auto()
    GOOD = auto()
    ATTENTION = auto()
    WARNING = auto()
    ACCENT = auto()

class Spacing(LowercaseStrEnum):
    DEFAULT = auto()
    NONE = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    EXTRA_LARGE = "extraLarge"
    PADDING = auto()
    
class AssociatedInputs(LowercaseStrEnum):
    AUTO = auto()
    NONE = auto()
    
class ActionStyle(LowercaseStrEnum):
    DEFAULT = auto()
    POSITIVE = auto()
    DESTRUCTIVE = auto()
    
class ActionMode(LowercaseStrEnum):
    PRIMARY = auto()
    SECONDARY = auto()
    
class TextInputStyle(LowercaseStrEnum):
    TEXT = auto()
    TEL = auto()
    URL = auto()
    EMAIL = auto()
    PASSWORD = auto()
    
class ChoiceInputStyle(LowercaseStrEnum):
    COMPACT = auto()
    EXPANDED = auto()
    FILTERED = auto()
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class BackgroundImage:
    uri: str = field(metadata=utils.get_metadata("1.0"))
    fill_mode: Optional[ImageFillMode] = field(default=None, metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.2"))
    vertical_alignment: Optional[VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Refresh:
    action: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    expires: Optional[str] = field(default=None, metadata=utils.get_metadata("1.6"))
    user_ids: Optional[list[str]] = field(default=None, metadata=utils.get_metadata("1.4"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TokenExchangeResource:
    id: str = field(default="", metadata=utils.get_metadata("1.4"))
    uri: str = field(default="", metadata=utils.get_metadata("1.4"))
    provider_id: str = field(default="", metadata=utils.get_metadata("1.4"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class AuthCardButtons:
    type: str = field(default="", metadata=utils.get_metadata("1.4"))
    value: str = field(default="", metadata=utils.get_metadata("1.4"))
    title: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    image: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Authentication:
    text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    connection_name: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    token_exchange_resource: Optional[TokenExchangeResource] = field(default=None, metadata=utils.get_metadata("1.4"))
    buttons: Optional[AuthCardButtons] = field(default=None, metadata=utils.get_metadata("1.4"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Metadata:
    web_url: Optional[str] = field(default=None, metadata=utils.get_metadata("1.6"))