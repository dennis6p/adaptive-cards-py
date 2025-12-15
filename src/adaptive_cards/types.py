"""Implementations for all general card-related types and enums"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from adaptive_cards import utils


class CaseInsensitiveMixin(str, Enum):
    @classmethod
    def _missing_(cls, value):
        # Convert the input value to lowercase for case-insensitive matching
        value = value.lower()
        for member in cls:
            if member.value.lower() == value:
                return member
        # If no match is found, raise a ValueError
        raise ValueError(f"'{value}' is not a valid {cls.__name__}")


class MSTeamsCardWidth(CaseInsensitiveMixin):
    """
    Enumerates the different fill modes for an image.

    Attributes:
        FULL: The cards' width will be set to full. Occupies all of the
              available horizontal space.
        NONE: The cards' width will be set to None. Default width.
    """

    FULL = "Full"
    DEFAULT = None


class ImageFillMode(CaseInsensitiveMixin):
    """
    Enumerates the different fill modes for an image.

    Attributes:
        COVER: The image will be scaled to cover the entire area, possibly cropping parts of the
        image.
        REPEAT_HORIZONTALLY: The image will be repeated horizontally to fill the area.
        REPEAT_VERTICALLY: The image will be repeated vertically to fill the area.
        REPEAT: The image will be repeated both horizontally and vertically to fill the area.
    """

    COVER = "cover"
    REPEAT_HORIZONTALLY = "repeatHorizontally"
    REPEAT_VERTICALLY = "repeatVertically"
    REPEAT = "repeat"


class HorizontalAlignment(CaseInsensitiveMixin):
    """
    Enumerates the horizontal alignment options.

    Attributes:
        LEFT: Aligns the content to the left.
        CENTER: Centers the content horizontally.
        RIGHT: Aligns the content to the right.
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class VerticalAlignment(CaseInsensitiveMixin):
    """
    Enumerates the vertical alignment options.

    Attributes:
        TOP: Aligns the content to the top.
        CENTER: Centers the content vertically.
        BOTTOM: Aligns the content to the bottom.
    """

    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class Colors(CaseInsensitiveMixin):
    """
    Enumerates the color options.

    Attributes:
        DEFAULT: The default color.
        DARK: A dark color.
        LIGHT: A light color.
        ACCENT: An accent color.
        GOOD: A color indicating a positive or successful state.
        WARNING: A color indicating a warning or caution state.
        ATTENTION: A color indicating an attention or critical state.
    """

    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    ACCENT = "accent"
    GOOD = "good"
    WARNING = "warning"
    ATTENTION = "attention"


class FontType(CaseInsensitiveMixin):
    """
    Enumerates the font type options.

    Attributes:
        DEFAULT: The default font type.
        MONOSPACE: A monospace font type.
    """

    DEFAULT = "default"
    MONOSPACE = "monospace"


class FontSize(CaseInsensitiveMixin):
    """
    Enumerates the font size options.

    Attributes:
        DEFAULT: The default font size.
        SMALL: A small font size.
        MEDIUM: A medium font size.
        LARGE: A large font size.
        EXTRA_LARGE: An extra large font size.
    """

    DEFAULT = "default"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class FontWeight(CaseInsensitiveMixin):
    """
    Enumerates the font weight options.

    Attributes:
        DEFAULT: The default font weight.
        LIGHTER: A lighter font weight.
        BOLDER: A bolder font weight.
    """

    DEFAULT = "default"
    LIGHTER = "lighter"
    BOLDER = "bolder"


class TextBlockStyle(CaseInsensitiveMixin):
    """
    Enumerates the text block style options.

    Attributes:
        DEFAULT: The default text block style.
        HEADING: A heading style for the text block.
    """

    DEFAULT = "default"
    HEADING = "heading"


class BlockElementHeight(CaseInsensitiveMixin):
    """
    Enumerates the block element height options.

    Attributes:
        AUTO: Automatically adjusts the height.
        STRETCH: Stretches the height to fill available space.
    """

    AUTO = "auto"
    STRETCH = "stretch"


class ImageSize(CaseInsensitiveMixin):
    """
    Enumerates the image size options.

    Attributes:
        AUTO: Automatically determines the size.
        STRETCH: Stretches the image to fill available space.
        SMALL: A small image size.
        MEDIUM: A medium image size.
        LARGE: A large image size.
    """

    AUTO = "auto"
    STRETCH = "stretch"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ImageStyle(CaseInsensitiveMixin):
    """
    Enumerates the image style options.

    Attributes:
        DEFAULT: The default image style.
        PERSON: An image style for representing a person.
    """

    DEFAULT = "default"
    PERSON = "person"


