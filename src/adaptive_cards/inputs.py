"""Implementations for adaptive card input types"""

from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Union, Optional
from adaptive_cards import utils
import adaptive_cards.card_types as ct
from adaptive_cards import actions


class Input(BaseModel):
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = Field(
        default="Input.Text", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
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
    inline_action: Optional[actions.SelectAction] = Field(
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = Field(
        default="Input.Number", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = Field(
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = Field(
        default="Input.Time", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="Input.Toggle", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(json_schema_extra=utils.get_metadata("1.0"))  # pylint: disable=C0103
    type: str = Field(
        default="Input.ChoiceSet",
        json_schema_extra=utils.get_metadata("1.0"),
        frozen=True,
    )
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


class InputChoice(BaseModel):
    """
    Represents a choice within an input choice set.

    Attributes:
        title: The title or display text of the choice.
        value: The value associated with the choice.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    value: str = Field(json_schema_extra=utils.get_metadata("1.0"))


InputTypes = Union[
    InputText,
    InputNumber,
    InputDate,
    InputTime,
    InputToggle,
    InputChoiceSet,
]

Input.model_rebuild()
