from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config, Undefined
from typing import TypeVar, Self, Optional, Any
from interfaces.interface import Builder

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

ElementT = CaptionSource | \
           Image | \
           Media | \
           RichTextBlock | \
           TextBlock
           
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class CardElement:
    Element: Optional[Any] = field(default=None, metadata=config(exclude=utils.is_none))
    separator: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=config(exclude=utils.is_none))
    id: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    is_visible: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    requires: Optional[dict[str, str]] = field(default=None, metadata=config(exclude=utils.is_none))   
    height: Optional[ct.BlockElementHeight] = field(default=None, metadata=config(exclude=utils.is_none))    
           
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class TextBlock(CardElement):
    text: str
    type: str = "TextBlock"
    color: Optional[ct.Colors] = field(default=None, metadata=config(exclude=utils.is_none))
    font_type: Optional[ct.FontType] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    is_subtle: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    max_lines: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    size: Optional[ct.FontSize] = field(default=None, metadata=config(exclude=utils.is_none))
    weight: Optional[ct.FontWeight] = field(default=None, metadata=config(exclude=utils.is_none))
    wrap: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.TextBlockStyle] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class Image(CardElement):
    url: str
    type: str = "Image"
    alt_text: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    background_color: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[actions.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    size: Optional[ct.ImageSize] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ImageStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class Media(CardElement):
    type: str = "Media"
    sources: list[MediaSource]
    poster: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    alt_text: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    caption_sources: Optional[list[CaptionSource]] = field(default=None, metadata=config(exclude=utils.is_none))
 
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class MediaSource:
    url: str
    mime_type: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class CaptionSource:
    mime_type: str
    url: str
    label: str

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class RichTextBlock(CardElement):
    inlines: list[str | TextRun]
    type: str = "RichTextBlock"
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class TextRun:
    text: str
    type: str = "TextRun"
    color: Optional[ct.Colors] = field(default=None, metadata=config(exclude=utils.is_none))
    font_type: Optional[ct.FontType] = field(default=None, metadata=config(exclude=utils.is_none))
    highlight: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    is_subtle: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    italic: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[actions.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    size: Optional[ct.FontSize] = field(default=None, metadata=config(exclude=utils.is_none))
    strikethrough: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    underline: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    weight: Optional[ct.FontWeight] = field(default=None, metadata=config(exclude=utils.is_none))