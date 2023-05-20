"""Implementations for adaptive card element types"""

from dataclasses import dataclass, field
from typing import Union, Optional, Any
from dataclasses_json import LetterCase, dataclass_json

from adaptive_cards import actions
from adaptive_cards import utils
import adaptive_cards.card_types as ct

Element = Union["Image", "TextBlock", "Media", "CaptionSource", "RichTextBlock"]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class CardElement:
    """
    Represents a card element.

    Attributes:
        Element: The element of the card.
        separator: Indicates whether a separator should be displayed before the element.
        spacing: The spacing for the element.
        id: The ID of the element.
        is_visible: Indicates whether the element is visible.
        requires: The requirements for the element.
        height: The height of the element.
    """

    element: Optional[Any | Element] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0")) # pylint: disable=C0103
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    requires: Optional[dict[str, str]] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TextBlock(CardElement):
    # pylint: disable=too-many-instance-attributes
    """
    Represents a text block card element.

    Inherits from CardElement.

    Attributes:
        text: The text content of the text block.
        type: The type of the card element.
        color: The color of the text block.
        font_type: The font type of the text block.
        horizontal_alignment: The horizontal alignment of the text block.
        is_subtle: Indicates whether the text block has subtle styling.
        max_lines: The maximum number of lines to display for the text block.
        size: The font size of the text block.
        weight: The font weight of the text block.
        wrap: Indicates whether the text should wrap within the text block.
        style: The style of the text block.
    """

    text: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="TextBlock", metadata=utils.get_metadata("1.0"))
    color: Optional[ct.Colors] = field(default=None, metadata=utils.get_metadata("1.0"))
    font_type: Optional[ct.FontType] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    is_subtle: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    max_lines: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    size: Optional[ct.FontSize] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    weight: Optional[ct.FontWeight] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    style: Optional[ct.TextBlockStyle] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Image(CardElement):
    # pylint: disable=too-many-instance-attributes
    """
    Represents an image card element.

    Inherits from CardElement.

    Attributes:
        url: The URL of the image.
        type: The type of the card element.
        alt_text: The alternative text for the image.
        background_color: The background color of the image.
        horizontal_alignment: The horizontal alignment of the image.
        select_action: The select action associated with the image.
        size: The size of the image.
        style: The style of the image.
        width: The width of the image.
    """

    url: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Image", metadata=utils.get_metadata("1.0"))
    alt_text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    background_color: Optional[str] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    select_action: Optional[actions.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    size: Optional[ct.ImageSize] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    style: Optional[ct.ImageStyle] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    width: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Media(CardElement):
    """
    Represents a media card element.

    Inherits from CardElement.

    Attributes:
        type: The type of the card element.
        sources: The list of media sources.
        poster: The poster image URL.
        alt_text: The alternative text for the media.
        caption_sources: The list of caption sources.
    """

    type: str = field(default="Media", metadata=utils.get_metadata("1.1"))
    sources: list["MediaSource"] = field(metadata=utils.get_metadata("1.1"))
    poster: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    alt_text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    caption_sources: Optional[list["CaptionSource"]] = field(
        default=None, metadata=utils.get_metadata("1.6")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class MediaSource:
    """
    Represents a media source.

    Attributes:
        url: The URL of the media source.
        mime_type: The MIME type of the media source.
    """

    url: str = field(metadata=utils.get_metadata("1.1"))
    mime_type: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class CaptionSource:
    """
    Represents a caption source.

    Attributes:
        mime_type: The MIME type of the caption source.
        url: The URL of the caption source.
        label: The label of the caption source.
    """

    mime_type: str = field(metadata=utils.get_metadata("1.6"))
    url: str = field(metadata=utils.get_metadata("1.6"))
    label: str = field(metadata=utils.get_metadata("1.6"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class RichTextBlock(CardElement):
    """
    Represents a rich text block.

    Inherits from CardElement.

    Attributes:
        inlines: A list of inlines in the rich text block. Each inline can be a string
        or a TextRun object.
        type: The type of the rich text block.
        horizontal_alignment: The horizontal alignment of the rich text block.
    """

    inlines: list[Union[str, "TextRun"]] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="RichTextBlock", metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TextRun:
    # pylint: disable=too-many-instance-attributes
    """
    Represents a text run.

    Attributes:
        text: The text content of the text run.
        type: The type of the text run.
        color: The color of the text run.
        font_type: The font type of the text run.
        highlight: Specifies whether the text run should be highlighted.
        is_subtle: Specifies whether the text run is subtle.
        italic: Specifies whether the text run is italicized.
        select_action: The select action associated with the text run.
        size: The font size of the text run.
        strikethrough: Specifies whether the text run should have a strikethrough effect.
        underline: Specifies whether the text run should be underlined.
        weight: The font weight of the text run.
    """

    text: str = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="TextRun", metadata=utils.get_metadata("1.2"))
    color: Optional[ct.Colors] = field(default=None, metadata=utils.get_metadata("1.2"))
    font_type: Optional[ct.FontType] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    highlight: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    is_subtle: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    italic: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    select_action: Optional[actions.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    size: Optional[ct.FontSize] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    strikethrough: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    underline: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.3"))
    weight: Optional[ct.FontWeight] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
