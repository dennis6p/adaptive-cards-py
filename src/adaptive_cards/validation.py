"""Validation class for evaluating a cards schema"""

import json
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from typing import Union

from jsonschema.exceptions import ValidationError as SchemaValidationError
from jsonschema.validators import Draft6Validator

from adaptive_cards.card import AdaptiveCard
from adaptive_cards.target_frameworks import (
    AbstractTargetFramework,
    BotWebChat,
    Outlook,
    MicrosoftTeams,
    CortanaSkills,
    WindowsTimeline,
    CiscoWebExTeams,
    VivaConnections,
    WindowsWidgets,
    SchemaVersion,
)
from result import Result, Err, Ok

MINIMUM_VERSION_KEY: str = "min_version"


class ValidationFailure(str, Enum):
    """Validation failure types"""

    EMPTY_CARD = "card body is empty"
    """card doesn't contain any elements"""

    INVALID_FIELD_VERSION = "field version exceeds card version"
    """used elements might not yet be available for the defined card version"""

    INVALID_SCHEMA = "official card schema violated"
    """card structure does not meet the required schema"""

    SIZE_LIMIT_EXCEEDED = "card exceeds the allowed card size for framework"
    """size of card exceeds the defined limit for the target framework"""

    ID_NOT_FOUND = "ID not found - requested element is not part of the card in scope"
    """ID was not found for any element in card"""

    INVALID_VALUE_TYPE = "Value type does not match the field type meant to be updated"
    """Value type does not match what is expected for the field as per definition in the
    pydantic model"""

    ELEMENT_NOT_SUPPORTED_BY_TARGET_FRAMEWORK = (
        "Validated element is not supported by the target framework"
    )
    """validated element is currently not supported by the target framework"""

    FIELD_NOT_SUPPORTED_BY_TARGET_FRAMEWORK = (
        "Validated field is not supported by the target framework"
    )
    """validated field is currently not supported by the target framework"""


class CardValidatorAbstractFactory(ABC):
    """Abstract card validator factory"""

    @classmethod
    @abstractmethod
    def create_validator_bot(cls) -> "AbstractCardValidator":
        """
        Create card validator for Bot WebChat

        Returns:
            AbstractCardValidator: Card validator for Bot WebChat
        """

    @classmethod
    @abstractmethod
    def create_validator_outlook(cls) -> "AbstractCardValidator":
        """
        Create card validator for outlook

        Returns:
            AbstractCardValidator: Card validator for outlook
        """

    @classmethod
    @abstractmethod
    def create_validator_microsoft_teams(cls) -> "AbstractCardValidator":
        """
        Create card validator for target framework MS Teams

        Returns:
            AbstractCardValidator: Card validator for MS Teams as target framework
        """

    @classmethod
    @abstractmethod
    def create_validator_cortana_skills(cls) -> "AbstractCardValidator":
        """
        Create card validator for Cortana Skills

        Returns:
            AbstractCardValidator: Card validator for Cortana Skills
        """

    @classmethod
    @abstractmethod
    def create_validator_windows_timeline(cls) -> "AbstractCardValidator":
        """
        Create card validator for Windows Timeline

        Returns:
            AbstractCardValidator: Card validator for Windows Timeline
        """

    @classmethod
    @abstractmethod
    def create_validator_cisco_webex_teams(cls) -> "AbstractCardValidator":
        """
        Create card validator for Cisco WebEx Teams

        Returns:
            AbstractCardValidator: Card validator for Cisco WebEx Teams
        """

    @classmethod
    @abstractmethod
    def create_validator_viva_connections(cls) -> "AbstractCardValidator":
        """
        Create card validator for Viva Connections

        Returns:
            AbstractCardValidator: Card validator for Viva Connections
        """

    @classmethod
    @abstractmethod
    def create_validator_windows_widgets(cls) -> "AbstractCardValidator":
        """
        Create card validator for Windows Widgets

        Returns:
            AbstractCardValidator: Card validator for Windows Widgets
        """


