from typing import Literal
from abc import ABC

SchemaVersion = Literal["1.0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]


class AbstractTargetFramework(ABC):
    """
    Abstract interface representing the AbstractTargetFramework cards can be send to
    """

    NAME: str

    def __init__(self, max_card_size_kb: float, schema_version: SchemaVersion) -> None:
        self.__max_card_size_kb: float = max_card_size_kb
        self.__schema_version: SchemaVersion = schema_version

    def name(self) -> str:
        """
        Return name of target framework

        Returns:
            str: Name of target framework
        """
        return self.NAME

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

    NAME: str = "BotWebChat"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.5"
        super().__init__(max_card_size_kb, schema_version)


class Outlook(AbstractTargetFramework):
    """Outlook target framework"""

    NAME: str = "Outlook"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(max_card_size_kb, schema_version)


class MicrosoftTeams(AbstractTargetFramework):
    """MicrosoftTeams target framework"""

    NAME: str = "Microsoft Teams"

    def __init__(self):
        """"""
        max_card_size_kb: float = 28
        schema_version: SchemaVersion = "1.5"
        super().__init__(max_card_size_kb, schema_version)


class CortanaSkills(AbstractTargetFramework):
    """Cortana Skills target framework"""

    NAME: str = "Cortana Skills"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(max_card_size_kb, schema_version)


class WindowsTimeline(AbstractTargetFramework):
    """Windows Timeline target framework"""

    NAME: str = "Windows Timeline"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.0"
        super().__init__(max_card_size_kb, schema_version)


class CiscoWebExTeams(AbstractTargetFramework):
    """Cisco WebEx Teams target framework"""

    NAME: str = "Cisco WebEx Teams"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.2"
        super().__init__(max_card_size_kb, schema_version)


class VivaConnections(AbstractTargetFramework):
    """Viva Connections target framework"""

    NAME: str = "Viva Connections"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.2"
        super().__init__(max_card_size_kb, schema_version)


class WindowsWidgets(AbstractTargetFramework):
    """Windows Widgets target framework"""

    NAME: str = "WindowsWidgets"

    def __init__(self):
        """"""
        max_card_size_kb: float = 40
        schema_version: SchemaVersion = "1.6"
        super().__init__(max_card_size_kb, schema_version)
