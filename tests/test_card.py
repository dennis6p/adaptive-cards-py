# test_math_operations.py
import sys
import inspect
import unittest
from adaptive_cards import *
from adaptive_cards import (
    AdaptiveCard,
    TextBlock,
    Image,
    TargetElement,
    ActionToggleVisibility,
    Container,
    ContainerTypes,
    ColumnSet,
    Column,
)
import json
from typing import Any
from pathlib import Path
from enum import EnumMeta

import adaptive_cards.card_types as types


class TestAdaptiveCard(unittest.TestCase):

    def setUp(self):
        with open(
            Path(__file__).parent.joinpath("test_card.json"), "r+", encoding="utf-8"
        ) as f:
            self.test_card: dict[str, Any] = json.load(f)

    def tearDown(self):
        del self.test_card

    def test_create(self):
        """Run test for simple card"""

        containers: list[ContainerTypes] = []

        icon_source: str = "https://icons8.com/icon/vNXFqyQtOSbb/launch"
        icon_url: str = "https://img.icons8.com/3d-fluency/94/launched-rocket.png"

        header_column_set: ColumnSet = ColumnSet(
            columns=[
                Column(
                    items=[
                        TextBlock(
                            text="Your Daily Wrap-Up", size=types.FontSize.EXTRA_LARGE
                        )
                    ],
                    width="stretch",
                ),
                Column(
                    items=[Image(url=icon_url, width="40px")], rtl=True, width="auto"
                ),
            ]
        )
        containers.append(
            Container(
                items=[header_column_set],
                style=types.ContainerStyle.EMPHASIS,
                bleed=True,
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

        with open("schema-1.1.0.json", "r+") as f:
            schema = json.load(f)

        from copy import deepcopy

        schema_iter = deepcopy(schema)
        for name, definition in schema_iter.get("definitions").items():

            new_name: str = name.replace(".", "")
            schema["definitions"][new_name] = definition
            del schema["definitions"][name]

            # schema["definitions"][name.replace(".", "")] = definition
            # del schema["definitions"][name]

        for module in [
            "actions",
            "card_types",
            "card",
            "containers",
            "elements",
            "inputs",
        ]:
            for name, obj in inspect.getmembers(
                sys.modules[f"adaptive_cards.{module}"]
            ):
                if inspect.getmodule(obj) is None:
                    continue
                if "adaptive_cards" not in inspect.getmodule(obj).__name__:
                    continue

                if not inspect.isclass(obj):
                    continue

                if inspect.isclass(obj) and isinstance(obj, EnumMeta):
                    # Is enum object
                    continue

                properties = obj.__dict__

                print(name, schema.get("definitions").get(name))

                # print(name, properties)

        # print(card.to_dict())

        # self.assertEqual(json.loads(card.to_json()), self.test_card)


if __name__ == "__main__":
    unittest.main()
