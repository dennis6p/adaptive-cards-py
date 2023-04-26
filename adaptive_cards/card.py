
from adaptive_cards.actions import SelectAction, ActionT
from adaptive_cards.containers import ContainerT
from adaptive_cards.elements import ElementT
from adaptive_cards.inputs import InputT
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config
from typing import TypeVar, Optional
import adaptive_cards.card_types as ct
import adaptive_cards.utils as utils
from abc import ABC

AdaptiveCardBuilder = TypeVar("AdaptiveCardBuilder", bound="AdaptiveCardBuilder")

SCHEMA: str = "http://adaptivecards.io/schemas/adaptive-card.json"
TYPE: str = "AdaptiveCard"
VERSION: str = "1.0"

AdaptiveCard = TypeVar("AdaptiveCard", bound="AdaptiveCard")

class Builder(ABC):
    ...

class AdaptiveCardBuilder(Builder):
    def __init__(self) -> None:
        self.__reset()
        
    def __reset(self) -> None:
        self.__card = AdaptiveCard()
    
    def type(self, type: str) -> AdaptiveCardBuilder:
        self.__card.type = type
        return self
        
    def version(self, version: str) -> AdaptiveCardBuilder:
        self.__card.version = version
        return self
    
    def refresh(self, refresh: ct.Refresh) -> AdaptiveCardBuilder:
        self.__card.refresh = refresh
        return self
    
    def authentication(self, authentication: ct.Authentication) -> AdaptiveCardBuilder:
        self.__card.authentication = authentication
        return self
    
    def select_action(self, select_action: SelectAction) -> AdaptiveCardBuilder:
        self.__card.select_action = select_action
        return self
    
    def fallback_text(self, fallback_text: str) -> AdaptiveCardBuilder:
        self.__card.fallback_text = fallback_text
        return self
    
    def background_image(self, background_image: ct.BackgroundImage) -> AdaptiveCardBuilder:
        self.__card.background_image = background_image
        return self
    
    def metadata(self, metadata: ct.Metadata) -> AdaptiveCardBuilder:
        self.__card.metadata = metadata
        return self
    
    def min_height(self, min_height: str) -> AdaptiveCardBuilder:
        self.__card.min_height = min_height
        return self
    
    def rtl(self, rtl: bool) -> AdaptiveCardBuilder:
        self.__card.rtl = rtl
        return self
    
    def speak(self, speak: str) -> AdaptiveCardBuilder:
        self.__card.speak = speak
        return self
    
    def lang(self, lang: str) -> AdaptiveCardBuilder:
        self.__card.lang = lang
        return self
    
    def vertical_content_alignment(self, 
            vertical_content_align: ct.VerticalAlignment) -> AdaptiveCardBuilder:
        self.__card.vertical_content_align = vertical_content_align
        return self

    def schema(self, version: str) -> AdaptiveCardBuilder:
        self.__card.version = version
        return self
    
    def add_item(self, item: ElementT | ContainerT | InputT) -> AdaptiveCardBuilder:
        if self.__card.body is None:
            self.__card.body = list()
        self.__card.body.append(item)
        return self
    
    def add_items(self, items: list[ElementT | ContainerT | InputT]) -> AdaptiveCardBuilder:
        if self.__card.body is None:
            self.__card.body = list()
        for item in items:
            self.add_item(item)
        
        return self    
    
    def add_action(self, action: ActionT) -> AdaptiveCardBuilder:
        if self.__card.actions is None:
            self.__card.actions = list()
        self.__card.actions.append(action)
        return self
    
    def add_actions(self, actions: list[ActionT]) -> AdaptiveCardBuilder:
        if self.__card.actions is None:
            self.__card.actions = list()
        for action in actions:
            self.add_action(action)
        
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
    body: Optional[list[ElementT | ContainerT | InputT]] = field(default=None, metadata=config(exclude=utils.is_none))
    actions: Optional[list[ActionT]] = field(default=None, metadata=config(exclude=utils.is_none))
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


    
