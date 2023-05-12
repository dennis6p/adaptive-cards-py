from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config
from typing import TypeVar, Optional, Any

import adaptive_cards.actions as action
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct
import adaptive_cards.elements as elements
import adaptive_cards.inputs as inputs

ActionSet = TypeVar("ActionSet", bound="ActionSet")
Container = TypeVar("Container", bound="Container")
ColumnSet = TypeVar("ColumnSet", bound="ColumnSet")
Column = TypeVar("Column", bound="Column")
FactSet = TypeVar("FactSet", bound="FactSet")
Fact = TypeVar("Fact", bound="Fact")
ImageSet = TypeVar("ImageSet", bound="ImageSet")
Table = TypeVar("Table", bound="Table")
TableCell = TypeVar("TableCell", bound="TableCell")

ContainerT = ActionSet | Container | ColumnSet | FactSet | ImageSet | Table


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ContainerBase:
    """
    The ContainerBase class represents a base container for elements with various properties.

    Attributes:
        fallback: The fallback element, if any, to be displayed when the container cannot be rendered. Defaults to None.
        separator: Determines whether a separator should be shown above the container. Defaults to None.
        spacing: The spacing style to be applied within the container. Defaults to None.
        id: The unique identifier of the container. Defaults to None.
        is_visible: Determines whether the container is visible. Defaults to None.
        requires: A dictionary of requirements that must be satisfied for the container to be displayed. Defaults to None.
        height: The height style to be applied to the container. Defaults to None.
    """

    fallback: Optional[elements.ElementT | action.ActionT | inputs.InputT] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    spacing: Optional[ct.Spacing] = field(
        default=None, metadata=utils.get_metadata("1.2")
    )
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

    actions: list[action.ActionT] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="ActionSet", metadata=utils.get_metadata("1.2"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Container(ContainerBase):
    """Represents a container for elements with various properties.

    Inherits from ContainerBase.

    Attributes:
        items: A list of elements, sub-containers, or input elements contained within the container.
        type: The type of the container. Defaults to "Container".
        select_action: An optional select action associated with the container. Defaults to None.
        style: The style of the container. Defaults to None.
        vertical_content_alignment: The vertical alignment of the container's content. Defaults to None.
        bleed: Determines whether the container bleeds beyond its boundary. Defaults to None.
        background_image: The background image of the container. Defaults to None.
        min_height: The minimum height of the container. Defaults to None.
        rtl: Determines whether the container's content is displayed right-to-left. Defaults to None.
    """

    items: list[elements.ElementT | ContainerT | inputs.InputT] = field(
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
        columns: An optional list of Column objects within the column set. Defaults to None.
        select_action: An optional select action associated with the column set. Defaults to None.
        style: The style of the column set. Defaults to None.
        bleed: Determines whether the column set bleeds beyond its boundary. Defaults to None.
        min_height: The minimum height of the column set. Defaults to None.
        horizontal_alignment: The horizontal alignment of the column set. Defaults to None.
    """

    type: str = field(default="ColumnSet", metadata=utils.get_metadata("1.0"))
    columns: Optional[list[Column]] = field(
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
    """Represents a column within a container.

    Inherits from ContainerBase.

    Attributes:
        items: An optional list of elements contained within the column. Defaults to None.
        background_image: The background image of the column. Defaults to None.
        bleed: Determines whether the column bleeds beyond its boundary. Defaults to None.
        min_height: The minimum height of the column. Defaults to None.
        rtl: Determines whether the column's content is displayed right-to-left. Defaults to None.
        separator: Determines whether a separator should be shown above the column. Defaults to None.
        spacing: The spacing style to be applied within the column. Defaults to None.
        select_action: An optional select action associated with the column. Defaults to None.
        style: The style of the column. Defaults to None.
        vertical_content_alignment: The vertical alignment of the column's content. Defaults to None.
        width: The width of the column. Defaults to None.
    """

    items: Optional[list[elements.ElementT]] = field(
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

    facts: list[Fact] = field(metadata=utils.get_metadata("1.0"))
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
        image_size: The size of the images within the image set. Defaults to None.
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
        horizontal_cell_content_alignment: The horizontal alignment of cell content. Defaults to None.
        vertical_cell_content_alignment: The vertical alignment of cell content. Defaults to None.
        width: The width of the table column. Defaults to None.
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
        cells: The cells within the table row. Defaults to None.
        horizontal_cell_content_alignment: The horizontal alignment of cell content. Defaults to None.
        vertical_cell_content_alignment: The vertical alignment of cell content. Defaults to None.
        style: The style of the table row. Defaults to None.
    """

    cells: Optional[TableCell] = field(default=None, metadata=utils.get_metadata("1.5"))
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
    """Represents a table within a container.

    Inherits from ContainerBase.

    Attributes:
        type: The type of the table. Defaults to "Table".
        columns: The column definitions of the table. Defaults to None.
        rows: The rows of the table. Defaults to None.
        first_row_as_header: Whether the first row should be treated as a header. Defaults to None.
        show_grid_lines: Whether to show grid lines in the table. Defaults to None.
        grid_style: The style of the table grid. Defaults to None.
        horizontal_cell_content_alignment: The horizontal alignment of cell content. Defaults to None.
        vertical_cell_content_alignment: The vertical alignment of cell content. Defaults to None.
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
    """Represents a cell within a table.

    Attributes:
        items: The elements within the cell.
        select_action: The action to perform when the cell is selected. Defaults to None.
        style: The style of the cell. Defaults to None.
        vertical_content_alignment: The vertical alignment of cell content. Defaults to None.
        bleed: Whether the cell should bleed beyond its boundaries. Defaults to None.
        background_image: The background image of the cell. Defaults to None.
        min_height: The minimum height of the cell. Defaults to None.
        rtl: Whether the cell should be rendered in right-to-left direction. Defaults to None.
    """
    items: list[elements.ElementT] = field(metadata=utils.get_metadata("1.5"))
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
