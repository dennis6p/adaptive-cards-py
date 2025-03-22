"""Implementations for all adaptive card container types"""

from __future__ import annotations
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


import adaptive_cards.actions as action
import adaptive_cards.card_types as ct
from adaptive_cards import elements, inputs, utils


class ContainerBase(BaseModel):
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    fallback: Optional[elements.Element | action.ActionTypes | inputs.InputTypes] = (
        Field(default=None, json_schema_extra=utils.get_metadata("1.2"))
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    # pylint: disable=C0103
    id: Optional[str] = Field(default=None, json_schema_extra=utils.get_metadata("1.2"))
    is_visible: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    requires: Optional[dict[str, str]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    height: Optional[ct.BlockElementHeight] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )


class ActionSet(ContainerBase):
    """Represents an action set, a container for a list of actions.

    Inherits from ContainerBase.

    Attributes:
        actions: A list of actions in the action set.
        type: The type of the action set. Defaults to "ActionSet".
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    actions: list[action.ActionTypes] = Field(
        json_schema_extra=utils.get_metadata("1.2")
    )
    type: str = Field(
        default="ActionSet", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    items: list[elements.Element | ContainerTypes | inputs.InputTypes] = Field(
        json_schema_extra=utils.get_metadata("1.0")
    )
    type: str = Field(
        default="Container", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    select_action: Optional[action.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="ColumnSet", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    columns: Optional[list["Column"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[action.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    horizontal_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class Column(ContainerBase):
    # pylint: disable=too-many-instance-attributes
    """Represents a column within a container.

    Inherits from ContainerBase.

    Attributes:
        type: The type of the column. Defaults to "Column".
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="Column", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )
    items: Optional[list[elements.Element | ContainerTypes | inputs.Input]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    separator: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    spacing: Optional[ct.Spacing] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    select_action: Optional[action.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    width: Optional[str | int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class FactSet(ContainerBase):
    """Represents a set of facts within a container.

    Inherits from ContainerBase.

    Attributes:
        facts: A list of Fact objects within the fact set.
        type: The type of the fact set. Defaults to "FactSet".
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    facts: list["Fact"] = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="FactSet", json_schema_extra=utils.get_metadata("1.0"), frozen=True
    )


class Fact(BaseModel):
    """Represents a fact.

    Attributes:
        title: The title of the fact.
        value: The value of the fact.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str = Field(json_schema_extra=utils.get_metadata("1.0"))
    value: str = Field(json_schema_extra=utils.get_metadata("1.0"))


class ImageSet(ContainerBase):
    """Represents a set of images within a container.

    Inherits from ContainerBase.

    Attributes:
        images: A list of Image objects within the image set.
        type: The type of the image set. Defaults to "ImageSet".
        image_size: The size of the images within the image set.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    images: list[elements.Image] = Field(json_schema_extra=utils.get_metadata("1.0"))
    type: str = Field(
        default="ImageSet", json_schema_extra=utils.get_metadata("1.2"), frozen=True
    )
    image_size: Optional[ct.ImageSize] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.0")
    )


class TableColumnDefinition(BaseModel):
    """Represents a definition for a table column.

    Attributes:
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        width: The width of the table column.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    width: Optional[str | int] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class TableRow(BaseModel):
    """Represents a row within a table.

    Attributes:
        cells: The cells within the table row.
        horizontal_cell_content_alignment: The horizontal alignment of cell content.
        vertical_cell_content_alignment: The vertical alignment of cell content.
        style: The style of the table row.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="TableRow", json_schema_extra=utils.get_metadata("1.5"), frozen=True
    )
    cells: Optional[list["TableCell"]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    style: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(default="Table", json_schema_extra=utils.get_metadata("1.5"))
    columns: Optional[list[TableColumnDefinition]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    rows: Optional[list[TableRow]] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    first_row_as_header: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    show_grid_lines: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    grid_style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


class TableCell(BaseModel):
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

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    type: str = Field(
        default="TableCell", json_schema_extra=utils.get_metadata("1.5"), frozen=True
    )
    items: list[elements.Element] = Field(json_schema_extra=utils.get_metadata("1.5"))
    select_action: Optional[action.SelectAction] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    style: Optional[ct.ContainerStyle] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )
    vertical_content_alignment: Optional[ct.VerticalAlignment] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.1")
    )
    bleed: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    background_image: Optional[ct.BackgroundImage | str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    min_height: Optional[str] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.2")
    )
    rtl: Optional[bool] = Field(
        default=None, json_schema_extra=utils.get_metadata("1.5")
    )


ContainerTypes = Union[
    ActionSet,
    Container,
    ColumnSet,
    FactSet,
    ImageSet,
    Table,
]

ContainerBase.model_rebuild()
