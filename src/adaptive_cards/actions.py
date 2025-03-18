"""Implementations for all adaptive card action types"""

from __future__ import annotations
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

import adaptive_cards.card_types as ct
from adaptive_cards import utils


class Action(BaseModel):
    # pylint: disable=too-many-instance-attributes
    """
    Represents an action that can be performed.

    Attributes:
        title: An optional string representing the title of the action.
        icon_url: An optional string representing the URL of the icon associated with the action.
        id: An optional string representing the ID of the action.
        style: An optional ActionStyle enum value representing the style of the action.
        fallback: An optional fallback ActionTypes object representing the fallback action to be
        performed.
        tooltip: An optional string representing the tooltip text for the action.
        is_enabled: An optional boolean indicating whether the action is enabled or disabled.
        mode: An optional ActionMode enum value representing the mode of the action.
        requires: An optional dictionary mapping string keys to string values representing the
        requirements for the action.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

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
    fallback: Optional["ActionTypes"] = Field(
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
        type: The type of the action. Default is "Action.OpenUrl".
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    url: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="Action.OpenUrl",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )


class ActionSubmit(Action):
    """
    Represents an action to submit data.

    Inherits from Action.

    Attributes:
        type: The type of the action. Default is "Action.Submit".
        data: Optional data associated with the action.
        associated_inputs: Optional associated inputs for the action.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="Action.Submit",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
    data: Optional[str | Any] = Field(
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
        type: The type of the action. Default is "Action.ShowCard".
        card: Optional card to show.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="Action.ShowCard",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
    card: Optional[Any] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class TargetElement(BaseModel):
    """
    Represents a target element.

    Attributes:
        element_id: The ID of the target element.
        is_visible: Optional flag indicating the visibility of the target element.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    element_id: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class ActionToggleVisibility(Action):
    """
    Represents an action that toggles the visibility of target elements.

    Inherits from Action.

    Attributes:
        target_elements: A list of TargetElement objects representing the target elements to toggle.
        type: The type of the action, set to "Action.ToggleVisibility".
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    target_elements: list[TargetElement] = Field(
        json_schema_extra=utils.get_metadata("1.2")
    )
    type: str = Field(
        default="Action.ToggleVisibility",
        json_schema_extra=utils.get_metadata("1.2"),
        frozen=True,
    )


class ActionExecute(Action):
    """
    Represents an action that executes a command or performs an action.

    Inherits from Action.

    Attributes:
        type: The type of the action, set to "Action.ShowCard".
        verb: An optional string representing the verb of the action.
        data: An optional string or Any type representing additional data associated
        with the action.
        associated_inputs: An optional AssociatedInputs object representing associated
        inputs for the action.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="Action.ShowCard",
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


ActionTypes = Union[
    ActionOpenUrl,
    ActionSubmit,
    ActionShowCard,
    ActionToggleVisibility,
    ActionExecute,
]

SelectAction = Union[
    ActionExecute,
    ActionOpenUrl,
    ActionSubmit,
    ActionToggleVisibility,
]

Action.model_rebuild()
