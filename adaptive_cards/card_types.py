"""Implementations for all general card-related types and enums"""

from dataclasses import dataclass, field
from typing import Optional
from enum import auto
from dataclasses_json import dataclass_json, LetterCase
from strenum import LowercaseStrEnum
from adaptive_cards import utils


class ImageFillMode(LowercaseStrEnum):
    """
    Enumerates the different fill modes for an image.

    Attributes:
        COVER: The image will be scaled to cover the entire area, possibly cropping parts of the
        image.
        REPEAT_HORIZONTALLY: The image will be repeated horizontally to fill the area.
        REPEAT_VERTICALLY: The image will be repeated vertically to fill the area.
        REPEAT: The image will be repeated both horizontally and vertically to fill the area.
    """

    COVER = auto()
    REPEAT_HORIZONTALLY = "repeatHorizontally"
    REPEAT_VERTICALLY = "repeatVertically"
    REPEAT = auto()


class HorizontalAlignment(LowercaseStrEnum):
    """
    Enumerates the horizontal alignment options.

    Attributes:
        LEFT: Aligns the content to the left.
        CENTER: Centers the content horizontally.
        RIGHT: Aligns the content to the right.
    """

    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


class VerticalAlignment(LowercaseStrEnum):
    """
    Enumerates the vertical alignment options.

    Attributes:
        TOP: Aligns the content to the top.
        CENTER: Centers the content vertically.
        BOTTOM: Aligns the content to the bottom.
    """

    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()


class Colors(LowercaseStrEnum):
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

    DEFAULT = auto()
    DARK = auto()
    LIGHT = auto()
    ACCENT = auto()
    GOOD = auto()
    WARNING = auto()
    ATTENTION = auto()


class FontType(LowercaseStrEnum):
    """
    Enumerates the font type options.

    Attributes:
        DEFAULT: The default font type.
        MONOSPACE: A monospace font type.
    """

    DEFAULT = auto()
    MONOSPACE = auto()


class FontSize(LowercaseStrEnum):
    """
    Enumerates the font size options.

    Attributes:
        DEFAULT: The default font size.
        SMALL: A small font size.
        MEDIUM: A medium font size.
        LARGE: A large font size.
        EXTRA_LARGE: An extra large font size.
    """

    DEFAULT = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    EXTRA_LARGE = "extraLarge"


class FontWeight(LowercaseStrEnum):
    """
    Enumerates the font weight options.

    Attributes:
        DEFAULT: The default font weight.
        LIGHTER: A lighter font weight.
        BOLDER: A bolder font weight.
    """

    DEFAULT = auto()
    LIGHTER = auto()
    BOLDER = auto()


class TextBlockStyle(LowercaseStrEnum):
    """
    Enumerates the text block style options.

    Attributes:
        DEFAULT: The default text block style.
        HEADING: A heading style for the text block.
    """

    DEFAULT = auto()
    HEADING = auto()


class BlockElementHeight(LowercaseStrEnum):
    """
    Enumerates the block element height options.

    Attributes:
        AUTO: Automatically adjusts the height.
        STRETCH: Stretches the height to fill available space.
    """

    AUTO = auto()
    STRETCH = auto()


class ImageSize(LowercaseStrEnum):
    """
    Enumerates the image size options.

    Attributes:
        AUTO: Automatically determines the size.
        STRETCH: Stretches the image to fill available space.
        SMALL: A small image size.
        MEDIUM: A medium image size.
        LARGE: A large image size.
    """

    AUTO = auto()
    STRETCH = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class ImageStyle(LowercaseStrEnum):
    """
    Enumerates the image style options.

    Attributes:
        DEFAULT: The default image style.
        PERSON: An image style for representing a person.
    """

    DEFAULT = auto()
    PERSON = auto()


class ContainerStyle(LowercaseStrEnum):
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

    DEFAULT = auto()
    EMPHASIS = auto()
    GOOD = auto()
    ATTENTION = auto()
    WARNING = auto()
    ACCENT = auto()


