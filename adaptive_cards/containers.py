"""Implementations for all adaptive card container types"""

from dataclasses import dataclass, field
from typing import Optional, Union
from dataclasses_json import LetterCase, dataclass_json

from adaptive_cards import elements
from adaptive_cards import inputs
from adaptive_cards import utils
import adaptive_cards.actions as action
import adaptive_cards.card_types as ct

ContainerTypes = Union[
    "ActionSet", "Container", "ColumnSet", "FactSet", "ImageSet", "Table"
]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ContainerBase:
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

    fallback: Optional[
        elements.Element | action.ActionTypes | inputs.InputTypes
    ] = field(default=None, metadata=utils.get_metadata("1.2"))
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    spacing: Optional[ct.Spacing] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    # pylint: disable=C0103
    id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    requires: Optional[dict[str, str]] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionSet(ContainerBase):
    """Represents an action set, a container for a list of actions.

    Inherits from ContainerBase.

    Attributes:
        actions: A list of actions in the action set.
        type: The type of the action set. Defaults to "ActionSet".
    """

    actions: list[action.ActionTypes] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="ActionSet", metadata=utils.get_metadata("1.2"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    items: list[elements.Element | ContainerTypes | inputs.InputTypes] = field(
        metadata=utils.get_metadata("1.0")
    )
    type: str = field(default="Container", metadata=utils.get_metadata("1.0"))
    select_action: Optional[action.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    background_image: Optional[ct.BackgroundImage | str] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    type: str = field(default="ColumnSet", metadata=utils.get_metadata("1.0"))
    columns: Optional[list["Column"]] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    select_action: Optional[action.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Column(ContainerBase):
    # pylint: disable=too-many-instance-attributes
    """Represents a column within a container.

    Inherits from ContainerBase.

    Attributes:
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

    items: Optional[list[elements.Element]] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    background_image: Optional[ct.BackgroundImage | str] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    select_action: Optional[action.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    width: Optional[str | int] = field(default=None, metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class FactSet(ContainerBase):
    """Represents a set of facts within a container.

    Inherits from ContainerBase.

    Attributes:
        facts: A list of Fact objects within the fact set.
        type: The type of the fact set. Defaults to "FactSet".
    """

    facts: list["Fact"] = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="FactSet", metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Fact:
    """Represents a fact.

    Attributes:
        title: The title of the fact.
        value: The value of the fact.
    """

    title: str = field(metadata=utils.get_metadata("1.0"))
    value: str = field(metadata=utils.get_metadata("1.0"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ImageSet(ContainerBase):
    """Represents a set of images within a container.

    Inherits from ContainerBase.

    Attributes:
        images: A list of Image objects within the image set.
        type: The type of the image set. Defaults to "ImageSet".
        image_size: The size of the images within the image set.
    """

    images: list[elements.Image] = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="ImageSet", metadata=utils.get_metadata("1.2"))
    image_size: Optional[ct.ImageSize] = field(
        default=None, metadata=utils.get_metadata("1.0")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableColumnDefinition:
    """Represents a definition for a table column.

    Attributes:
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        width: The width of the table column.
    """

    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    width: Optional[str | int] = field(default=None, metadata=utils.get_metadata("1.5"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableRow:
    """Represents a row within a table.

    Attributes:
        cells: The cells within the table row.
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        style: The style of the table row.
    """

    cells: Optional["TableCell"] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    style: Optional[str] = field(default=None, metadata=utils.get_metadata("1.5"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
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

    type: str = field(default="Table", metadata=utils.get_metadata("1.5"))
    columns: Optional[list[TableColumnDefinition]] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    rows: Optional[list[TableRow]] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    first_row_as_header: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    show_grid_lines: Optional[bool] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    grid_style: Optional[ct.ContainerStyle] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableCell:
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

    items: list[elements.Element] = field(metadata=utils.get_metadata("1.5"))
    select_action: Optional[action.SelectAction] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = field(
        default=None, metadata=utils.get_metadata("1.5")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(
        default=None, metadata=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    background_image: Optional[ct.BackgroundImage | str] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
