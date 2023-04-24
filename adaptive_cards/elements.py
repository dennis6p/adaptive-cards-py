from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config
from typing import TypeVar, Optional, Any

import adaptive_cards.actions as actions
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct

Image = TypeVar("Image", bound="Image")
TextBlock = TypeVar("TextBlock", bound="TextBlock")
Media = TypeVar("Media", bound="Media")
MediaSource = TypeVar("MediaSource", bound="MediaSource")
CaptionSource = TypeVar("CaptionSource", bound="CaptionSource")
RichTextBlock = TypeVar("RichTextBlock", bound="RichTextBlock")
TextRun = TypeVar("TextRun", bound="TextRun")

ElementT = CaptionSource | Image | Media | RichTextBlock | TextBlock
           
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class CardElement:
    Element: Optional[Any | ElementT] = field(default=None, metadata=utils.get_metadata("1.2"))
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=utils.get_metadata("1.0"))
    id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    requires: Optional[dict[str, str]] = field(default=None, metadata=utils.get_metadata("1.2"))   
    height: Optional[ct.BlockElementHeight] = field(default=None, metadata=utils.get_metadata("1.1"))    
           
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class TextBlock(CardElement):
    text: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="TextBlock", metadata=utils.get_metadata("1.0"))
    color: Optional[ct.Colors] = field(default=None, metadata=utils.get_metadata("1.0"))
    font_type: Optional[ct.FontType] = field(default=None, metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.0"))
    is_subtle: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    max_lines: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    size: Optional[ct.FontSize] = field(default=None, metadata=utils.get_metadata("1.0"))
    weight: Optional[ct.FontWeight] = field(default=None, metadata=utils.get_metadata("1.0"))
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    style: Optional[ct.TextBlockStyle] = field(default=None, metadata=utils.get_metadata("1.5"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class Image(CardElement):
    url: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Image", metadata=utils.get_metadata("1.0"))
    alt_text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    background_color: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.0"))
    select_action: Optional[actions.SelectAction] = field(default=None, metadata=utils.get_metadata("1.1"))
    size: Optional[ct.ImageSize] = field(default=None, metadata=utils.get_metadata("1.0"))
    style: Optional[ct.ImageStyle] = field(default=None, metadata=utils.get_metadata("1.0"))
    width: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class Media(CardElement):
    type: str = field(default="Media", metadata=utils.get_metadata("1.1"))
    sources: list[MediaSource] = field(metadata=utils.get_metadata("1.1"))
    poster: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    alt_text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    caption_sources: Optional[list[CaptionSource]] = field(default=None, metadata=utils.get_metadata("1.6"))
 
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class MediaSource:
    url: str = field(metadata=utils.get_metadata("1.1"))
    mime_type: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class CaptionSource:
    mime_type: str = field(metadata=utils.get_metadata("1.6"))
    url: str = field(metadata=utils.get_metadata("1.6"))
    label: str = field(metadata=utils.get_metadata("1.6"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class RichTextBlock(CardElement):
    inlines: list[str | TextRun] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="RichTextBlock", metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class TextRun:
    text: str = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="TextRun", metadata=utils.get_metadata("1.2"))
    color: Optional[ct.Colors] = field(default=None, metadata=utils.get_metadata("1.2"))
    font_type: Optional[ct.FontType] = field(default=None, metadata=utils.get_metadata("1.2"))
    highlight: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    is_subtle: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    italic: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    select_action: Optional[actions.SelectAction] = field(default=None, metadata=utils.get_metadata("1.2"))
    size: Optional[ct.FontSize] = field(default=None, metadata=utils.get_metadata("1.2"))
    strikethrough: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    underline: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.3"))
    weight: Optional[ct.FontWeight] = field(default=None, metadata=utils.get_metadata("1.2"))