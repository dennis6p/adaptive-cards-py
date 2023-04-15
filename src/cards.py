
from typing import Self, TypeVar, Optional
from src.card_elements import ElementT, TextBlock, Image, Media, MediaSource, CaptionSource, RichTextBlock, TextRun
import src.card_elements as card_elements
from src.card_containers import Container, ContainerT
from interfaces.interface import Builder
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config
import src.card_types as ct
import src.utils as utils
from src.actions import SelectAction, Action

SCHEMA: str = "http://adaptivecards.io/schemas/adaptive-card.json"
TYPE: str = "AdaptiveCard"
VERSION: str = "1.0"

AdaptiveCard = TypeVar("AdaptiveCard", bound="AdaptiveCard")

class AdaptiveCardBuilder(Builder):
    def __init__(self) -> None:
        self.__reset()
        
    def __reset(self) -> None:
        self.__card = AdaptiveCard()
        
    def version(self, version: str) -> Self:
        self.__card.version = version
        return self
    
    def add_item(self, item: ElementT | ContainerT) -> Self:
        if self.__card.body is None:
            self.__card.body = list()
        self.__card.body.append(item)
        return self
    
    def add_items(self, items: list[ElementT | ContainerT]) -> Self:
        if self.__card.body is None:
            self.__card.body = list()
        for item in items:
            self.add_item(item)
        
        return self    
    
    def create(self) -> AdaptiveCard:
        return self.__card

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AdaptiveCard:
    type: str = TYPE
    version: str = VERSION
    refresh: Optional[ct.Refresh] = field(default=None, metadata=config(exclude=utils.is_none))
    authentication: Optional[ct.Authentication] = field(default=None, metadata=config(exclude=utils.is_none))
    body: Optional[list[ElementT | ContainerT]] = field(default=None, metadata=config(exclude=utils.is_none))
    actions: Optional[list[Action]] = field(default=None, metadata=config(exclude=utils.is_none))
    select_action: Optional[SelectAction] = field(default=None, metadata=config(exclude=utils.is_none))
    fallback_text: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    background_image: Optional[ct.BackgroundImage | str] = field(default=None, metadata=config(exclude=utils.is_none))
    metadata: Optional[ct.Metadata] = field(default=None, metadata=config(exclude=utils.is_none))
    min_height: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    rtl: Optional[bool] = field(default=None, metadata=config(exclude=utils.is_none))
    speak: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    lang: Optional[str] = field(default=None, metadata=config(exclude=utils.is_none))
    vertical_content_align: Optional[ct.VerticalAlignment] = field(default=None, metadata=config(exclude=utils.is_none))
    schema: str = field(default=SCHEMA, metadata=config(field_name=f"$schema"))
       
    @staticmethod
    def new():
        return AdaptiveCardBuilder()
    
    def to_json(self) -> str:
        return self.to_json()


    
