from dataclasses import dataclass, field
from typing import TypeVar, Optional, Any
from dataclasses_json import dataclass_json, LetterCase , config
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct

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
    title: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    icon_url: Optional[str] = field(default=None, metadata=utils.get_metadata("1.1"))
    id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    style: Optional[ct.ActionStyle] = field(default=None, metadata=utils.get_metadata("1.2"))
    fallback: Optional[ActionT] = field(default=None, metadata=utils.get_metadata("1.2"))
    tooltip: Optional[str] = field(default=None, metadata=utils.get_metadata("1.5"))
    is_enabled: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    mode: Optional[ct.ActionMode] = field(default=None, metadata=utils.get_metadata("1.5"))
    requires: Optional[dict[str, str]] = field(default=None, metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionOpenUrl(Action):
    url: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Action.OpenUrl", metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True) 
class ActionSubmit(Action):
    type: str = field(default="Action.Submit", metadata=utils.get_metadata("1.0"))
    data: Optional[str | Any] = field(default=None, metadata=utils.get_metadata("1.0"))
    associated_inputs: Optional[ct.AssociatedInputs] = field(default=None, metadata=utils.get_metadata("1.3"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionShowCard(Action):
    type: str = field(default="Action.ShowCard", metadata=utils.get_metadata("1.0"))
    card: Optional[Any] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TargetElement:
    element_id: str = field(metadata=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionToggleVisibility(Action):
    target_elements: list[TargetElement] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="Action.ToggleVisibility", metadata=utils.get_metadata("1.2"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionExecute(Action):
    type: str = field(default="Action.ShowCard", metadata=utils.get_metadata("1.4"))
    verb: Optional[str] = field(default=None, metadata=utils.get_metadata("1.4"))
    data: Optional[str | Any] = field(default=None, metadata=utils.get_metadata("1.4"))
    associated_inputs: Optional[ct.AssociatedInputs] = field(default=None, metadata=utils.get_metadata("1.4"))
