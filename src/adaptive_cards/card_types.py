"""Implementations for all general card-related types and enums"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

import adaptive_cards.target_frameworks as tf
from adaptive_cards import utils
from adaptive_cards.actions import ActionExecute


class MSTeamsCardWidth(str, Enum):
    """
    Enumerates the different fill modes for an image.

    Attributes:
        FULL: The cards' width will be set to full. Occupies all of the
              available horizontal space.
        NONE: The cards' width will be set to None. Default width.
    """

    FULL = "full"
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


class BackgroundImage(BaseModel):
    """
    Represents the background image properties.

    Attributes:
        uri: The URI of the background image.
        fill_mode: The fill mode of the image.
        horizontal_alignment: The horizontal alignment of the image.
        vertical_alignment: The vertical alignment of the image.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    uri: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    fill_mode: Optional[ImageFillMode] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    vertical_alignment: Optional[VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class RefreshDefinition(BaseModel):
    """Represents the refresh properties."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    action: Optional[ActionExecute] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    """The Action.Execute action to invoke to refresh the card."""

    user_ids: Optional[list[str]] = Field(default=None, json_schema_extra=utils.get_metadata("1.4"))
    """The list of user Ids for which the card will be automatically refreshed.
    In Teams, in chats or channels with more than 60 users, the card will automatically
    refresh only for users specified in the userIds list.
    Other users will have to manually click on a "refresh" button.
    In contexts with fewer than 60 users, the card will automatically refresh for all users."""


class TokenExchangeResource(BaseModel):
    """Represents a token exchange resource."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))  # pylint: disable=C0103
    """The unique identified of this token exchange instance."""

    provider_id: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    """An identifier for the identity provider with which to attempt a token exchange."""

    uri: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    """An application ID or resource identifier with which to exchange a token on behalf of.
    This property is identity provider- and application-specific."""


class AuthCardButton(BaseModel):
    """Represents buttons used in an authentication card."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    """Must be signin."""

    image: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.4"))
    """A URL to an image to display alongside the button’s caption."""

    title: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.4"))
    """The caption of the button."""

    value: str = Field(default="", json_schema_extra=utils.get_metadata("1.4"))
    """The value associated with the button. The meaning of value depends on the button's type."""


class Authentication(BaseModel):
    """Represents authentication properties."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    buttons: Optional[AuthCardButton] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    """The buttons that should be displayed to the user when prompting for authentication.
    The array MUST contain one button of type “signin”. Other button types are not currently supported."""

    connection_name: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    """The identifier for registered OAuth connection setting information."""

    text: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.4"))
    """The text that can be displayed to the end user when prompting them to authenticate."""

    token_exchange_resource: Optional[TokenExchangeResource] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    """Provides information required to enable on-behalf-of single sign-on user authentication."""


class CardMetadata(BaseModel):
    """Represents metadata properties."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    web_url: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.4"))
    """The URL the card originates from. When webUrl is set, the card is dubbed an
    Adaptive Card-based Loop Component and, when pasted in Teams or other Loop
    Component-capable host applications, the URL will unfurl to the same exact card."""


class MentionedEntity(BaseModel):
    """Represents a mentioned person or tag."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))
    """The Id of a person (typically a Microsoft Entra user Id) or tag."""

    mention_type: Optional[str] = Field(
        default="Person", json_schema_extra=utils.get_metadata("1.0")
    )
    """The type of the mentioned entity."""

    name: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))
    """The name of the mentioned entity."""


class Mention(BaseModel):  #
    """Represents a mention to a person."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={"limited_to_target_platforms": [tf.MicrosoftTeams.NAME]},
    )
    type: str = Field(
        default="mention",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
    """Must be mention."""

    mentioned: Optional[MentionedEntity] = Field(
        default=None,
        json_schema_extra=utils.get_metadata("1.0"),
    )
    """Defines the entity being mentioned."""

    text: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))
    """The text that will be substituted with the mention."""


class StringResource(BaseModel):
    """Defines the replacement string values."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    default_value: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """The default value of the string resource, used when no localization is available."""

    localized_values: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    """Localized values of the string, where keys represent the locale (e.g. en-US) in the
    <ISO 639-1>(-<ISO 3166-1 alpha-2>) format. <ISO 639-1> is the 2-letter language code
    and <ISO 3166-1 alpha-2> is the optional 2-letter country code."""


class Resources(BaseModel):
    """The resources that can be used in the body of the card."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    strings: Optional[StringResource] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    """String resources that can provide translations in multiple languages.
    String resources make it possible to craft cards that are automatically localized
    according to the language settings of the application that displays the card."""


class TeamsCardProperties(BaseModel):
    """Represents specific properties for MS Teams as the target framework."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    entities: Optional[Mention] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))
    """The Teams-specific entities associated with the card."""

    width: Optional[MSTeamsCardWidth] = Field(
        default=MSTeamsCardWidth.DEFAULT, json_schema_extra=utils.get_metadata("1.0")
    )
    """Controls the width of the card in a Teams chat.

    Note that setting width to "full" will not actually stretch the card to the "full width" of the chat pane.
    It will only make the card wider than when the width property isn't set."""


class AdaptiveCardReference(BaseModel):
    """A type of reference whose content is an Adaptive Card."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(default="AdaptiveCardReference.", json_schema_extra=utils.get_metadata("1.0"))
    """Must be AdaptiveCardReference."""

    abstract: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """The abstract of the reference, providing a short summary of the reference's content."""

    content: Optional[Any] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """The abstract of the reference, providing a short summary of the reference's content."""

    icon: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Icon to be displayed in the reference."""

    keywords: Optional[list[str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5"), max_length=3
    )
    """Keywords for the reference. Maximum allowed is 3."""

    title: Optional[list[str]] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Title of the reference."""

    url: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Optional URL for the reference title."""


class DocumentReference(BaseModel):
    """A type of reference whose content is an Adaptive Card."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(default="DocumentReference.", json_schema_extra=utils.get_metadata("1.0"))
    """Must be DocumentReference."""

    abstract: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """The abstract of the reference, providing a short summary of the reference's content."""

    icon: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Icon to be displayed in the reference."""

    keywords: Optional[list[str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5"), max_length=3
    )
    """Keywords for the reference. Maximum allowed is 3."""

    title: Optional[list[str]] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Title of the reference."""

    url: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.5"))
    """Optional URL for the reference title."""
