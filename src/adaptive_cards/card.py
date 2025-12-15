"""Implementation of the adaptive card type"""

from __future__ import annotations

from typing import (
    Annotated,
    Any,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr
from pydantic.alias_generators import to_camel
from result import Err, Ok, Result

import adaptive_cards.types as ct
from adaptive_cards import utils

SCHEMA: str = "http://adaptivecards.io/schemas/adaptive-card.json"
TYPE: str = "AdaptiveCard"
CardVersion = Literal["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]
VERSION: CardVersion = "1.0"

InputTypes = Union[
    "InputText",
    "InputNumber",
    "InputDate",
    "InputTime",
    "InputToggle",
    "InputChoiceSet",
]

Element = Union[
    "Image",
    "TextBlock",
    "Media",
    "CaptionSource",
    "RichTextBlock",
]

ContainerTypes = Union[
    "ActionSet",
    "Container",
    "ColumnSet",
    "FactSet",
    "ImageSet",
    "Table",
]

ActionTypes = Union[
    "ActionOpenUrl",
    "ActionSubmit",
    "ActionShowCard",
    "ActionToggleVisibility",
    "ActionExecute",
]

SelectAction = Union[
    "ActionExecute",
    "ActionOpenUrl",
    "ActionSubmit",
    "ActionToggleVisibility",
]

ItemType = Union[Element, ContainerTypes, InputTypes]
ActionType = ActionTypes

AnnotatedItemType = Annotated[
    Union[
        "InputText",
        "InputNumber",
        "InputDate",
        "InputTime",
        "InputToggle",
        "InputChoiceSet",
        "Image",
        "TextBlock",
        "Media",
        "RichTextBlock",
        "ActionSet",
        "Container",
        "ColumnSet",
        "FactSet",
        "ImageSet",
        "Table",
    ],
    Field(discriminator="type"),
]
AnnotatedItemNoType = Annotated[Union["CaptionSource"], Field()]
AnnotatedItem = Annotated[Union[AnnotatedItemType, AnnotatedItemNoType], Field()]

AnnotatedAction = Annotated[
    Union[
        "ActionOpenUrl",
        "ActionSubmit",
        "ActionShowCard",
        "ActionToggleVisibility",
        "ActionExecute",
    ],
    Field(discriminator="type"),
]

AnnotatedSelectAction = Annotated[
    Union[
        "ActionExecute",
        "ActionOpenUrl",
        "ActionSubmit",
        "ActionToggleVisibility",
    ],
    Field(discriminator="type"),
]


class AdaptiveCardBuilder:
    """Builder class for creating adaptive cards dynamically"""

    def __init__(self) -> None:
        self.__reset()

    @classmethod
    def __collect_id_mappings(
        cls, component: Any
    ) -> dict[str, ItemType] | dict[str, ActionType]:
        """Collect all IDs from a given component and its children recursively.

        Note:
            - If ids are not set they will not be collected
            - If multiple components share the same ID, the last one found will be stored

        Args:
            component (Any): Component to collect IDs from
        Returns:
            dict[str, ItemType] | dict[str, ActionType]: Dictionary with collected IDs and a reference to the component
        """
        components: dict[str, ItemType] | dict[str, ActionType] = {
            "actions": {},
            "items": {},
        }

        if component is None:
            return components

        if isinstance(component, list):
            for c in component:
                results = cls.__collect_id_mappings(c)
                components["actions"].update(results["actions"])
                components["items"].update(results["items"])

        if isinstance(component, AdaptiveCard):
            results: dict[str, dict[str, ItemType] | dict[str, ActionType]] = (
                cls.__collect_id_mappings(
                    component.body or [] + component.actions or []
                )
            )
            components["actions"].update(results["actions"])
            components["items"].update(results["items"])

        id = cls.__get_id(component)
        if isinstance(component, BaseModel):
            if id := cls.__get_id(component):
                key = (
                    "actions" if "Action" in getattr(component, "type", "") else "items"
                )
                components[key][id] = component

            for field, _ in component.model_fields.items():
                value = getattr(component, field)
                if not value:
                    continue
                results = cls.__collect_id_mappings(value)
                components["actions"].update(results["actions"])
                components["items"].update(results["items"])

        return components

    @staticmethod
    def __get_id(
        component: ItemType | ActionType,
    ) -> str | None:
        if not hasattr(component, "id"):
            return

        return component.id  # type: ignore -> safe as attribute is checked before

    def __reset(self) -> None:
        self.__card = AdaptiveCard()
        self.__items: dict[str, ItemType] = {}
        self.__actions: dict[str, ActionType] = {}

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

    def from_json(self, json_data: str) -> "AdaptiveCardBuilder":
        """
        Load adaptive card from JSON string

        Args:
            json_string (str): JSON string representing an adaptive card
        Returns:
            AdaptiveCardBuilder: Builder object
        """
        self.__card = AdaptiveCard.model_validate_json(
            json_data,
        )

        # we have to re-collect all IDs defined in the json file in order to allow updating elements later on
        collected_ids = AdaptiveCardBuilder.__collect_id_mappings(self.__card)

        self.__items = collected_ids["items"]
        self.__actions = collected_ids["actions"]

        return self

    def add_item(self, item: ItemType) -> "AdaptiveCardBuilder":
        """
        Add single element, container or input to card

        Args:
            item (ItemType): Item to be added to card

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

    def add_items(self, items: Sequence[ItemType]) -> "AdaptiveCardBuilder":
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

    def add_action(self, action: ActionType) -> "AdaptiveCardBuilder":
        """
        Add single action to card

        Args:
            action (ActionType): Action to be added

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

    def add_actions(self, actions: list[ActionType]) -> "AdaptiveCardBuilder":
        """
        Add multiple actions to card

        Args:
            actions (list[ActionType]): Actions to be added

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


class ComponentBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AdaptiveCard(ComponentBaseModel):
    """
    Represents an Adaptive Card.

    Attributes:
        type: The type of the Adaptive Card. Defaults to "AdaptiveCard".
        version: The version of the Adaptive Card.
        schema: The schema of the Adaptive Card.
        refresh: The refresh settings for the card.
        authentication: The authentication settings for the card.
        body: The list of card items.
        actions: The list of card
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

    _items: dict[str, ItemType] = PrivateAttr({})
    _actions: dict[str, ActionType] = PrivateAttr({})

    type: Literal["AdaptiveCard"] = Field(
        default="AdaptiveCard", json_schema_extra=utils.get_metadata("1.0"), frozen=True
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
    body: Optional[List[AnnotatedItem]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    actions: Optional[List[AnnotatedAction]] = Field(
        default=None,
        json_schema_extra=utils.get_metadata("1.0"),
    )
    select_action: Optional[AnnotatedSelectAction] = Field(
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
        components: dict[str, AnnotatedItem] | dict[str, AnnotatedAction],
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


class Action(ComponentBaseModel):
    # pylint: disable=too-many-instance-attributes
    """
    Represents an action that can be performed.

    Attributes:
        title: An optional string representing the title of the
        icon_url: An optional string representing the URL of the icon associated with the
        id: An optional string representing the ID of the
        style: An optional ActionStyle enum value representing the style of the
        fallback: An optional fallback AnnotatedAction object representing the fallback action to be
        performed.
        tooltip: An optional string representing the tooltip text for the
        is_enabled: An optional boolean indicating whether the action is enabled or disabled.
        mode: An optional ActionMode enum value representing the mode of the
        requires: An optional dictionary mapping string keys to string values representing the
        requirements for the
    """

    title: Optional[str] = Field(
        default=None,
        json_schema_extra=utils.get_metadata("1.0"),
    )
    icon_url: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    id: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    style: Optional[ct.ActionStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    fallback: Optional["AnnotatedAction"] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    tooltip: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    is_enabled: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    mode: Optional[ct.ActionMode] = Field(
        default=ct.ActionMode.PRIMARY, json_schema_extra=utils.get_metadata("1.5")
    )
    requires: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class ActionOpenUrl(Action):
    """
    Represents an action to open a URL.

    Inherits from Action

    Attributes:
        url: The URL to be opened.
        type: The type of the  Default is "Action.OpenUrl".
    """

    url: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: Literal["Action.OpenUrl"] = Field(
        default="Action.OpenUrl",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )


class ActionSubmit(Action):
    """
    Represents an action to submit data.

    Inherits from Action.

    Attributes:
        type: The type of the  Default is "Action.Submit".
        data: Optional data associated with the
        associated_inputs: Optional associated inputs for the
    """

    type: Literal["Action.Submit"] = Field(
        default="Action.Submit",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
    data: Optional[str | dict[Any, Any]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    associated_inputs: Optional[ct.AssociatedInputs] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )


class ActionShowCard(Action):
    """
    Represents an action to show a card.

    Inherits from Action.

    Attributes:
        type: The type of the  Default is "Action.ShowCard".
        card: Optional card to show.
    """

    type: Literal["Action.ShowCard"] = Field(
        default="Action.ShowCard",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )

    card: Optional["AdaptiveCard"] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )

    # Note: The type hint for 'card' uses a string ("AdaptiveCard") to avoid circular imports.
    # If you need to use AdaptiveCard at runtime (not just for type checking),
    # import it inside the method or function where it's needed.


class TargetElement(ComponentBaseModel):
    """
    Represents a target element.

    Attributes:
        element_id: The ID of the target element.
        is_visible: Optional flag indicating the visibility of the target element.
    """

    element_id: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class ActionToggleVisibility(Action):
    """
    Represents an action that toggles the visibility of target

    Inherits from Action.

    Attributes:
        target_elements: A list of TargetElement objects representing the target elements to toggle.
        type: The type of the action, set to "Action.ToggleVisibility".
    """

    target_elements: list[TargetElement] = Field(
        json_schema_extra=utils.get_metadata("1.2")
    )
    type: Literal["Action.ToggleVisibility"] = Field(
        default="Action.ToggleVisibility",
        json_schema_extra=utils.get_metadata("1.2"),
        frozen=True,
    )


class ActionExecute(Action):
    """
    Represents an action that executes a command or performs an

    Inherits from Action.

    Attributes:
        type: The type of the action, set to "Action.Execute".
        verb: An optional string representing the verb of the
        data: An optional string or Any type representing additional data associated
        with the
        associated_inputs: An optional AssociatedInputs object representing associated
        inputs for the
    """

    type: Literal["Action.Execute"] = Field(
        default="Action.Execute",
        json_schema_extra=utils.get_metadata("1.4"),
        frozen=True,
    )
    verb: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    data: Optional[str | Any] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )
    associated_inputs: Optional[ct.AssociatedInputs] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.4")
    )


class ContainerBase(ComponentBaseModel):
    """
    The ContainerBase class represents a base container for elements with various properties.

    Attributes:
        fallback: The fallback element, if any, to be displayed when the container
        cannot be rendered.
        separator: Determines whether a separator should be shown above the container.
        spacing: The spacing style to be applied within the container.
        id: The unique identifier of the container.
        is_visible: Determines whether the container is visible.
        requires: A dictionary of requirements that must be satisfied for the container
        to be displayed.
        height: The height style to be applied to the container.
    """

    fallback: Optional[Element | AnnotatedAction | InputTypes] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    # pylint: disable=C0103
    id: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.2"))
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    requires: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


class ActionSet(ContainerBase):
    """Represents an action set, a container for a list of actions

    Inherits from ContainerBase.

    Attributes:
        actions: A list of actions in the action set.
        type: The type of the action set. Defaults to "ActionSet".
    """

    type: Literal["ActionSet"] = Field(
        default="ActionSet", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )
    actions: List[AnnotatedAction] = Field(json_schema_extra=utils.get_metadata("1.2"))


class Container(ContainerBase):
    # pylint: disable=too-many-instance-attributes
    """Represents a container for elements with various properties.

    Inherits from ContainerBase.

    Attributes:
        items: A list of elements, sub-containers, or input elements contained within the container.
        type: The type of the container. Defaults to "Container".
        select_action: An optional select action associated with the container.
        style: The style of the container.
        vertical_content_alignment: The vertical alignment of the container's content.
        bleed: Determines whether the container bleeds beyond its boundary.
        background_image: The background image of the container.
        min_height: The minimum height of the container.
        rtl: Determines whether the container's content is displayed right-to-left.
    """

    type: Literal["Container"] = Field(
        default="Container", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    items: List[AnnotatedItem] = Field(json_schema_extra=utils.get_metadata("1.0"))
    select_action: Optional[AnnotatedSelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class ColumnSet(ContainerBase):
    """Represents a set of columns within a container.

    Inherits from ContainerBase.

    Attributes:
        type: The type of the column set. Defaults to "ColumnSet".
        columns: An optional list of Column objects within the column set.
        select_action: An optional select action associated with the column set.
        style: The style of the column set.
        bleed: Determines whether the column set bleeds beyond its boundary.
        min_height: The minimum height of the column set.
        horizontal_alignment: The horizontal alignment of the column set.
    """

    type: Literal["ColumnSet"] = Field(
        default="ColumnSet", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    columns: Optional[list["Column"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[AnnotatedSelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class Column(ContainerBase):
    # pylint: disable=too-many-instance-attributes
    """Represents a column within a container.

    Inherits from ContainerBase.

    Attributes:
        type: The type of the column. Defaults to "Column".
        items: An optional list of elements contained within the column.
        background_image: The background image of the column.
        bleed: Determines whether the column bleeds beyond its boundary.
        min_height: The minimum height of the column.
        rtl: Determines whether the column's content is displayed right-to-left.
        separator: Determines whether a separator should be shown above the column.
        spacing: The spacing style to be applied within the column.
        select_action: An optional select action associated with the column.
        style: The style of the column.
        vertical_content_alignment: The vertical alignment of the column's content.
        width: The width of the column.
    """

    type: Literal["Column"] = Field(
        default="Column", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    items: Optional[list[Element | ContainerTypes | Input]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[AnnotatedSelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    width: Optional[str | int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class FactSet(ContainerBase):
    """Represents a set of facts within a container.

    Inherits from ContainerBase.

    Attributes:
        facts: A list of Fact objects within the fact set.
        type: The type of the fact set. Defaults to "FactSet".
    """

    type: Literal["FactSet"] = Field(
        default="FactSet", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    facts: list["Fact"] = Field(json_schema_extra=utils.get_metadata("1.0"))


class Fact(ComponentBaseModel):
    """Represents a fact.

    Attributes:
        title: The title of the fact.
        value: The value of the fact.
    """

    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    value: str = Field(json_schema_extra=utils.get_metadata("1.0"))


class ImageSet(ContainerBase):
    """Represents a set of images within a container.

    Inherits from ContainerBase.

    Attributes:
        images: A list of Image objects within the image set.
        type: The type of the image set. Defaults to "ImageSet".
        image_size: The size of the images within the image set.
    """

    images: list[Image] = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: Literal["ImageSet"] = Field(
        default="ImageSet", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )
    image_size: Optional[ct.ImageSize] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class TableColumnDefinition(ComponentBaseModel):
    """Represents a definition for a table column.

    Attributes:
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        width: The width of the table column.
    """

    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    width: Optional[str | int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class TableRow(ComponentBaseModel):
    """Represents a row within a table.

    Attributes:
        cells: The cells within the table row.
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        style: The style of the table row.
    """

    type: Literal["TableRow"] = Field(
        default="TableRow", json_schema_extra=utils.get_metadata("1.5"), frozen=True
    )
    cells: Optional[list["TableCell"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    style: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class Table(ContainerBase):
    # pylint: disable=too-many-instance-attributes
    """Represents a table within a container.

    Inherits from ContainerBase.

    Attributes:
        type: The type of the table. Defaults to "Table".
        columns: The column definitions of the table.
        rows: The rows of the table.
        first_row_as_header: Whether the first row should be treated as a header.
        show_grid_lines: Whether to show grid lines in the table.
        grid_style: The style of the table grid.
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
    """

    type: Literal["Table"] = Field(
        default="Table", json_schema_extra=utils.get_metadata("1.5")
    )
    columns: Optional[list[TableColumnDefinition]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    rows: Optional[list[TableRow]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    first_row_as_header: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    show_grid_lines: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    grid_style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class TableCell(ComponentBaseModel):
    # pylint: disable=too-many-instance-attributes
    """Represents a cell within a table.

    Attributes:
        items: The elements within the cell.
        select_action: The action to perform when the cell is selected.
        style: The style of the cell.
        vertical_content_alignment: The vertical alignment of cell content.
        bleed: Whether the cell should bleed beyond its boundaries.
        background_image: The background image of the cell.
        min_height: The minimum height of the cell.
        rtl: Whether the cell should be rendered in right-to-left direction.
    """

    type: Literal["TableCell"] = Field(
        default="TableCell", json_schema_extra=utils.get_metadata("1.5"), frozen=True
    )
    items: list[Element] = Field(json_schema_extra=utils.get_metadata("1.5"))
    select_action: Optional[AnnotatedSelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class CardElement(ComponentBaseModel):
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

    text: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: Literal["TextBlock"] = Field(
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
        height: The height of the image.
        horizontal_alignment: The horizontal alignment of the image.
        select_action: The select action associated with the image.
        size: The size of the image.
        style: The style of the image.
        width: The width of the image.
    """

    url: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: Literal["Image"] = Field(
        default="Image", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    alt_text: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    background_color: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    height: Optional[str | ct.BlockElementHeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[AnnotatedSelectAction] = Field(
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

    type: Literal["Media"] = Field(
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


class MediaSource(ComponentBaseModel):
    """
    Represents a media source.

    Attributes:
        url: The URL of the media source.
        mime_type: The MIME type of the media source.
    """

    url: str = Field(json_schema_extra=utils.get_metadata("1.1"))
    mime_type: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


class CaptionSource(ComponentBaseModel):
    """
    Represents a caption source.

    Attributes:
        mime_type: The MIME type of the caption source.
        url: The URL of the caption source.
        label: The label of the caption source.
    """

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

    inlines: list[Union[str, "TextRun"]] = Field(
        json_schema_extra=utils.get_metadata("1.2")
    )
    type: Literal["RichTextBlock"] = Field(
        default="RichTextBlock",
        json_schema_extra=utils.get_metadata("1.2"),
        frozen=True,
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class TextRun(ComponentBaseModel):
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

    type: Literal["TextRun"] = Field(
        default="TextRun", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )
    text: str = Field(json_schema_extra=utils.get_metadata("1.2"))
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
    select_action: Optional[AnnotatedSelectAction] = Field(
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


class Input(ComponentBaseModel):
    # pylint: disable=too-many-instance-attributes
    """
    Represents an input.

    Attributes:
        error_message: The error message for the input.
        is_required: Specifies whether the input is required.
        label: The label of the input.
        fallback: The fallback input.
        height: The height of the input.
        separator: Specifies whether a separator should be displayed before the input.
        spacing: The spacing of the input.
        is_visible: Specifies whether the input is visible.
        requires: The requirements for the input.
    """

    error_message: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )
    is_required: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )
    label: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )
    fallback: Optional[InputTypes] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    requires: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class InputText(Input):
    # pylint: disable=too-many-instance-attributes
    """
    Represents a text input.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input.
        is_multiline: Specifies whether the input supports multiline text.
        max_length: The maximum length of the input text.
        placeholder: The placeholder text for the input.
        regex: The regular expression pattern for validating the input text.
        style: The style of the text input.
        inline_action: The inline action associated with the input.
        value: The initial value of the input.
    """

    type: Literal["Input.Text"] = Field(
        default="Input.Text", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    is_multiline: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    max_length: Optional[int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    placeholder: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    regex: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.3")
    )
    style: Optional[ct.TextInputStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    inline_action: Optional[AnnotatedSelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    value: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class InputNumber(Input):
    """
    Represents an input field for numerical values.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input, which is "Input.Number".
        max: The maximum value allowed for the input. Optional.
        min: The minimum value allowed for the input. Optional.
        placeholder: The placeholder text for the input. Optional.
        value: The initial value of the input. Optional.
    """

    type: Literal["Input.Number"] = Field(
        default="Input.Number", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    max: Optional[int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    min: Optional[int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    placeholder: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value: Optional[int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class InputDate(Input):
    """
    Represents an input field for date values.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input, which is "Input.Date".
        max: The maximum date allowed for the input. Optional.
        placeholder: The placeholder text for the input. Optional.
        value: The initial value of the input. Optional.
    """

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: Literal["Input.Date"] = Field(
        default="Input.Date", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    max: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    placeholder: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class InputTime(Input):
    """
    Represents an input field for time values.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input, which is "Input.Time".
        max: The maximum time allowed for the input. Optional.
        min: The minimum time allowed for the input. Optional.
        placeholder: The placeholder text for the input. Optional.
        value: The initial value of the input. Optional.
    """

    type: Literal["Input.Time"] = Field(
        default="Input.Time", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    max: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    min: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    placeholder: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class InputToggle(Input):
    """
    Represents a toggle input field.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        title: The title or label for the input.
        type: The type of the input, which is "Input.Toggle".
        value: The initial value of the input. Optional.
        value_off: The value when the toggle is turned off. Optional.
        value_on: The value when the toggle is turned on. Optional.
        wrap: Indicates whether the input should wrap to the next line if needed. Optional.
    """

    type: Literal["Input.Toggle"] = Field(
        default="Input.Toggle", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    value: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value_off: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value_on: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    wrap: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class InputChoiceSet(Input):
    # pylint: disable=too-many-instance-attributes
    """
    Represents a choice set input field.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input, which is "Input.ChoiceSet".
        choices: The list of choices for the input. Optional.
        is_multi_select: Indicates whether multiple choices can be selected. Optional.
        style: The style of the choice input. Optional.
        value: The initial value of the input. Optional.
        placeholder: The placeholder text for the input. Optional.
        wrap: Indicates whether the input should wrap to the next line if needed. Optional.
    """

    type: Literal["Input.ChoiceSet"] = Field(
        default="Input.ChoiceSet",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    choices: Optional[list["InputChoice"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    is_multi_select: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    style: Optional[ct.ChoiceInputStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    value: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    placeholder: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    wrap: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )


class InputChoice(ComponentBaseModel):
    """
    Represents a choice within an input choice set.

    Attributes:
        title: The title or display text of the choice.
        value: The value associated with the choice.
    """

    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    value: str = Field(json_schema_extra=utils.get_metadata("1.0"))


Action.model_rebuild()
ContainerBase.model_rebuild()
Input.model_rebuild()

AdaptiveCard.model_rebuild()
