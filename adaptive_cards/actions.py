"""Implementations for all adaptive card action types"""

from dataclasses import dataclass, field
from typing import Optional, Any, Union
from dataclasses_json import dataclass_json, LetterCase
from adaptive_cards import utils
import adaptive_cards.card_types as ct

ActionTypes = Union[
    "ActionOpenUrl",
    "ActionSubmit",
    "ActionShowCard",
    "ActionToggleVisibility",
    "ActionExecute",
]
SelectAction = Union[
    "ActionExecute", "ActionOpenUrl", "ActionSubmit", "ActionToggleVisibility"
]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Action:
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

    title: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    icon_url: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0")) # pylint: disable=C0103
    style: Optional[ct.ActionStyle] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    fallback: Optional[ActionTypes] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    tooltip: Optional[str] = field(default=None, metadata=utils.get_metadata("1.5"))
    is_enabled: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    mode: Optional[ct.ActionMode] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    requires: Optional[dict[str, str]] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionOpenUrl(Action):
    """
    Represents an action to open a URL.

    Inherits from Action

    Attributes:
        url: The URL to be opened.
        type: The type of the action. Default is "Action.OpenUrl".
    """

    url: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Action.OpenUrl", metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionSubmit(Action):
    """
    Represents an action to submit data.

    Inherits from Action.

    Attributes:
        type: The type of the action. Default is "Action.Submit".
        data: Optional data associated with the action.
        associated_inputs: Optional associated inputs for the action.
    """

    type: str = field(default="Action.Submit", metadata=utils.get_metadata("1.0"))
    data: Optional[str | Any] = field(default=None, metadata=utils.get_metadata("1.0"))
    associated_inputs: Optional[ct.AssociatedInputs] = field(
        default=None, metadata=utils.get_metadata("1.3")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionShowCard(Action):
    """
    Represents an action to show a card.

    Inherits from Action.

    Attributes:
        type: The type of the action. Default is "Action.ShowCard".
        card: Optional card to show.
    """

    type: str = field(default="Action.ShowCard", metadata=utils.get_metadata("1.0"))
    card: Optional[Any] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TargetElement:
    """
    Represents a target element.

    Attributes:
        element_id: The ID of the target element.
        is_visible: Optional flag indicating the visibility of the target element.
    """

    element_id: str = field(metadata=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionToggleVisibility(Action):
    """
    Represents an action that toggles the visibility of target elements.

    Inherits from Action.

    Attributes:
        target_elements: A list of TargetElement objects representing the target elements to toggle.
        type: The type of the action, set to "Action.ToggleVisibility".
    """

    target_elements: list[TargetElement] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(
        default="Action.ToggleVisibility", metadata=utils.get_metadata("1.2")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    type: str = field(default="Action.ShowCard", metadata=utils.get_metadata("1.4"))
    verb: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    data: Optional[str | Any] = field(default=None, metadata=utils.get_metadata("1.4"))
    associated_inputs: Optional[ct.AssociatedInputs] = field(
        default=None, metadata=utils.get_metadata("1.4")
    )
