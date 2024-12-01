"""Implementations for all general card-related types and enums"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json

from adaptive_cards import utils


class MSTeamsCardWidth(str, Enum):
    """
    Enumerates the different fill modes for an image.

    Attributes:
        FULL: The cards' width will be set to full. Occupies all of the
              available horizontal space.
        NONE: The cards' width will be set to None. Default width.
    """

    FULL = "Full"
    DEFAULT = None


class ImageFillMode(str, Enum):
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


class HorizontalAlignment(str, Enum):
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


class VerticalAlignment(str, Enum):
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


class Colors(str, Enum):
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


# class FontType(str, Enum):
class FontType(str, Enum):
    """
    Enumerates the font type options.

    Attributes:
        DEFAULT: The default font type.
        MONOSPACE: A monospace font type.
    """

    DEFAULT = "default"
    MONOSPACE = "monospace"


class FontSize(str, Enum):
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


class FontWeight(str, Enum):
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


class TextBlockStyle(str, Enum):
    """
    Enumerates the text block style options.

    Attributes:
        DEFAULT: The default text block style.
        HEADING: A heading style for the text block.
    """

    DEFAULT = "default"
    HEADING = "heading"


class BlockElementHeight(str, Enum):
    """
    Enumerates the block element height options.

    Attributes:
        AUTO: Automatically adjusts the height.
        STRETCH: Stretches the height to fill available space.
    """

    AUTO = "auto"
    STRETCH = "stretch"


class ImageSize(str, Enum):
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


class ImageStyle(str, Enum):
    """
    Enumerates the image style options.

    Attributes:
        DEFAULT: The default image style.
        PERSON: An image style for representing a person.
    """

    DEFAULT = "default"
    PERSON = "person"


class ContainerStyle(str, Enum):
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


class Spacing(str, Enum):
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


class AssociatedInputs(str, Enum):
    """
    Enumerates the associated inputs options.

    Attributes:
        AUTO: Automatically associate inputs.
        NONE: Do not associate inputs.
    """

    AUTO = "auto"
    NONE = "none"


class ActionStyle(str, Enum):
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


class ActionMode(str, Enum):
    """
    Enumerates the action modes.

    Attributes:
        PRIMARY: The primary action mode.
        SECONDARY: The secondary action mode.
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"


class TextInputStyle(str, Enum):
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


class ChoiceInputStyle(str, Enum):
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

    id: str = field(default="", metadata=utils.get_metadata("1.4"))  # pylint: disable=C0103
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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class MSTeams:
    """
    Represents specific properties for MS Teams as the target framework.

    Attributes:
        width: The total horizontal space an adaptive cards is allowed to occupy
               when posted to MS Teams. Defaults to "None".
    """

    width: Optional[MSTeamsCardWidth] = field(
        default=MSTeamsCardWidth.DEFAULT, metadata=utils.get_metadata("1.0")
    )
