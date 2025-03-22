"""Implementations for adaptive card element types"""

from __future__ import annotations
from typing import Union, Optional, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from adaptive_cards import actions
from adaptive_cards import utils
import adaptive_cards.card_types as ct


class CardElement(BaseModel):
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    element: Optional[Any | Element] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    id: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    requires: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="TextBlock", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    color: Optional[ct.Colors] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    font_type: Optional[ct.FontType] = Field(
        default=None,
        json_schema_extra=utils.get_metadata("1.2"),
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    is_subtle: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    max_lines: Optional[int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    size: Optional[ct.FontSize] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    weight: Optional[ct.FontWeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    wrap: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    style: Optional[ct.TextBlockStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="Image", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    alt_text: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    background_color: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[actions.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    size: Optional[ct.ImageSize] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    style: Optional[ct.ImageStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    width: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="Media", json_schema_extra=utils.get_metadata("1.1"), frozen=True
    )
    sources: list["MediaSource"] = Field(json_schema_extra=utils.get_metadata("1.1"))
    poster: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    alt_text: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    caption_sources: Optional[list["CaptionSource"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.6")
    )


class MediaSource(BaseModel):
    """
    Represents a media source.

    Attributes:
        url: The URL of the media source.
        mime_type: The MIME type of the media source.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str = Field(json_schema_extra=utils.get_metadata("1.1"))
    mime_type: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


class CaptionSource(BaseModel):
    """
    Represents a caption source.

    Attributes:
        mime_type: The MIME type of the caption source.
        url: The URL of the caption source.
        label: The label of the caption source.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    mime_type: str = Field(json_schema_extra=utils.get_metadata("1.6"))
    url: str = Field(json_schema_extra=utils.get_metadata("1.6"))
    label: str = Field(json_schema_extra=utils.get_metadata("1.6"))


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    inlines: list[Union[str, "TextRun"]] = Field(
        json_schema_extra=utils.get_metadata("1.2")
    )
    type: str = Field(
        default="RichTextBlock",
        json_schema_extra=utils.get_metadata("1.2"),
        frozen=True,
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class TextRun(BaseModel):
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    text: str = Field(json_schema_extra=utils.get_metadata("1.2"))
    type: str = Field(
        default="TextRun", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )
    color: Optional[ct.Colors] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    font_type: Optional[ct.FontType] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    highlight: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    is_subtle: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    italic: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    select_action: Optional[actions.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    size: Optional[ct.FontSize] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    strikethrough: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    underline: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )
    weight: Optional[ct.FontWeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


Element = Union[
    Image,
    TextBlock,
    Media,
    CaptionSource,
    RichTextBlock,
]

CardElement.model_rebuild()