class Spacing(LowercaseStrEnum):
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

    DEFAULT = auto()
    NONE = auto()
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()
    EXTRA_LARGE = "extraLarge"
    PADDING = auto()


class AssociatedInputs(LowercaseStrEnum):
    """
    Enumerates the associated inputs options.

    Attributes:
        AUTO: Automatically associate inputs.
        NONE: Do not associate inputs.
    """

    AUTO = auto()
    NONE = auto()


class ActionStyle(LowercaseStrEnum):
    """
    Enumerates the action styles.

    Attributes:
        DEFAULT: The default action style.
        POSITIVE: A positive or affirmative action style.
        DESTRUCTIVE: A destructive or negative action style.
    """

    DEFAULT = auto()
    POSITIVE = auto()
    DESTRUCTIVE = auto()


class ActionMode(LowercaseStrEnum):
    """
    Enumerates the action modes.

    Attributes:
        PRIMARY: The primary action mode.
        SECONDARY: The secondary action mode.
    """

    PRIMARY = auto()
    SECONDARY = auto()


class TextInputStyle(LowercaseStrEnum):
    """
    Enumerates the text input styles.

    Attributes:
        TEXT: The default text input style.
        TEL: The telephone number input style.
        URL: The URL input style.
        EMAIL: The email input style.
        PASSWORD: The password input style.
    """

    TEXT = auto()
    TEL = auto()
    URL = auto()
    EMAIL = auto()
    PASSWORD = auto()


class ChoiceInputStyle(LowercaseStrEnum):
    """
    Enumerates the choice input styles.

    Attributes:
        COMPACT: A compact choice input style.
        EXPANDED: An expanded choice input style.
        FILTERED: A filtered choice input style.
    """

    COMPACT = auto()
    EXPANDED = auto()
    FILTERED = auto()


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class BackgroundImage:
    """
    Represents the background image properties.

    Attributes:
        uri: The URI of the background image.
        fill_mode: The fill mode of the image.
        horizontal_alignment: The horizontal alignment of the image.
        vertical_alignment: The vertical alignment of the image.
    """

    uri: str = field(metadata=utils.get_metadata("1.0"))
    fill_mode: Optional[ImageFillMode] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    vertical_alignment: Optional[VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Refresh:
    """
    Represents the refresh properties.

    Attributes:
        action: The action associated with the refresh.
        expires: The expiration time of the refresh.
        user_ids: The list of user IDs associated with the refresh.
    """

    action: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    expires: Optional[str] = field(default=None, metadata=utils.get_metadata("1.6"))
    user_ids: Optional[list[str]] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TokenExchangeResource:
    """
    Represents a token exchange resource.

    Attributes:
        id: The ID of the resource.
        uri: The URI of the resource.
        provider_id: The provider ID associated with the resource.
    """

    id: str = field(default="", metadata=utils.get_metadata("1.4")) # pylint: disable=C0103
    uri: str = field(default="", metadata=utils.get_metadata("1.4"))
    provider_id: str = field(default="", metadata=utils.get_metadata("1.4"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class AuthCardButtons:
    """
    Represents buttons used in an authentication card.

    Attributes:
        type: The type of the button.
        value: The value associated with the button.
        title: The title of the button.
        image: The image URL of the button.
    """

    type: str = field(default="", metadata=utils.get_metadata("1.4"))
    value: str = field(default="", metadata=utils.get_metadata("1.4"))
    title: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    image: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Authentication:
    """
    Represents authentication properties.

    Attributes:
        text: The authentication text.
        connection_name: The connection name.
        token_exchange_resource: The token exchange resource.
        buttons: The authentication buttons.
    """

    text: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    connection_name: Optional[str] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )
    token_exchange_resource: Optional[TokenExchangeResource] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )
    buttons: Optional[AuthCardButtons] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Metadata:
    """
    Represents metadata properties.

    Attributes:
        web_url: The web URL.
    """

    web_url: Optional[str] = field(default=None, metadata=utils.get_metadata("1.6"))
