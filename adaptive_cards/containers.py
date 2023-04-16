from dataclasses import dataclass, field
from dataclasses_json import LetterCase, dataclass_json, config
from typing import TypeVar, Self, Optional
from interfaces.interface import Builder

import adaptive_cards.actions as action
import adaptive_cards.utils as utils
import adaptive_cards.card_types as ct
import adaptive_cards.elements as elements

ActionSet = TypeVar("ActionSet", bound="ActionSet")
Container = TypeVar("Container", bound="Container")
ColumnSet = TypeVar("ColumnSet", bound="ColumnSet")
Column = TypeVar("Column", bound="Column")
FactSet = TypeVar("FactSet", bound="FactSet")
Fact = TypeVar("Fact", bound="Fact")
ImageSet = TypeVar("ImageSet", bound="ImageSet")
Table = TypeVar("Table", bound="Table")
TableCell = TypeVar("TableCell", bound="TableCell")

ContainerT = ActionSet | Container | ColumnSet | Column | FactSet | Fact | ImageSet | Table | TableCell

class ActionSetBuilder(Builder):
    def __init__(self, actions: list[action.Action]) -> None:
        self.__reset(actions)
        
    def __reset(self, actions: list[action.Action]) -> None:    
        self.__action_set = ActionSet(actions=actions)
        
    def create(self) -> ActionSet:
        return self.__action_set

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ActionSet:
    type: str = "ActionSet"
    actions: list[action.Action] = field(default_factory=list)

    @staticmethod
    def new(actions: list[action.Action]) -> ActionSetBuilder:
        return ActionSetBuilder(actions)
    
class ContainerBuilder(Builder):
    def __init__(self, items: list[elements.ElementT]) -> None:
        self.__reset(items)
        
    def __reset(self, items: list[elements.ElementT]) -> None:    
        self.__container = Container(items=items)
        
    def select_action(self, select_action: action.SelectAction) -> Self:
        self.__container.select_action = select_action
        return self
    
    def style(self, style: ct.ContainerStyle) -> Self:
        self.__container.style = style
        return self
    
    def vertical_content_alignment(self, vertical_content_alignment: ct.VerticalAlignment) -> Self:
        self.__container.vertical_content_alignment = vertical_content_alignment
        return self
    
    def bleed(self, bleed: bool) -> Self:
        self.__container.bleed = bleed
        return self
    
    def background_image(self, background_image: ct.BackgroundImage | str) -> Self:
        self.__container.background_image = background_image
        return self
    
    def min_height(self, min_height: str) -> Self:
        self.__container.min_height = min_height
        return self
    
    def rtl(self, rtl: bool) -> Self:
        self.__container.rtl = rtl
        return self
    
    def create(self) -> Container:
        return self.__container

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Container:
    type: str = "Container"
    items: list[elements.ElementT] = field(default_factory=list)
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool]= field(default=None, metadata=config(exclude=utils.is_none))

    @staticmethod
    def new(items: list[elements.ElementT]) -> ContainerBuilder:
        return ContainerBuilder(items)
    
class ColumnSetBuilder(Builder):
    def __init__(self) -> None:
        self.__reset()
        
    def __reset(self) -> None:    
        self.__column_set = ColumnSet()
        
    def columns(self, columns: list[Column]) -> Self:
        self.__column_set.columns = columns
        return self
    
    def select_action(self, select_action: action.SelectAction) -> Self:
        self.__column_set.select_action = select_action
        return self
    
    def style(self, style: ct.ContainerStyle) -> Self:
        self.__column_set.style = style
        return self
    
    def bleed(self, bleed: bool) -> Self:
        self.__column_set.bleed = bleed
        return self
    
    def min_height(self, min_height: str) -> Self:
        self.__column_set.min_height = min_height
        return self
    
    def horizontal_alignment(self, horizontal_alginment: ct.HorizontalAlignment) -> Self:
        self.__column_set.horizontal_alignment = horizontal_alginment
        return self
        
    def create(self) -> ColumnSet:
        return self.__column_set

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ColumnSet:
    type: str = "ColumnSet"
    columns: Optional[list[Column]] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))

    @staticmethod
    def new() -> ColumnSetBuilder:
        return ColumnSetBuilder()
    
class ColumnBuilder(Builder):
    def __init__(self) -> None:
        self.__reset()
        
    def __reset(self) -> None:    
        self.__column = Column()
        
    def items(self, items: list[elements.ElementT]) -> Self:
        self.__column.items = items
        return self
    
    def background_image(self, background_image: ct.BackgroundImage | str) -> Self:
        self.__column.background_image = background_image
        return self
    
    def bleed(self, bleed: bool) -> Self:
        self.__column.bleed = bleed
        return self
    
    def fallback(self, fallback: Column | str) -> Self:
        self.__column.fallback = fallback
        return self
    
    def min_height(self, min_height: str) -> Self:
        self.__column.min_height = min_height
        return self
    
    def rtl(self, rtl: bool) -> Self:
        self.__column.rtl = rtl
        return self
    
    def separator(self, separator: bool) -> Self:
        self.__column.separator = separator
        return self
    
    def spacing(self, spacing: ct.Spacing) -> Self:
        self.__column.spacing = spacing
        return self
    
    def select_action(self, select_action: action.SelectAction) -> Self:
        self.__column.select_action = select_action
        return self
    
    def style(self, style: ct.ContainerStyle) -> Self:
        self.__column.style = style
        return self
    
    def vertical_contant_alignment(self, vertical_contant_alignment: ct.VerticalAlignment) -> Self:
        self.__column.vertical_content_alignment = vertical_contant_alignment
        return self
    
    def width(self, width: str | int) -> Self:
        self.__column.width = width
        return self
        
    def create(self) -> Column:
        return self.__column

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Column:
    items: Optional[list[elements.ElementT]] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    fallback: Optional[Self | str] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    separator: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    spacing: Optional[ct.Spacing] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str | int] = field(default=None, metadata=config(exclude=utils.is_none))

    @staticmethod
    def new() -> ColumnBuilder:
        return ColumnBuilder()
    
