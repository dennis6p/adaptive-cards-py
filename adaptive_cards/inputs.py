from dataclasses import dataclass, field
from typing import TypeVar, Optional, Any, Self
from dataclasses_json import dataclass_json, LetterCase , config
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct
import adaptive_cards.actions as actions
from abc import ABC

InputText = TypeVar("InputText", bound="InputText")
InputNumber = TypeVar("InputNumber", bound="InputNumber")
InputDate = TypeVar("InputDate", bound="InputDate")
InputTime = TypeVar("InputTime", bound="InputTime")
InputToggle = TypeVar("InputToggle", bound="InputToggle")
InputChoiceSet = TypeVar("InputChoiceSet", bound="InputChoiceSet")
InputChoice = TypeVar("InputChoice", bound="InputChoice")
InputT = InputText | InputNumber | InputDate | InputTime | InputToggle | InputChoiceSet | InputChoice
    
    
class Input:
    error_message: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    is_required: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    label: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    fallback: Optional[InputT] = field(default=None, metadata=config(exclude=utils.is_none))
    height: Optional[ct.BlockElementHeight] = field(default=None, metadata=config(exclude=utils.is_none))
    separator: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=config(exclude=utils.is_none))
    is_visible: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    requires: Optional[dict[str, str]] = field(default=None, metadata=config(exclude=utils.is_none))    

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputText(Input):
    id: str
    type: str = "Input.Text"
    is_multiline: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    max_length: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    placeholder: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    regex: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.TextInputStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    inline_action: Optional[actions.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    value: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputNumber(Input):
    id: str
    type: str = "Input.Number"
    max: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    max: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    placeholder: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    value: Optional[int] = field(default=None, metadata=config(exclude=utils.is_none))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputDate(Input):
    id: str
    type: str = "Input.Date"
    max: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    max: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    placeholder: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    value: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputTime(Input):
    id: str
    type: str = "Input.Date"
    max: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    max: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    placeholder: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    value: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputToggle(Input):
    id: str
    title: str
    type: str = "Input.Toggle"
    value: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    value_off: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    value_on: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    wrap: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputChoiceSet(Input):
    id: str
    type: str = "Input.ChoiceSet"
    choices: Optional[list[InputChoice]] = field(default=None, metadata=config(exclude=utils.is_none))
    is_multi_select: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ChoiceInputStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    value: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    placeholder: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    wrap: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputChoice(Input):
    title: str
    value: str
    