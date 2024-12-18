"""Validation class for evaluating a cards schema"""

import dataclasses
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum, Flag
from pathlib import Path
from typing import Any, Literal

from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft6Validator

from adaptive_cards.card import AdaptiveCard

MINIMUM_VERSION_KEY: str = "min_version"

SchemaVersion = Literal["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]


class Result(Flag):
    """
    Represents the overall validation result value as a combination of flags.
    """

    SUCCESS = 0
    """validation successful"""

    FAILURE = 1
    """validation failed"""


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


class AbstractTargetFramework(ABC):
    """
    Abstract interface representing the AbstractTargetFramework cards can be send to
    """

    def __init__(
        self, name: str, max_card_size_kb: float, schema_version: SchemaVersion
    ) -> None:
        self.__name: str = name
        self.__max_card_size_kb: float = max_card_size_kb
        self.__schema_version: SchemaVersion = schema_version

    def name(self) -> str:
        """
        Return name of target framework

        Returns:
            str: Name of target framework
        """
        return self.__name

    def max_card_size(self) -> float:
        """
        Calculate the maximum allowed card size for the target framework

        Returns:
            float: maximum card size
        """
        return self.__max_card_size_kb

    def schema_version(self) -> SchemaVersion:
        """
        Schema version the card is validated against

        Returns:
            float: schema version
        """
        return self.__schema_version


class BotWebChat(AbstractTargetFramework):
    """Bot WebChat target framework"""

    def __init__(self):
        """"""
        name: str = "BotWebChat"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.5"
        super().__init__(name, max_card_size_kb, schema_version)


class Outlook(AbstractTargetFramework):
    """Outlook target framework"""

    def __init__(self):
        """"""
        name: str = "Outlook"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(name, max_card_size_kb, schema_version)


class MicrosoftTeams(AbstractTargetFramework):
    """MicrosoftTeams target framework"""

    def __init__(self):
        """"""
        name: str = "Microsoft Teams"
        max_card_size_kb: float = 28
        schema_version: SchemaVersion = "1.5"
        super().__init__(name, max_card_size_kb, schema_version)


class CortanaSkills(AbstractTargetFramework):
    """Cortana Skills target framework"""

    def __init__(self):
        """"""
        name: str = "Cortana Skills"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(name, max_card_size_kb, schema_version)


class WindowsTimeline(AbstractTargetFramework):
    """Windows Timeline target framework"""

    def __init__(self):
        """"""
        name: str = "Windows Timeline"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(name, max_card_size_kb, schema_version)


class CiscoWebExTeams(AbstractTargetFramework):
    """Cisco WebEx Teams target framework"""

    def __init__(self):
        """"""
        name: str = "Cisco WebEx Teams"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.2"
        super().__init__(name, max_card_size_kb, schema_version)


class VivaConnections(AbstractTargetFramework):
    """Viva Connections target framework"""

    def __init__(self):
        """"""
        name: str = "Viva Connections"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.2"
        super().__init__(name, max_card_size_kb, schema_version)


class WindowsWidgets(AbstractTargetFramework):
    """Windows Widgets target framework"""

    def __init__(self):
        """"""
        name: str = "WindowsWidgets"
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.6"
        super().__init__(name, max_card_size_kb, schema_version)


class CardValidatorAbstractFactory(ABC):
    """Abstract card validator factory"""

    def __init__(self):
        pass

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


@dataclass
class Finding:
    """
    Class for storing an individual finding during schema validation
    """

    failure: ValidationFailure
    """Validation failure"""

    message: str
    """Corresponding failure message"""

    message_additional: str = ""
    """Addition information"""


class AbstractCardValidator(ABC):
    """
    Abstract interface for card validators
    """

    def __init__(self):
        pass

    @abstractmethod
    def validate(self, card: AdaptiveCard, debug: bool = True) -> Result:
        """
        Run validation on card.

        Args:
            card (AdaptiveCard): Card to be validated

        Returns:
            Result: Validation result
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

    def validate(self, card: AdaptiveCard, debug: bool = True) -> Result:
        self.__card = card
        self.__reset()
        self.__validate_card()

        if debug:
            self.__debug()

        return Result.SUCCESS if len(self.__findings) == 0 else Result.FAILURE

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
        self.__validate_version_for_elements(self.__card.body)

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

    def __validate_version_for_elements(self, items: Any | list[Any]):
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
            for field in fields(item):
                value: Any = getattr(item, field.name)

                if value is None:
                    continue

                if isinstance(value, list):
                    iterables.append(value)
                    continue

                if dataclasses.is_dataclass(value):
                    custom_types.append(value)
                    continue

                self.__validate_field_version(
                    field.name, field.metadata.get(MINIMUM_VERSION_KEY)
                )

        for iterable in iterables:
            self.__validate_version_for_elements(iterable)

        for custom_type in custom_types:
            self.__validate_version_for_elements(custom_type)

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
                    f"{self.__target_framework.name()} | "
                    f"{self.__target_framework.max_card_size()} KB",
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
            Draft6Validator(schema).validate(json.loads(self.__card.to_json()))

        except ValidationError as ex:
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
