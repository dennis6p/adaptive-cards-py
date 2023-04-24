from dataclasses import dataclass, field
from typing import TypeVar, Optional
from dataclasses_json import dataclass_json, LetterCase , config
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct
import adaptive_cards.actions as actions

InputText = TypeVar("InputText", bound="InputText")
InputNumber = TypeVar("InputNumber", bound="InputNumber")
InputDate = TypeVar("InputDate", bound="InputDate")
InputTime = TypeVar("InputTime", bound="InputTime")
InputToggle = TypeVar("InputToggle", bound="InputToggle")
InputChoiceSet = TypeVar("InputChoiceSet", bound="InputChoiceSet")
InputChoice = TypeVar("InputChoice", bound="InputChoice")

InputT = InputText | InputNumber | InputDate | InputTime | InputToggle | InputChoiceSet
  
  
# TODO: Metadata  
    
class Input:
    error_message: Optional[str] = field(default=None, metadata=utils.get_metadata("1.3"))
    is_required: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.3"))
    label: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.3"))
    fallback: Optional[InputT] = field(default=None, metadata=utils.get_metadata("1.2"))
    height: Optional[ct.BlockElementHeight] = field(default=None, metadata=utils.get_metadata("1.1"))
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=utils.get_metadata("1.0"))
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    requires: Optional[dict[str, str]] = field(default=None, metadata=utils.get_metadata("1.2"))    

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputText(Input):
    id: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Text", metadata=utils.get_metadata("1.0"))
    is_multiline: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    max_length: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    regex: Optional[str] = field(default=None, metadata=utils.get_metadata("1.3"))
    style: Optional[ct.TextInputStyle] = field(default=None, metadata=utils.get_metadata("1.0"))
    inline_action: Optional[actions.SelectAction] = field(default=None, metadata=utils.get_metadata("1.2"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputNumber(Input):
    id: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Number", metadata=utils.get_metadata("1.0"))
    max: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    max: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputDate(Input):
    id: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Date", metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputTime(Input):
    id: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Time", metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputToggle(Input):
    id: str =  field(metadata=utils.get_metadata("1.0"))
    title: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Toggle", metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value_off: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value_on: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputChoiceSet(Input):
    id: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.ChoiceSet", metadata=utils.get_metadata("1.0"))
    choices: Optional[list[InputChoice]] = field(default=None, metadata=utils.get_metadata("1.0"))
    is_multi_select: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    style: Optional[ct.ChoiceInputStyle] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputChoice:
    title: str = field(metadata=utils.get_metadata("1.0"))
    value: str = field(metadata=utils.get_metadata("1.0"))
    