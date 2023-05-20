"""Implementations for adaptive card input types"""

from dataclasses import dataclass, field
from typing import Union, Optional
from dataclasses_json import dataclass_json, LetterCase
from adaptive_cards import utils
import adaptive_cards.card_types as ct
from adaptive_cards import actions

InputTypes = Union[
    "InputText",
    "InputNumber",
    "InputDate",
    "InputTime",
    "InputToggle",
    "InputChoiceSet",
]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Input:
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

    error_message: Optional[str] = field(
        default=None, metadata=utils.get_metadata("1.3")
    )
    is_required: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.3")
    )
    label: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.3"))
    fallback: Optional[InputTypes] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    requires: Optional[dict[str, str]] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = field(default="Input.Text", metadata=utils.get_metadata("1.0"))
    is_multiline: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    max_length: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    regex: Optional[str] = field(default=None, metadata=utils.get_metadata("1.3"))
    style: Optional[ct.TextInputStyle] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    inline_action: Optional[actions.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = field(default="Input.Number", metadata=utils.get_metadata("1.0"))
    max: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    max: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[int] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = field(default="Input.Date", metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputTime(Input):
    """
    Represents an input field for time values.

    Inherits from Input.

    Attributes:
        id: The ID of the input.
        type: The type of the input, which is "Input.Time".
        max: The maximum time allowed for the input. Optional.
        placeholder: The placeholder text for the input. Optional.
        value: The initial value of the input. Optional.
    """

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = field(default="Input.Time", metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    max: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    title: str = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Input.Toggle", metadata=utils.get_metadata("1.0"))
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value_off: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    value_on: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    id: str = field(metadata=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = field(default="Input.ChoiceSet", metadata=utils.get_metadata("1.0"))
    choices: Optional[list["InputChoice"]] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    is_multi_select: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    style: Optional[ct.ChoiceInputStyle] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    value: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    placeholder: Optional[str] = field(default=None, metadata=utils.get_metadata("1.0"))
    wrap: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class InputChoice:
    """
    Represents a choice within an input choice set.

    Attributes:
        title: The title or display text of the choice.
        value: The value associated with the choice.
    """

    title: str = field(metadata=utils.get_metadata("1.0"))
    value: str = field(metadata=utils.get_metadata("1.0"))
