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
   Element: Optional[Any] = field(default=None, metadata=config(exclude=utils.is_none))
   separator: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
   spacing: Optional[ct.Spacing] = field(default=None, metadata=config(exclude=utils.is_none))
   id: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
   is_visible: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
   requires: Optional[dict[str, str]] = field(default=None, metadata=config(exclude=utils.is_none))   
   height: Optional[ct.BlockElementHeight] = field(default=None, metadata=config(exclude=utils.is_none))    
           

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ActionSet(ContainerBase):
    actions: list[action.ActionT]
    type: str = "ActionSet"

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Container(ContainerBase):
    items: list[elements.ElementT | ContainerT | inputs.InputT]
    type: str = "Container"
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool]= field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ColumnSet(ContainerBase):
    type: str = "ColumnSet"
    columns: Optional[list[Column]] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Column(ContainerBase):
    items: Optional[list[elements.ElementT]] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str | int] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class FactSet(ContainerBase):
    facts: list[Fact]
    type: str = "FactSet"

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Fact:
    title: str
    value: str

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class ImageSet(ContainerBase):
    images: list[elements.Image]
    type: str = "ImageSet"
    image_size: Optional[ct.ImageSize] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableColumnDefinition:
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str | int] = field(default=None, metadata=config(exclude=utils.is_none))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableRow:
    cells: Optional[TableCell] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class Table(ContainerBase):
    type: str = "Table"
    columns: Optional[list[TableColumnDefinition]] = field(default=None, metadata=config(exclude=utils.is_none))
    rows: Optional[list[TableRow]] = field(default=None, metadata=config(exclude=utils.is_none))
    first_row_as_header: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    show_grid_lines: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    grid_style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class TableCell:
    items: list[elements.ElementT]
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))    