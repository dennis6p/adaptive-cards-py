"""Implementation of the adaptive card type"""

from dataclasses import dataclass, field
from typing import Optional
from dataclasses_json import dataclass_json, LetterCase
from adaptive_cards.actions import SelectAction, ActionTypes
from adaptive_cards.containers import ContainerTypes
from adaptive_cards.elements import Element
from adaptive_cards.inputs import InputTypes
from adaptive_cards import utils
import adaptive_cards.card_types as ct


SCHEMA: str = "http://adaptivecards.io/schemas/adaptive-card.json"
TYPE: str = "AdaptiveCard"
VERSION: str = "1.0"


class AdaptiveCardBuilder:
    """Builder class for creating adaptive cards dynamically"""

    def __init__(self) -> None:
        self.__reset()

    def __reset(self) -> None:
        self.__card = AdaptiveCard()

    def type(self, _type: str) -> "AdaptiveCardBuilder":
        """
        Set type of card

        Args:
            type (str): Type of card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.type = _type
        return self

    def version(self, version: str) -> "AdaptiveCardBuilder":
        """
        Set card version

        Args:
            version (str): Version of card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.version = version
        return self

    def refresh(self, refresh: ct.Refresh) -> "AdaptiveCardBuilder":
        """
        Set refresh mode

        Args:
            refresh (ct.Refresh): Refresh mode

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.refresh = refresh
        return self

    def authentication(
        self, authentication: ct.Authentication
    ) -> "AdaptiveCardBuilder":
        """
        Set authentication mode

        Args:
            authentication (ct.Authentication): Authentication mode

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.authentication = authentication
        return self

    def select_action(self, select_action: SelectAction) -> "AdaptiveCardBuilder":
        """
        Set select_action element for card

        Args:
            select_action (SelectAction): Action element when selected

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.select_action = select_action
        return self

    def fallback_text(self, fallback_text: str) -> "AdaptiveCardBuilder":
        """
        Set fallback text when rendering fails

        Args:
            fallback_text (str): Text displayed as a fallback

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.fallback_text = fallback_text
        return self

    def background_image(
        self, background_image: ct.BackgroundImage
    ) -> "AdaptiveCardBuilder":
        """
        Set background image for card

        Args:
            background_image (ct.BackgroundImage): Image show as background

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.background_image = background_image
        return self

    def metadata(self, metadata: ct.Metadata) -> "AdaptiveCardBuilder":
        """
        Set additional metadata for card

        Args:
            metadata (ct.Metadata): Object with addtional metadata

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.metadata = metadata
        return self

    def min_height(self, min_height: str) -> "AdaptiveCardBuilder":
        """
        Set minimum card height

        Args:
            min_height (str): Minimum height for card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.min_height = min_height
        return self

    def rtl(self, rtl: bool) -> "AdaptiveCardBuilder":
        """
        Set right-to-left mode for card

        Args:
            rtl (bool): rtl status for card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.rtl = rtl
        return self

    def speak(self, speak: str) -> "AdaptiveCardBuilder":
        """
        Set what should be spoken for card

        Args:
            speak (str): Simple text to be spoken

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.speak = speak
        return self

    def lang(self, lang: str) -> "AdaptiveCardBuilder":
        """
        Set card language

        Args:
            lang (str): Language used for card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.lang = lang
        return self

    def vertical_content_alignment(
        self, vertical_content_align: ct.VerticalAlignment
    ) -> "AdaptiveCardBuilder":
        """
        Set vertical alignment for card

        Args:
            vertical_content_align (ct.VerticalAlignment): Vertical alignment of content

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.vertical_content_align = vertical_content_align
        return self

    def schema(self, schema: str) -> "AdaptiveCardBuilder":
        """
        Set card schema

        Args:
            schema (str): Card schema

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card.schema = schema
        return self

    def add_item(self, item: Element | ContainerTypes | InputTypes) -> "AdaptiveCardBuilder":
        """
        Add single element, container or input to card

        Args:
            item (Element | ContainerTypes | InputTypes): Item to be added to card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        if self.__card.body is None:
            self.__card.body = []
        self.__card.body.append(item)
        return self

    def add_items(
        self, items: list[Element | ContainerTypes | InputTypes]
    ) -> "AdaptiveCardBuilder":
        """
        Add multiple elements, containers or inputs to card

        Args:
            items (list[Element  |  ContainerTypes  |  InputTypes]): Items to be added to card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        if self.__card.body is None:
            self.__card.body = []
        for item in items:
            self.add_item(item)

        return self

    def add_action(self, action: ActionTypes) -> "AdaptiveCardBuilder":
        """
        Add single action to card

        Args:
            action (ActionTypes): Action to be added

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        if self.__card.actions is None:
            self.__card.actions = []
        self.__card.actions.append(action)
        return self

    def add_actions(self, actions: list[ActionTypes]) -> "AdaptiveCardBuilder":
        """
        Add multiple actions to card

        Args:
            actions (list[ActionTypes]): Actions to be added

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        if self.__card.actions is None:
            self.__card.actions = []
        for action in actions:
            self.add_action(action)

        return self

    def create(self) -> "AdaptiveCard":
        """
        Create final card object.

        Please note: This method must be called to get a actual card object from the card builder.

        Returns:
            AdaptiveCard: Fully defined apdative card object
        """
        return self.__card


# pylint: disable=too-many-instance-attributes
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AdaptiveCard:
    """
    Represents an Adaptive Card.

    Attributes:
        type: The type of the Adaptive Card. Defaults to "AdaptiveCard".
        version: The version of the Adaptive Card.
        schema: The schema of the Adaptive Card.
        refresh: The refresh settings for the card.
        authentication: The authentication settings for the card.
        body: The list of card elements.
        actions: The list of card actions.
        select_action: The select action for the card.
        fallback_text: The fallback text for the card.
        background_image: The background image for the card.
        metadata: The metadata for the card.
        min_height: The minimum height of the card.
        rtl: Whether the card should be displayed right-to-left.
        speak: The speak text for the card.
        lang: The language for the card.
        vertical_content_align: The vertical alignment of the card's content.
    """

    type: str = field(default=TYPE, metadata=utils.get_metadata("1.0"))
    version: str = field(default=VERSION, metadata=utils.get_metadata("1.0"))
    schema: str = field(
        default=SCHEMA, metadata=utils.get_metadata("1.0") | {"field_name": "$schema"}
    )
    refresh: Optional[ct.Refresh] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )
    authentication: Optional[ct.Authentication] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )
    body: Optional[list[Element | ContainerTypes | InputTypes]] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    actions: Optional[list[ActionTypes]] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    select_action: Optional[SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    fallback_text: Optional[str] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    background_image: Optional[ct.BackgroundImage | str] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    metadata: Optional[ct.Metadata] = field(
        default=None, metadata=utils.get_metadata("1.6")
    )
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    speak: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    lang: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    vertical_content_align: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )

    @staticmethod
    def new() -> AdaptiveCardBuilder:
        """
        Create a new adaptive card

        Returns:
             AdaptiveCardBuilder: A builder object which allows to set up an adaptive card
                                  step by step.
        """
        return AdaptiveCardBuilder()

    def to_json(self) -> str:
        """
        Converts the full adaptive card schema into a json string.

        Returns:
            str: Adaptive card schema as JSON string.
        """
        return self.to_json()
