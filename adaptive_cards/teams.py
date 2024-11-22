"""Implementations for MS Teams specific properties"""

from dataclasses import dataclass, field
from typing import Optional
from dataclasses_json import LetterCase, dataclass_json
from adaptive_cards import utils
from adaptive_cards.card_types import MSTeamsCardWidth


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(kw_only=True)
class MSTeams:
    """
    Represents specific properties for MS Teams as the target framework.

    Attributes:
        width: The total horizontal space an adaptive cards is allowed to occupy
               when posted to MS Teams. Defaults to "None".
    """

    width: Optional[MSTeamsCardWidth] = field(
        default=MSTeamsCardWidth.DEFAULT, metadata=utils.get_metadata("1.0")
    )
