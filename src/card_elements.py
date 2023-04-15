from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config, Undefined
from typing import TypeVar, Self, Optional
from interfaces.interface import Builder

import src.actions as actions
import src.utils as utils
import src.card_types as ct

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

class TextBlockBuilder(Builder):
    def __init__(self, text: str) -> None:
        self.__reset(text)
        
    def __reset(self, text: str) -> None:    
        self.__text_block = TextBlock(text=text)
        
    def color(self, color: ct.Colors) -> Self:
        self.__text_block.color = color
        return self
    
    def font_type(self, font_type: ct.FontType) -> Self:
        self.__text_block.font_type = font_type
        return self
    
    def horizontal_alignment(self, horizontal_alignment: ct.HorizontalAlignment) -> Self:
        self.__text_block.horizontal_alignment = horizontal_alignment
        return self
    
    def is_subtle(self, is_subtle: bool) -> Self:
        self.__text_block.is_subtle = is_subtle
        return self
    
    def max_lines(self, max_lines: int) -> Self:
        self.__text_block.max_lines = max_lines
        return self
    
    def size(self, size: ct.FontSize) -> Self:
        self.__text_block.size = size
        return self
    
    def weight(self, weight: ct.FontWeight) -> Self:
        self.__text_block.weight = weight
        return self
    
    def wrap(self, wrap: bool) -> Self:
        self.__text_block.wrap = wrap
        return self
    
    def style(self, style: ct.TextBlockStyle) -> Self:
        self.__text_block.style = style
        return self
        
    def create(self) -> TextBlock:
        return self.__text_block

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass 
class TextBlock:
    type: str = field(default="TextBlock")
    text: str = ""
    color: Optional[ct.Colors] = field(default=None, metadata=config(exclude=utils.is_none))
    font_type: Optional[ct.FontType] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    is_subtle: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    max_lines: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    size: Optional[ct.FontSize] = field(default=None, metadata=config(exclude=utils.is_none))
    weight: Optional[ct.FontWeight] = field(default=None, metadata=config(exclude=utils.is_none))
    wrap: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.TextBlockStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new(text: str) -> TextBlockBuilder:
        return TextBlockBuilder(text)
    