class CardValidatorFactory(CardValidatorAbstractFactory):
    """Factory for creating different kinds of card validators"""

    def __init__(self):
        pass

    @classmethod
    def create_validator_bot(cls) -> "CardValidator":
        return CardValidator(BotWebChat())

    @classmethod
    def create_validator_outlook(cls) -> "CardValidator":
        return CardValidator(Outlook())

    @classmethod
    def create_validator_microsoft_teams(cls) -> "CardValidator":
        return CardValidator(MicrosoftTeams())

    @classmethod
    def create_validator_cortana_skills(cls) -> "CardValidator":
        return CardValidator(CortanaSkills())

    @classmethod
    def create_validator_windows_timeline(cls) -> "CardValidator":
        return CardValidator(WindowsTimeline())

    @classmethod
    def create_validator_cisco_webex_teams(cls) -> "CardValidator":
        return CardValidator(CiscoWebExTeams())

    @classmethod
    def create_validator_viva_connections(cls) -> "CardValidator":
        return CardValidator(VivaConnections())

    @classmethod
    def create_validator_windows_widgets(cls) -> "CardValidator":
        return CardValidator(WindowsWidgets())


class Finding(BaseModel):
    """
    Class for storing an individual finding during schema validation
    """

    failure: ValidationFailure
    """Validation failure"""

    message: str
    """Corresponding failure message"""

    message_additional: str = ""
    """Addition information"""

    def __init__(
        self,
        failure: ValidationFailure,
        message: str,
        message_additional: str = "",
    ) -> None:
        super(Finding, self).__init__(
            failure=failure,
            message=message,
            message_additional=message_additional,
        )


class AbstractCardValidator(ABC):
    """
    Abstract interface for card validators
    """

    @abstractmethod
    def validate(self, card: AdaptiveCard, debug: bool = True) -> Result[None, Err]:
        """
        Run validation on card.

        Args:
            card (AdaptiveCard): Card to be validated

        Returns:
            Result[None, Err]: Result of validation
        """

    @classmethod
    @abstractmethod
    def card_size(cls, card: AdaptiveCard) -> float:
        """
        Get size of card in KB

        Args:
            card (AdaptiveCard): Card the size should be calculated for

        Returns:
            float: Card size in KB
        """

    @abstractmethod
    def details(self) -> list[Finding]:
        """
        Return a list of all individual findings occurred during the last validation. The data
        will last until a new validation is executed.

        Returns:
            list[Finding]: List of findings
        """


