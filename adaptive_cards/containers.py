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
   fallback: Optional[elements.ElementT | action.ActionT | inputs.InputT] = field(default=None, metadata=utils.get_metadata("1.2"))
   separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
   spacing: Optional[ct.Spacing] = field(default=None, metadata=utils.get_metadata("1.2"))
   id: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
   is_visible: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
   requires: Optional[dict[str, str]] = field(default=None, metadata=utils.get_metadata("1.2"))   
   height: Optional[ct.BlockElementHeight] = field(default=None, metadata=utils.get_metadata("1.1"))    
           

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionSet(ContainerBase):
    actions: list[action.ActionT] = field(metadata=utils.get_metadata("1.2"))
    type: str = field(default="ActionSet", metadata=utils.get_metadata("1.2"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Container(ContainerBase):
    items: list[elements.ElementT | ContainerT | inputs.InputT] = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="Container", metadata=utils.get_metadata("1.0"))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=utils.get_metadata("1.1"))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=utils.get_metadata("1.0"))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.1"))
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool]= field(default=None, metadata=utils.get_metadata("1.5"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ColumnSet(ContainerBase):
    type: str = field(default="ColumnSet", metadata=utils.get_metadata("1.0"))
    columns: Optional[list[Column]] = field(default=None, metadata=utils.get_metadata("1.0"))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=utils.get_metadata("1.1"))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=utils.get_metadata("1.2"))
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Column(ContainerBase):
    items: Optional[list[elements.ElementT]] = field(default=None, metadata=utils.get_metadata("1.0"))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=utils.get_metadata("1.2"))
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    separator: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.0"))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=utils.get_metadata("1.0"))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=utils.get_metadata("1.1"))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=utils.get_metadata("1.0"))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.1"))
    width: Optional[str | int] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class FactSet(ContainerBase):
    facts: list[Fact] = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="FactSet", metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Fact:
    title: str = field(metadata=utils.get_metadata("1.0"))
    value: str = field(metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ImageSet(ContainerBase):
    images: list[elements.Image] = field(metadata=utils.get_metadata("1.0"))
    type: str = field(default="ImageSet", metadata=utils.get_metadata("1.2"))
    image_size: Optional[ct.ImageSize] = field(default=None, metadata=utils.get_metadata("1.0"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableColumnDefinition:
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))
    width: Optional[str | int] = field(default=None, metadata=utils.get_metadata("1.5"))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableRow:
    cells: Optional[TableCell] = field(default=None, metadata=utils.get_metadata("1.5"))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))
    style: Optional[str] = field(default=None, metadata=utils.get_metadata("1.5"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Table(ContainerBase):
    type: str = field(default="Table", metadata=utils.get_metadata("1.5"))
    columns: Optional[list[TableColumnDefinition]] = field(default=None, metadata=utils.get_metadata("1.5"))
    rows: Optional[list[TableRow]] = field(default=None, metadata=utils.get_metadata("1.5"))
    first_row_as_header: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    show_grid_lines: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))
    grid_style: Optional[ct.ContainerStyle] = field(default=None, metadata=utils.get_metadata("1.5"))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.5"))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableCell:
    items: list[elements.ElementT] = field(metadata=utils.get_metadata("1.5"))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=utils.get_metadata("1.1"))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=utils.get_metadata("1.5"))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=utils.get_metadata("1.1"))
    bleed: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.2"))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=utils.get_metadata("1.2"))
    min_height: Optional[str] = field(default=None, metadata=utils.get_metadata("1.2"))
    rtl: Optional[bool] = field(default=None, metadata=utils.get_metadata("1.5"))    