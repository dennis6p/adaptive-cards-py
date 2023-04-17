from dataclasses import dataclass, field
from typing import TypeVar, Optional, Any, Self
from interfaces.interface import Builder
from dataclasses_json import dataclass_json, LetterCase , config
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct
from abc import ABC

ActionOpenUrl = TypeVar("ActionOpenUrl", bound="ActionOpenUrl")
ActionSubmit = TypeVar("ActionSubmit", bound="ActionSubmit")
ActionShowCard = TypeVar("ActionShowCard", bound="ActionShowCard")
TargetElement = TypeVar("TargetElement", bound="TargetElement")
ActionToggleVisibility = TypeVar("ActionToggleVisibility", bound="ActionToggleVisibility") 
ActionExecute = TypeVar("ActionExecute", bound="ActionExecute") 
ActionT = ActionOpenUrl | ActionSubmit | ActionShowCard | ActionToggleVisibility | ActionExecute
SelectAction = ActionExecute | ActionOpenUrl | ActionSubmit | ActionToggleVisibility
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Action:
    title: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    icon_url: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    id: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ActionStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    fallback: Optional[ActionT] = field(default=None, metadata=config(exclude=utils.is_none))
    tooltip: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    is_enabled: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    mode: Optional[ct.ActionMode] = field(default=None, metadata=config(exclude=utils.is_none))
    requires: Optional[dict[str, str]] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionOpenUrl(Action):
    url: str
    type: str = "Action.OpenUrl"

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class ActionSubmit(Action):
    type: str = "Action.Submit"
    data: Optional[str | Any] = field(default=None, metadata=config(exclude=utils.is_none))
    associated_inputs: Optional[ct.AssociatedInputs] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionShowCard(Action):
    type: str = "Action.ShowCard"
    card: Optional[Any] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TargetElement:
    element_id: str
    is_visible: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionToggleVisibility(Action):
    target_elements: list[TargetElement]
    type: str = "Action.ToggleVisibility"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionExecute(Action):
    type: str = "Action.Execute"
    verb: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    data: Optional[str | Any] = field(default=None, metadata=config(exclude=utils.is_none))
    associated_inputs: Optional[ct.AssociatedInputs] = field(default=None, metadata=config(exclude=utils.is_none))