class FactSetBuilder(Builder):
    def __init__(self, facts: list[Fact]) -> None:
        self.__reset(facts)
        
    def __reset(self, facts: list[Fact]) -> None:    
        self.__fact_set = FactSet(facts=facts)
        
    def create(self) -> FactSet:
        return self.__fact_set

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FactSet:
    type: str = "FactSet"
    facts: list[Fact] = field(default_factory=list)

    @staticmethod
    def new(facts: list[Fact]) -> FactSetBuilder:
        return FactSetBuilder(facts)
    
class FactBuilder(Builder):
    def __init__(self, title: str, value: str) -> None:
        self.__reset(title, value)
        
    def __reset(self, title: str, value: str) -> None:    
        self.__fact = Fact(title=title, value=value)
        
    def create(self) -> Fact:
        return self.__fact

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Fact:
    title: str = ""
    value: str = ""

    @staticmethod
    def new(title: str, value: str) -> FactBuilder:
        return FactBuilder(title, value)

class ImageSetBuilder(Builder):
    def __init__(self, images: list[elements.Image]) -> None:
        self.__reset(images)
        
    def __reset(self, images: list[elements.Image]) -> None:    
        self.__image_set = ImageSet(images=images)
        
    def image_size(self, image_size: ct.ImageSize) -> Self:
        self.__image_set.image_size = image_size
        return self
        
    def create(self) -> ImageSet:
        return self.__image_set

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ImageSet:
    type: str = "ImageSet"
    images: list[elements.Image] = field(default_factory=list)
    image_size: Optional[ct.ImageSize] = field(default=None, metadata=config(exclude=utils.is_none))

    @staticmethod
    def new(images: list[elements.Image]) -> ImageSetBuilder:
        return ImageSetBuilder(images)

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TableColumnDefinition:
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    width: Optional[str | int] = field(default=None, metadata=config(exclude=utils.is_none))
    
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TableRow:
    cells: Optional[TableCell] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))

class TableBuilder(Builder):
    def __init__(self) -> None:
        self.__reset()
        
    def __reset(self) -> None:    
        self.__table = Table()
        
    def columns(self, columns: list[TableColumnDefinition]) -> Self:
        self.__table.columns = columns
        return self
        
    def rows(self, rows: list[TableRow]) -> Self:
        self.__table.rows = rows
        return self
        
    def first_row_as_header(self, first_row_as_header: bool) -> Self:
        self.__table.first_row_as_header = first_row_as_header
        return self
        
    def show_grid_lines(self, show_grid_lines: bool) -> Self:
        self.__table.show_grid_lines = show_grid_lines
        return self
        
    def grid_style(self, grid_style: ct.ContainerStyle) -> Self:
        self.__table.grid_style = grid_style
        return self
        
    def horizontal_cell_content_alignment(self, horizontal_cell_content_alignment: ct.HorizontalAlignment) -> Self:
        self.__table.horizontal_cell_content_alignment = horizontal_cell_content_alignment
        return self
        
    def vertical_cell_content_alignment(self, vertical_cell_content_alignment: ct.VerticalAlignment) -> Self:
        self.__table.vertical_cell_content_alignment = vertical_cell_content_alignment
        return self
        
    def create(self) -> Table:
        return self.__table

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Table:
    type: str = "Table"
    columns: Optional[list[TableColumnDefinition]] = field(default=None, metadata=config(exclude=utils.is_none))
    rows: Optional[list[TableRow]] = field(default=None, metadata=config(exclude=utils.is_none))
    first_row_as_header: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    show_grid_lines: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    grid_style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    horizontal_cell_content_alignment: Optional[ct.HorizontalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_cell_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    
    @staticmethod
    def new() -> TableBuilder:
        return TableBuilder()

class TableCellBuilder(Builder):
    def __init__(self, items: list[elements.ElementT]) -> None:
        self.__reset(items)
        
    def __reset(self, items: list[elements.ElementT]) -> None:    
        self.__table_cell = TableCell(items=items)
        
    def select_action(self, select_action: action.SelectAction) -> Self:
        self.__table_cell.select_action = select_action
        return self
        
    def style(self, style: ct.ContainerStyle) -> Self:
        self.__table_cell.style = style
        return self
        
    def vertical_content_alignment(self, vertical_content_alignment: ct.VerticalAlignment) -> Self:
        self.__table_cell.vertical_content_alignment = vertical_content_alignment
        return self
        
    def bleed(self, bleed: bool) -> Self:
        self.__table_cell.bleed = bleed
        return self
        
    def background_image(self, background_image: ct.BackgroundImage | str) -> Self:
        self.__table_cell.background_image = background_image
        return self
        
    def min_height(self, min_height: str) -> Self:
        self.__table_cell.min_height = min_height
        return self
        
    def rtl(self, rtl: bool) -> Self:
        self.__table_cell.rtl = rtl
        return self
        
    def create(self) -> TableCell:
        return self.__table_cell

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TableCell:
    items: list[elements.ElementT] = field(default_factory=list)
    select_action: Optional[action.SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    style: Optional[ct.ContainerStyle] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_alignment: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    bleed: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))    
    
    @staticmethod
    def new(items: list[elements.ElementT]) -> TableCellBuilder:
        return TableCellBuilder(items)