"""Implementation of the adaptive card type"""

from __future__ import annotations
from typing import Any, Literal, Optional, Sequence, get_origin, get_args
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic.alias_generators import to_camel

import adaptive_cards.card_types as ct
from adaptive_cards import utils
from adaptive_cards.actions import ActionTypes, SelectAction
from adaptive_cards.containers import ContainerTypes
from adaptive_cards.elements import Element
from adaptive_cards.inputs import InputTypes
from result import Ok, Err, Result

SCHEMA: str = "http://adaptivecards.io/schemas/adaptive-card.json"
TYPE: str = "AdaptiveCard"
CardVersion = Literal["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
VERSION: CardVersion = "1.0"


class AdaptiveCardBuilder:
    """Builder class for creating adaptive cards dynamically"""

    def __init__(self) -> None:
        self.__reset()

    @staticmethod
    def __get_id(
        component: Element | ContainerTypes | InputTypes | ActionTypes,
    ) -> str | None:
        if not hasattr(component, "id"):
            return

        return component.id  # type: ignore -> safe as attribute is checked before

    def __reset(self) -> None:
        self.__card = AdaptiveCard()
        self.__items: dict[str, Element | ContainerTypes | InputTypes] = {}
        self.__actions: dict[str, ActionTypes] = {}

    def version(self, version: CardVersion) -> "AdaptiveCardBuilder":
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
        Set select_action component for card

        Args:
            select_action (SelectAction): Action component when selected

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
            metadata (ct.Metadata): Object with additional metadata

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
        self.__card.schema_ = schema
        return self

    def width(self, width: ct.MSTeamsCardWidth) -> "AdaptiveCardBuilder":
        """
        Set card width for target framework. Please note, changing this property
        will only take affect in MS Teams. Other frameworks will simply ignore this
        field.


        Args:
            width (MSTeamsCardWidth): Width property for card

        Returns:
            AdaptiveCardBuilder: Builder object
        """
        if width == ct.MSTeamsCardWidth.FULL:
            self.__card.msteams = ct.MSTeams(width=width)
            return self

        self.__card.msteams = None
        return self

    def add_item(
        self, item: Element | ContainerTypes | InputTypes
    ) -> "AdaptiveCardBuilder":
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

        # add if id field is set
        if id := self.__get_id(item):
            self.__items[id] = item

        return self

    def add_items(
        self, items: Sequence[Element | ContainerTypes | InputTypes]
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

        # add if id field is set
        if id := self.__get_id(action):
            self.__actions[id] = action
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
            AdaptiveCard: Fully defined adaptive card object
        """
        card: AdaptiveCard = self.__card
        card._items = self.__items
        card._actions = self.__actions

        return self.__card


# pylint: disable=too-many-instance-attributes


class AdaptiveCard(BaseModel):
    """
    Represents an Adaptive Card.

    Attributes:
        type: The type of the Adaptive Card. Defaults to "AdaptiveCard".
        version: The version of the Adaptive Card.
        schema: The schema of the Adaptive Card.
        refresh: The refresh settings for the card.
        authentication: The authentication settings for the card.
        body: The list of card items.
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
        msteams: Set specific properties for MS Teams as the target framework
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    _items: dict[str, Element | ContainerTypes | InputTypes] = PrivateAttr({})
    _actions: dict[str, ActionTypes] = PrivateAttr({})

    type: str = Field(
        default=TYPE, json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    version: str = Field(default=VERSION, json_schema_extra=utils.get_metadata("1.0"))
    schema_: str = Field(
        default=SCHEMA,
        alias="$schema",
        json_schema_extra=utils.get_metadata("1.0", field_name="$schema"),
    )
    refresh: Optional[ct.Refresh] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    authentication: Optional[ct.Authentication] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    body: Optional[list[Element | ContainerTypes | InputTypes]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    actions: Optional[list[ActionTypes]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    fallback_text: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    metadata: Optional[ct.Metadata] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.6")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    speak: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    lang: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    vertical_content_align: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    msteams: Optional[ct.MSTeams] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
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

    @staticmethod
    def __get_field_type_from_annotation(annotation: Any) -> Any:
        """Determine a fields type from its annotation.

        Args:
            annotation (Any): Field annotation

        Returns:
            Any: Type of the field
        """
        if not get_origin(annotation):
            return annotation
        return get_args(annotation)[0]

    @staticmethod
    def __update(
        components: dict[str, Element | ContainerTypes | InputTypes]
        | dict[str, ActionTypes],
        id: str,
        **kwargs,
    ) -> Result[None, str]:
        """Update an item's or action's field value(s).

        Args:
            id (str): id of component to be updated

        Returns:
            Result[None, str]: Result of update procedure. None if successful, Error message otherwise.
        """
        # if id is not found -> exit
        if not components.get(id):
            return Err("No component found for given ID")

        for field, value in kwargs.items():
            # if attribute is not present -> exit
            if not hasattr(components[id], field):
                return Err("Field not found in component")

            # if new value's type doesn't match the expected one -> exit
            field_info = components[id].model_fields[field]
            field_type: Any = AdaptiveCard.__get_field_type_from_annotation(
                field_info.annotation
            )
            if not isinstance(value, field_type):
                return Err("Value type does not match expected field type")

            setattr(components[id], field, value)
        return Ok(None)

    def update_action(self, id: str, **kwargs) -> Result[None, str]:
        """Update an action's field value

        Note:
            The update procedure can only succeed if the following criteria is fulfilled:
            - ID of an component has been set when the card was created initially
            - The property about to be updated must be part of the actual data model of the parent component
            - The property's type must match the defined type in the parent data model

        Examples:
            `card.update_action(id="action-id", title="new title")`

        Args:
            id (str): id of action component to be updated

        Returns:
            Result[None, str]: Result of update procedure. None if successful, error string otherwise.
        """
        return AdaptiveCard.__update(self._actions, id, **kwargs)

    def update_item(self, id: str, **kwargs) -> Result[None, str]:
        """Update an item's field value

        Note:
            The update procedure can only succeed if the following criteria is fulfilled:
            - ID of an component has been set when the card was created initially
            - The property about to be updated must be part of the actual data model of the parent component
            - The property's type must match the defined type in the parent data model

        Examples:
            `card.update_item(id="action-id", text="new text")`

        Args:
            id (str): id of action component to be updated

        Returns:
            Result[None, str]: Result of update procedure. None if successful, error string otherwise.
        """
        return AdaptiveCard.__update(self._items, id, **kwargs)

    def to_json(self) -> str:
        """
        Converts the full adaptive card schema into a json string.

        Returns:
            str: Adaptive card schema as JSON string.
        """
        return self.model_dump_json(exclude_none=True, by_alias=True, warnings=False)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the full adaptive card schema into a dictionary.

        Returns:
            str: Adaptive card schema as dictionary.
        """

        return self.model_dump(exclude_none=True, by_alias=True, warnings=False)


AdaptiveCard.model_rebuild()