class ImageBuilder(Builder):
    def __init__(self, url: str, alt_text: str) -> None:
        self.__reset(url, alt_text)
        
    def __reset(self, url: str, alt_text: str) -> None:    
        self.__image = Image(url=url, alt_text=alt_text)
        
    def add_background_color(self, background_color: str) -> Self:
        self.__image.background_color = background_color
        return self
    
    def height(self, height: str) -> Self:
        self.__image.height = height
        return self
    
    def horizontal_alignment(self, horizontal_alignment: ct.HorizontalAlignment) -> Self:
        self.__image.horizontal_alignment = horizontal_alignment
        return self
    
    def select_action(self, select_action: actions.SelectAction) -> Self:
        self.__image.select_action = select_action
        return self
    
    def size(self, size: ct.ImageSize) -> Self:
        self.__image.size = size
        return self
    
    def style(self, style: ct.ImageStyle) -> Self:
        self.__image.style = style
        return self
    
    def width(self, width: str) -> Self:
        self.__image.width = width
        return self
    
        
    def create(self) -> Image:
        return self.__image

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass 
class Image:
    type: str = "Image"
    url: Optional[str] = field(default="", metadata=config(exclude=utils.is_none))
    alt_text: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    background_color: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[actions.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    size: Optional[ct.ImageSize] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ImageStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new(url: str, alt_text: str) -> ImageBuilder:
        return ImageBuilder(url, alt_text)

class MediaBuilder(Builder):
    def __init__(self, sources: list[MediaSource]) -> None:
        self.__reset(sources)
        
    def __reset(self, sources: list[MediaSource]) -> None:    
        self.__media = Media(sources=sources)
    
    def poster(self, poster: str) -> Self:
        self.__media.poster = poster
        return self
    
    def alt_text(self, alt_text: str) -> Self:
        self.__media.alt_text = alt_text
        return self
    
    def caption_sources(self, caption_sources: list[CaptionSource]) -> Self:
        self.__media.caption_sources = caption_sources
        return self
        
    def create(self) -> Media:
        return self.__media

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass 
class Media:
    type: str = "Media"
    sources: list[MediaSource] = field(default_factory=list)
    poster: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    alt_text: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    caption_sources: Optional[list[CaptionSource]] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new(sources: list[MediaSource]) -> MediaBuilder:
        return MediaBuilder(sources)
    
class MediaSourceBuilder(Builder):
    def __init__(self, url: str) -> None:
        self.__reset(url)
        
    def __reset(self, url: str) -> None:    
        self.__media_source = MediaSource(url=url)
    
    def mime_type(self, mime_type: str) -> Self:
        self.__media_source.mime_type = mime_type
        return self
        
    def create(self) -> MediaSource:
        return self.__media_source
    
@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
@dataclass
class MediaSource:
    url: str = field(default="")
    mime_type: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new(url: str) -> MediaSourceBuilder:
        return MediaSourceBuilder(url)

class CaptionSourceBuilder(Builder):
    def __init__(self, mime_type: str, url: str, label: str) -> None:
        self.__reset(mime_type, url, label)
        
    def __reset(self, mime_type: str, url: str, label: str) -> None:    
        self.__caption_source = CaptionSource(mime_type=mime_type, url=url, label=label)
    
    def mime_type(self, mime_type: str) -> Self:
        self.__caption_source.mime_type = mime_type
        return self
    
    def url(self, url: str) -> Self:
        self.__caption_source.url = url
        return self
        
    def label(self, label: str) -> Self:
        self.__caption_source.label = label
        return self
        
    def create(self) -> CaptionSource:
        return self.__caption_source

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CaptionSource:
    mime_type: str = ""
    url: str = ""
    label: str = ""
    
    @staticmethod
    def new(mime_type: str, url: str, label: str) -> CaptionSourceBuilder:
        return CaptionSourceBuilder(mime_type, url, label)
    
class RichTextBlockBuilder(Builder):
    def __init__(self, inlines: list[str | TextRun]) -> None:
        self.__reset(inlines)
        
    def __reset(self, inlines: list[str | TextRun]) -> None:    
        self.__rich_text_block = RichTextBlock(inlines=inlines)
    
    def horizontal_alignment(self, horizontal_alignment: ct.HorizontalAlignment) -> Self:
        self.__rich_text_block.horizontal_alignment = horizontal_alignment
        return self
        
    def create(self) -> RichTextBlock:
        return self.__rich_text_block

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RichTextBlock:
    type: str = "RichTextBlock"
    inlines: list[str | TextRun] = field(default_factory=list)
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new(inlines: list[str | TextRun]) -> RichTextBlockBuilder:
        return RichTextBlockBuilder(inlines)

class TextRunBuilder(Builder):
    def __init__(self, text: str) -> None:
        self.__reset(text)
        
    def __reset(self, text: str) -> None:    
        self.__text_run = TextRun(text=text)
    
    def color(self, color: ct.Colors) -> Self:
        self.__text_run.color = color
        return self
    
    def font_type(self, font_type: ct.FontType) -> Self:
        self.__text_run.font_type = font_type
        return self
        
    def highlight(self, highlight: bool) -> Self:
        self.__text_run.highlight = highlight
        return self
        
    def is_subtle(self, is_subtle: bool) -> Self:
        self.__text_run.is_subtle = is_subtle
        return self
        
    def italic(self, italic: bool) -> Self:
        self.__text_run.italic = italic
        return self
        
    def select_action(self, select_action: actions.SelectAction) -> Self:
        self.__text_run.select_action = select_action
        return self
        
    def size(self, size: ct.FontSize) -> Self:
        self.__text_run.size = size
        return self
        
    def strikethrough(self, strikethrough: bool) -> Self:
        self.__text_run.strikethrough = strikethrough
        return self
        
    def underline(self, underline: bool) -> Self:
        self.__text_run.underline = underline
        return self
        
    def weight(self, weight: ct.FontWeight) -> Self:
        self.__text_run.weight = weight
        return self
        
    def create(self) -> TextRun:
        return self.__text_run

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TextRun:
    type: str = "TextRun"
    text: str = ""
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
    
    @staticmethod
    def new(text: str) -> TextRunBuilder:
        return TextRunBuilder(text)