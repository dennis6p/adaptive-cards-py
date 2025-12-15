"""Example: wrap-up card"""

# pylint: disable=C0413

import sys

from requests import Response

sys.path.append("../../")
from result import Result, is_ok

import adaptive_cards.types as types
from adaptive_cards.card import (
    ActionToggleVisibility,
    AdaptiveCard,
    Column,
    ColumnSet,
    Container,
    ContainerTypes,
    Image,
    TargetElement,
    TextBlock,
)
from adaptive_cards.client import TeamsClient
from adaptive_cards.validation import CardValidator, CardValidatorFactory

containers: list[ContainerTypes] = []

icon_source: str = "https://icons8.com/icon/vNXFqyQtOSbb/launch"
icon_url: str = "https://img.icons8.com/3d-fluency/94/launched-rocket.png"

header_column_set: ColumnSet = ColumnSet(
    columns=[
        Column(
            items=[
                TextBlock(text="Your Daily Wrap-Up", size=types.FontSize.EXTRA_LARGE)
            ],
            width="stretch",
        ),
        Column(items=[Image(url=icon_url, width="40px")], rtl=True, width="auto"),
    ]
)
containers.append(
    Container(
        items=[header_column_set], style=types.ContainerStyle.EMPHASIS, bleed=True
    )
)

containers.append(
    Container(
        items=[
            TextBlock(
                text="**Some numbers for you**",
                size=types.FontSize.MEDIUM,
            ),
            ColumnSet(
                columns=[
                    Column(
                        items=[
                            TextBlock(text="_Total_"),
                            TextBlock(text="_Done by you_"),
                            TextBlock(text="_Done by other teams_"),
                            TextBlock(text="_Still open_"),
                            TextBlock(text="_Closed_"),
                        ]
                    ),
                    Column(
                        items=[
                            TextBlock(text="5"),
                            TextBlock(text="4"),
                            TextBlock(text="3"),
                            TextBlock(text="6"),
                            TextBlock(text="1"),
                        ],
                        spacing=types.Spacing.MEDIUM,
                        rtl=True,
                    ),
                ],
                separator=True,
            ),
        ],
        spacing=types.Spacing.MEDIUM,
    )
)

containers.append(
    Container(
        items=[
            TextBlock(
                text="**Detailed Results**",
                size=types.FontSize.MEDIUM,
            ),
        ],
        separator=True,
        spacing=types.Spacing.EXTRA_LARGE,
    )
)

sample_column_set: ColumnSet = ColumnSet(
    columns=[
        Column(items=[TextBlock(text="12312")]),
        Column(items=[TextBlock(text="done", color=types.Colors.GOOD)]),
        Column(items=[TextBlock(text="abc")]),
        Column(
            items=[
                Image(
                    url="https://adaptivecards.io/content/down.png",
                    width="20px",
                    horizontal_alignment=types.HorizontalAlignment.RIGHT,
                )
            ],
            select_action=ActionToggleVisibility(
                title="More",
                target_elements=[
                    TargetElement(
                        element_id="toggle-me",
                    )
                ],
            ),
        ),
    ]
)

containers.append(
    Container(
        items=[
            Container(
                items=[
                    ColumnSet(
                        columns=[
                            Column(items=[TextBlock(text="**Number**")]),
                            Column(items=[TextBlock(text="**Status**")]),
                            Column(items=[TextBlock(text="**Topic**")]),
                            Column(items=[TextBlock(text="")]),
                        ],
                        id="headline",
                    ),
                ],
                style=types.ContainerStyle.EMPHASIS,
                bleed=True,
            ),
            Container(items=[sample_column_set]),
            Container(
                items=[
                    TextBlock(
                        text="_Here you gonna find more information about the whole topic_",
                        id="toggle-me",
                        is_visible=False,
                        is_subtle=True,
                        wrap=True,
                    )
                ]
            ),
        ],
    )
)

containers.append(
    Container(
        items=[
            TextBlock(
                text=f"Icon used from: {icon_source}",
                size=types.FontSize.SMALL,
                horizontal_alignment=types.HorizontalAlignment.CENTER,
                is_subtle=True,
            )
        ]
    )
)

# Build card
card = AdaptiveCard.new().version("1.5").add_items(containers).create()


# Validate card
card_validator: CardValidator = CardValidatorFactory.create_validator_microsoft_teams()
result: Result = card_validator.validate(card)

print(f"Validation was successful: {is_ok(result)}")

# send card
webhook_url: str = "YOUR-URL"
client: TeamsClient = TeamsClient(webhook_url)
response: Response = client.send(card)