class CardValidator(AbstractCardValidator):
    """
    Validator class for checking a cards schema w.r.t. to version numbers of individual fields,
    card size and the overall card structure against the expected schema.
    """

    def __init__(self, target_framework: AbstractTargetFramework) -> None:
        self.__target_framework: AbstractTargetFramework = target_framework
        self.__schema_version: SchemaVersion = target_framework.schema_version()

        self.__card: AdaptiveCard
        self.__item: Any
        self.__findings: list[Finding]
        self.__card_size: float

    def validate(self, card: AdaptiveCard, debug: bool = True) -> Result[None, str]:
        self.__card = card
        self.__reset()
        self.__validate_card()

        if debug:
            self.__debug()

        return Ok(None) if len(self.__findings) == 0 else Err("Validation failed")

    @classmethod
    def card_size(cls, card: AdaptiveCard) -> float:
        return cls.__calculate_card_size(card)

    def details(self) -> list[Finding]:
        return self.__findings

    def __reset(self) -> None:
        self.__findings = []
        self.__card_size: float = 0

    def __validate_card(self) -> None:
        # check whether card body is empty or not
        self.__validate_card_body()

        # Check whether the overall card structure matches the expected schema
        self.__validate_schema()

        # check whether the version requirements are fulfilled for all elements
        self.__validate_target_framework_compatibility(self.__card.body)

        # check whether the card size is within the expected range
        # sizes are derived from the original documentation
        # https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cdesktop%2Cdesktop1%2Cdesktop2%2Cconnector-html#mention-support-within-adaptive-cards # pylint: disable=line-too-long
        self.__validate_card_size()

    def __validate_card_body(self) -> None:
        if self.__card.body is None:
            self.__findings.append(
                Finding(
                    ValidationFailure.EMPTY_CARD,
                    ValidationFailure.EMPTY_CARD.value,
                )
            )

    @staticmethod
    def __to_list(items: Any | list[Any]) -> list[Any]:
        """
        Put single item into list or keep data as is, if already of type list

        Args:
            items (Any | list[Any]): One or multiple items

        Returns:
            list[Any]: One or multiple items stored as a list
        """
        if not isinstance(items, list):
            items = [items]

        return items

    def __validate_target_framework_compatibility(self, items: Any | list[Any]):
        """
        Recursively check all elements against the overall card version

        Args:
            items (Any): Items to be checked
        """
        # return if no items at all
        if not items:
            return

        items = CardValidator.__to_list(items)

        custom_types: list[Any] = []
        iterables: list[Any] = []

        for item in items:
            self.__item = item
            self.__validate_target_framework_model()

            for field in item.model_fields_set:
                field_name: str = field.__str__()

                value: Any = getattr(item, field_name)

                if value is None:
                    continue

                if isinstance(value, list):
                    iterables.append(value)
                    continue

                if isinstance(value, BaseModel):
                    custom_types.append(value)
                    continue

                metadata = item.model_fields[field_name].json_schema_extra
                self.__validate_field_version(
                    field_name, metadata.get(MINIMUM_VERSION_KEY)
                )
                self.__validate_target_framework_field(field_name)

        for iterable in iterables:
            self.__validate_target_framework_compatibility(iterable)

        for custom_type in custom_types:
            self.__validate_target_framework_compatibility(custom_type)

    @staticmethod
    def __calculate_card_size(card: AdaptiveCard) -> float:
        json_string: bytes = card.to_json().encode("utf-8")
        return len(json_string) / 1024

    def __validate_card_size(self) -> None:
        self.__card_size = CardValidator.__calculate_card_size(self.__card)
        if self.__card_size > self.__target_framework.max_card_size():
            self.__findings.append(
                Finding(
                    ValidationFailure.SIZE_LIMIT_EXCEEDED,
                    ValidationFailure.SIZE_LIMIT_EXCEEDED.value,
                    f"{self.__target_framework.name()} | {self.__target_framework.max_card_size()} KB",
                )
            )

    def __validate_target_framework_model(self) -> None:
        if not self.__item.model_json_schema().get("limited_to_target_platforms"):
            return

        if (
            self.__target_framework.NAME
            in self.__item.model_json_schema()["limited_to_target_platforms"]
        ):
            return

        self.__findings.append(
            Finding(
                ValidationFailure.ELEMENT_NOT_SUPPORTED_BY_TARGET_FRAMEWORK,
                ValidationFailure.ELEMENT_NOT_SUPPORTED_BY_TARGET_FRAMEWORK.value,
                f"Element not supported by the target framework: {type(self.__item).__name__}",
            )
        )

    def __validate_target_framework_field(self, field_name: str) -> None:
        if not self.__item.model_json_schema()[field_name].get(
            "limited_to_target_platforms"
        ):
            return

        if (
            self.__target_framework.NAME
            in self.__item.model_json_schema()[field_name][
                "limited_to_target_platforms"
            ]
        ):
            return

        self.__findings.append(
            Finding(
                ValidationFailure.FIELD_NOT_SUPPORTED_BY_TARGET_FRAMEWORK,
                ValidationFailure.FIELD_NOT_SUPPORTED_BY_TARGET_FRAMEWORK.value,
                f"Field not supported by the target framework: {type(self.__item).__name__}",
            )
        )

    def __validate_field_version(self, field_name: str, minimum_version: Any) -> None:
        assert minimum_version is not None

        if float(self.__card.version) < float(minimum_version):
            self.__findings.append(
                Finding(
                    ValidationFailure.INVALID_FIELD_VERSION,
                    ValidationFailure.INVALID_FIELD_VERSION.value,
                    f"Field version exceeds card version: {type(self.__item).__name__}"
                    f" | {field_name} | {minimum_version}",
                )
            )

    def __read_schema_file(self) -> dict[str, Any]:
        with open(
            Path(__file__)
            .parent.joinpath("schemas")
            .joinpath(f"schema-{self.__schema_version}.json"),
            "r",
            encoding="utf-8",
        ) as f:  # pylint: disable=C0103
            return json.load(f)

    def __validate_schema(self) -> None:
        schema: dict[str, Any] = self.__read_schema_file()
        try:
            Draft6Validator(schema).validate(instance=self.__card.to_dict())

        except SchemaValidationError as ex:
            self.__findings.append(
                Finding(
                    ValidationFailure.INVALID_SCHEMA,
                    ValidationFailure.INVALID_SCHEMA.value,
                    f"{ex.message}",
                )
            )

    def __debug(self):
        for finding in self.__findings:
            print(finding.message, finding.message_additional)