class ContainerStyle(CaseInsensitiveMixin):
    """
    Enumerates the container styles.

    Attributes:
        DEFAULT: The default container style.
        EMPHASIS: An emphasis container style.
        GOOD: A container style indicating a positive status.
        ATTENTION: A container style indicating an attention or important status.
        WARNING: A container style indicating a warning or caution status.
        ACCENT: A container style for accentuated content.
    """

    DEFAULT = "default"
    EMPHASIS = "emphasis"
    GOOD = "good"
    ATTENTION = "attention"
    WARNING = "warning"
    ACCENT = "accent"


class Spacing(CaseInsensitiveMixin):
    """
    Enumerates the spacing options.

    Attributes:
        DEFAULT: The default spacing option.
        NONE: No spacing.
        SMALL: Small spacing.
        MEDIUM: Medium spacing.
        LARGE: Large spacing.
        EXTRA_LARGE: Extra large spacing.
        PADDING: Padding spacing.
    """

    DEFAULT = "default"
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"
    PADDING = "padding"


class AssociatedInputs(CaseInsensitiveMixin):
    """
    Enumerates the associated inputs options.

    Attributes:
        AUTO: Automatically associate inputs.
        NONE: Do not associate inputs.
    """

    AUTO = "auto"
    NONE = "none"


class ActionStyle(CaseInsensitiveMixin):
    """
    Enumerates the action styles.

    Attributes:
        DEFAULT: The default action style.
        POSITIVE: A positive or affirmative action style.
        DESTRUCTIVE: A destructive or negative action style.
    """

    DEFAULT = "default"
    POSITIVE = "positive"
    DESTRUCTIVE = "destructive"


class ActionMode(CaseInsensitiveMixin):
    """
    Enumerates the action modes.

    Attributes:
        PRIMARY: The primary action mode.
        SECONDARY: The secondary action mode.
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"


class TextInputStyle(CaseInsensitiveMixin):
    """
    Enumerates the text input styles.

    Attributes:
        TEXT: The default text input style.
        TEL: The telephone number input style.
        URL: The URL input style.
        EMAIL: The email input style.
        PASSWORD: The password input style.
    """

    TEXT = "text"
    TEL = "tel"
    URL = "url"
    EMAIL = "email"
    PASSWORD = "password"


class ChoiceInputStyle(CaseInsensitiveMixin):
    """
    Enumerates the choice input styles.

    Attributes:
        COMPACT: A compact choice input style.
        EXPANDED: An expanded choice input style.
        FILTERED: A filtered choice input style.
    """

    COMPACT = "compact"
    EXPANDED = "expanded"
    FILTERED = "filtered"


class TypeBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BackgroundImage(TypeBaseModel):
    """
    Represents the background image properties.

    Attributes:
        url: The URL of the background image.
        fill_mode: The fill mode of the image.
        horizontal_alignment: The horizontal alignment of the image.
        vertical_alignment: The vertical alignment of the image.
    """

    url: str = Field(json_schema_extra=utils.get_metadata("1.2"))
    fill_mode: Optional[ImageFillMode] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    vertical_alignment: Optional[VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class Refresh(TypeBaseModel):
    """
    Represents the refresh properties.

    Attributes:
        action: The action associated with the refresh.
        expires: The expiration time of the refresh.
        user_ids: The list of user IDs associated with the refresh.
    """

    action: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    expires: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.6")
    )
    user_ids: Optional[list[str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )


class TokenExchangeResource(TypeBaseModel):
    """
    Represents a token exchange resource.

    Attributes:
        id: The ID of the resource.
        uri: The URI of the resource.
        provider_id: The provider ID associated with the resource.
    """

    id: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))  # pylint: disable=C0103
    uri: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    provider_id: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))


class AuthCardButtons(TypeBaseModel):
    """
    Represents buttons used in an authentication card.

    Attributes:
        type: The type of the button.
        value: The value associated with the button.
        title: The title of the button.
        image: The image URL of the button.
    """

    type: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    value: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    title: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    image: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )


class Authentication(TypeBaseModel):
    """
    Represents authentication properties.

    Attributes:
        text: The authentication text.
        connection_name: The connection name.
        token_exchange_resource: The token exchange resource.
        buttons: The authentication buttons.
    """

    text: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    connection_name: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    token_exchange_resource: Optional[TokenExchangeResource] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    buttons: Optional[AuthCardButtons] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )


class Metadata(TypeBaseModel):
    """
    Represents metadata properties.

    Attributes:
        web_url: The web URL.
    """

    web_url: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.6")
    )


class MSTeams(TypeBaseModel):
    """
    Represents specific properties for MS Teams as the target framework.

    Attributes:
        width: The total horizontal space an adaptive cards is allowed to occupy
               when posted to MS Teams. Defaults to "None".
    """

    width: Optional[MSTeamsCardWidth] = Field(
        default=MSTeamsCardWidth.DEFAULT, json_schema_extra=utils.get_metadata("1.0")
    )
