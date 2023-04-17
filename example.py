from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import TextBlock, Media, MediaSource, Image
from adaptive_cards.containers import Container, ContainerT, ColumnSet, Column, FactSet, Fact
import adaptive_cards.card_types as types
from adaptive_cards.actions import ActionToggleVisibility, TargetElement

# ------------ PR examples ------------ #

containers: list[ContainerT] = list()
containers.append(Container(
    items=[
        TextBlock(
            text="**Pull Requests**",
            size=types.FontSize.EXTRA_LARGE,
            style=types.TextBlockStyle.HEADING
        ),
    ],
    style=types.ContainerStyle.EMPHASIS
))

containers.append(Container(
    items=[
        TextBlock(
            text="**Some numbers for you**", 
            size=types.FontSize.MEDIUM, 
            separator=True
        ),
        ColumnSet(
            columns=[
                Column(
                    items=[
                        TextBlock(text="_Total_"),
                        TextBlock(text="_Created by your team_"),
                        TextBlock(text="_Created by other teams_"),
                        TextBlock(text="_Reviewed_"),
                        TextBlock(text="_Open_"),
                        TextBlock(text="_Approved_"),
                    ]
                ),
                Column(
                    items=[
                        TextBlock(text="5"),
                        TextBlock(text="4"),
                        TextBlock(text="3"),
                        TextBlock(text="6"),
                        TextBlock(text="1"),
                        TextBlock(text="1"),
                    ],
                    spacing=types.Spacing.MEDIUM,
                    rtl=True,
                ),
            ]
        ),
    ],
    separator=True,
))

containers.append(Container(
    items=[
        TextBlock(
            text="**Open Pull Requests**",
            size=types.FontSize.MEDIUM,
            style=types.TextBlockStyle.HEADING
        ),
    ],
    separator=True,
))

el = TextBlock(text="Hallo", id="element")

containers.append(Container(
    items=[
        ColumnSet(
            columns=[
                Column(items=[TextBlock(text="test1")]),
                Column(items=[TextBlock(text="test1")]),
                Column(
                    items=[
                        TextBlock(text="show"),
                        TextBlock(text="Hide")
                    ],
                    select_action=ActionToggleVisibility(
                        target_elements=[
                            TargetElement(
                                element_id="element",
                                is_visible=False,
                            ),
                            TargetElement(
                                element_id="show",
                                is_visible=False,
                            ),
                            TargetElement(
                                element_id="hide",
                                is_visible=False,
                            ),
                            
                        ],
                        
                    ),
                ),
            ]
        )
    ]
))


card = AdaptiveCard.new().add_items(containers).create()
  
with open("text.json", "w+") as f:
    f.write(card.to_json())

