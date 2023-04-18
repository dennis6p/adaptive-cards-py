from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import TextBlock, Image
from adaptive_cards.containers import Container, ContainerT, ColumnSet, Column
import adaptive_cards.card_types as types
from adaptive_cards.actions import ActionToggleVisibility, TargetElement

# ------------ PR examples ------------ #

containers: list[ContainerT] = list()
containers.append(
    Container(
        items=[
            TextBlock(
                text="**Results**",
                size=types.FontSize.EXTRA_LARGE,
                horizontal_alignment=types.HorizontalAlignment.CENTER
            ),
        ],
        style=types.ContainerStyle.EMPHASIS,
        bleed=True
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
                    )
                ],
                separator=True
            ),
        ],
        spacing=types.Spacing.MEDIUM
    )
)

containers.append(Container(
    items=[
        TextBlock(
            text="**Detailed Results**",
            size=types.FontSize.MEDIUM,
        ),
    ],
    separator=True,
    spacing=types.Spacing.EXTRA_LARGE
))

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
                        id="headline"
                    ),       
                ],
                style=types.ContainerStyle.EMPHASIS,
                bleed=True,
            ),
            Container(
                items=[
                    ColumnSet(
                        columns=[
                            Column(items=[TextBlock(text="12312")]),
                            Column(items=[TextBlock(text="done", color=types.Colors.GOOD)]),
                            Column(items=[TextBlock(text="abc")]),
                            Column(
                                items=[
                                    Image(
                                        url="https://adaptivecards.io/content/down.png", 
                                        width="20px",
                                        horizontal_alignment=types.HorizontalAlignment.RIGHT
                                    )
                                ],
                                select_action=ActionToggleVisibility(
                                    title="More",
                                    target_elements=[
                                        TargetElement(
                                            element_id="toggle-me",
                                        )
                                    ],
                                    
                                )
                            ),
                        ]
                    ),       
                ]
            ),
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
            )
        ],
    )
)


card = AdaptiveCard.new().version("1.4").add_items(containers).create()
  
with open("examples/tasks.json", "w+") as f:
    f.write(card.to_json())

