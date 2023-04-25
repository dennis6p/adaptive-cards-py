from adaptive_cards.card import AdaptiveCard
from dataclasses import dataclass, fields
import dataclasses
from adaptive_cards.elements import ElementT
from adaptive_cards.containers import ContainerT
from adaptive_cards.inputs import InputT
from typing import Any
from enum import Flag

MINIMUM_VERSION_KEY: str = "min_version"

class Result(Flag):
    SUCCESS = 0
    EMPTY_CARD = 1
    INVALID_FIELD_VERSION = 2
    UNEDFINED = 3

@dataclass
class InvalidField:
    parent_type: str
    field_name: str
    version: str

class SchemaValidator:
    def __init__(self) -> None:
        ...
        
    def validate(self, card: AdaptiveCard) -> Result:
        self.__card = card
        self.__reset()
        result: Result = self.__validate_body()
        self.__debug()
        
        return result

    def __reset(self) -> None:
        self.__is_valid = True
        self.__invalid_fields: list[InvalidField] = list()
        
    def __validate_body(self) -> Result:
        if self.__card.body is None:
            return Result.EMPTY_CARD
    
        self.__validate_elements(self.__card.body)
        
        if len(self.__invalid_fields) > 0:
            return Result.INVALID_FIELD_VERSION
        
        return Result.SUCCESS
        

    def __validate_elements(self, items: Any):
        if not isinstance(items, list):
            items = [items]
        
        custom_types: list[Any] = []
        iterables: list[Any] = []
        
        for item in items:
            self.__item = item
            for field in fields(item):
                value: Any = getattr(item, field.name)
                
                if value is None:
                    continue
                
                if isinstance(value, list):
                    iterables.append(value)
                    # self.__validate_elements(value)
                    
                elif dataclasses.is_dataclass(value):
                    custom_types.append(value)
                    # self.__validate_elements(value)
                    
                else:
                    self.__validate_field_version(
                        field.name, 
                        field.metadata.get(MINIMUM_VERSION_KEY)
                    ) 

        
        for iterable in iterables:
            self.__validate_elements(iterable)

        for custom_type in custom_types:
            self.__validate_elements(custom_type)

            
    def __validate_field_version(self, field_name: str, minimum_version: Any) -> None:
        assert(minimum_version is not None)
            
        if float(self.__card.version) < float(minimum_version):
            self.__invalid_fields.append(
                InvalidField(type(self.__item).__name__, field_name, minimum_version)
            )
    
    def __debug(self):
        for invalid_field in self.__invalid_fields:
            print(f"Wrong version for field <{invalid_field.field_name}> " \
                f"in type <{invalid_field.parent_type}> | " \
                f"selected card version {self.__card.version} < minimum field version {invalid_field.version}")
                