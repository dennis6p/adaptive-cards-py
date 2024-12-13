# Adaptive Cards <!-- omit in toc -->

- [About](#about)
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Library structure](#library-structure)
- [Usage](#usage)
  - [A simple card](#a-simple-card)
  - [Adding multiple elements at once](#adding-multiple-elements-at-once)
  - [A more complex card](#a-more-complex-card)
  - [Validate schema](#validate-schema)
  - [Send card to MS Teams](#send-card-to-ms-teams)
- [Examples](#examples)
- [Feature Roadmap](#feature-roadmap)
- [Contribution](#contribution)

[![PyPI version](https://badge.fury.io/py/adaptive-cards-py.svg)](https://pypi.org/project/adaptive-cards-py/)

A thin Python wrapper for creating [**Adaptive Cards**](https://adaptivecards.io/) easily on code level. The deep integration of Python's `typing` package prevents you from creating invalid schemas and guides you while setting up the code for generating visual appealing cards.

If you are interested in the general concepts of adaptive cards and want to dig a bit deeper, have a look into the [**official documentation**](https://learn.microsoft.com/en-us/adaptive-cards/) or get used to the [**schema**](https://adaptivecards.io/explorer/) first.

💡 **Please note**
<br>This library is work in progress. Missing parts are planned to be added from time to time.

## About

This library is intended to provide a clear and simple interface for creating adaptive cards with only a few lines of code in a more robust way. The heavy usage of Python's `typing` library should prevent one from creating invalid schemes and structures. Instead, creating and sending cards should be intuitive and be supported by the typing system.

For a comprehensive introduction into the main ideas and patterns of adaptive cards, head over to the [**official documentation**](https://docs.microsoft.com/en-us/adaptive-cards). I also recommend using the [**schema explorer**](https://adaptivecards.io/explorer) page alongside the implementation, since the library's type system relies on these schemas.

Further resources can be found here:

* [__Format cards in Teams__](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cdesktop%2Cdesktop1%2Cdesktop2%2Cconnector-html)
* [__Official repository__](https://github.com/microsoft/AdaptiveCards)

💡 **Please note**
<br> There are size limitations related to the [__target framework__](https://learn.microsoft.com/en-us/adaptive-cards/resources/partners#live) (or "__Host__") a card is supposed to be used with. As of now, the maximum card size can be __28KB__ when used with Webhooks in Teams ([__Format cards in Teams__](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cdesktop%2Cdesktop1%2Cdesktop2%2Cconnector-html)). For bot frameworks the upper limit is set to __40KB__ ([__Format your bot messages__](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/format-your-bot-messages)). An corresponding check is planned to be added soon to the [`SchemaValidator`](#validate-schema).

## Features

💡 **Please note**
<br>It's highly recommended to turn on the **type check** capabilities for Python in your editor. This will serve you with direct feedback about the structures you create. If you are trying to assign values of incompatible types, your editor will mark it as such and yell at you right in the moment you are about to do so. Otherwise, invalid schemas can be detected by making use of the card validation, 
once the card has been successfully created.

+ Type annotated components based on Python's **dataclasses**
+ Schema validation for version compatibility
+ Simple `JSON` export
+ Compliant with the official structures and ideas
+ Send cards to MS Teams via `TeamsClient`

## Dependencies

* Python 3.10+
* `dataclasses-json`
* `requests`

## Installation

```bash
pip install adaptive-cards-py
```

## Library structure

**Adaptive cards** can consist of different kinds of components. The four main categories beside the actual cards are **Elements**, **Containers**, **Actions** and **Inputs**. You can find all available components for each category within the corresponding module. The `AdaptiveCard` is defined in the `cards` module.

In addition to that, some fields of certain components are of custom types. These types are living inside the `card_types` mpdule. For instance, if you are about to assign a color to a `TextBlock`, the field `color` will only accept a value of type `Colors`, which is implemented in the aforementioned Python file.

To perform validation on a fully initialized card, one can make use of the `CardValidator` class (`validation` module). Similar to the whole library, this class provides a simple interface. For creating a validator, a Factory (`CardValidatorFactory`) can be used, in order to account for the desired target framework. Validation will check the following points:


* Are any components used, which are not yet available for the card version?
* Is the card size within the limitation defined by the target framework?
* Does the schema correspond to the official card schema?
* Are there any components in the card body at all?

## Usage

### A simple card

A simple `TextBlock` lives in the `elements` module and can be used after it's import.

```Python
from adaptive_cards.elements import TextBlock

text_block: TextBlock = TextBlock(text="It's your first card")
```
For this component, `text` is the only required property. However, if more customization is needed, further available fields can be used.

```Python
from adaptive_cards.elements import TextBlock
import adaptive_cards.card_types as types

text_block: TextBlock = TextBlock(
    text="It's your second card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)
```

An actual card with only this component can be created like this.

```Python
from adaptive_cards.card import AdaptiveCard

...

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new() \
                                 .version(version) \
                                 .add_item(text_block) \
                                 .create()
```

Find your final layout below.

![simple card](https://github.com/dennis6p/adaptive-cards-py/blob/main/examples/simple_card/simple_card.jpg?raw=true)

💡 **Please note**
<br>After building the object is done, the `create(...)` method must be called in order to create the final object. In this case, the object will be of type `AdaptiveCard`.

To directly export your result, make use of the
`to_json()` method provided by every card.

```Python
with open("path/to/out/file.json", "w+") as f:
    f.write(card.to_json())

```

### Adding multiple elements at once

Assuming you have a bunch of elements you want your card to enrich with. There is also a method for doing so. Let's re-use the example from before, but add another `Image` element here as well.

```Python
from adaptive_cards.elements import TextBlock, Image
import adaptive_cards.card_types as types

text_block: TextBlock = TextBlock(
    text="It's your third card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

image: Image = Image(url="https://adaptivecards.io/content/bf-logo.png")

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new() \
                                 .version(version) \
                                 .add_items([text_block, image]) \
                                 .create()

# Alternatively, you can also chain multiple add_item(...) functions:
# card = AdaptiveCard.new() \
#                    .version(version) \
#                    .add_item(text_block) \
#                    .add_item(image) \
#                    .create()


with open("path/to/out/file.json", "w+") as f:
    f.write(card.to_json())
```

This will result in a card like shown below.

![simple card 2](https://github.com/dennis6p/adaptive-cards-py/blob/main/examples/simple_card/simple_card_2.jpg?raw=true)

### A more complex card

You can have a look on the following example for getting an idea of what's actually possible with adaptive cards.

![wrap up card](https://github.com/dennis6p/adaptive-cards-py/blob/main/examples/wrap_up_card/wrap_up_card.jpg?raw=true)

<details>
<summary>Code</summary>

```python
import adaptive_cards.card_types as types
from adaptive_cards.actions import ActionToggleVisibility, TargetElement
from adaptive_cards.validation import SchemaValidator, Result
from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import TextBlock, Image
from adaptive_cards.containers import Container, ContainerTypes, ColumnSet, Column

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

card = AdaptiveCard.new().version("1.5").add_items(containers).create()

validator: SchemaValidator = SchemaValidator()
result: Result = validator.validate(card)

print(f"Validation was successful: {result == Result.SUCCESS}")

```

</details>

<details>
<summary>Schema</summary>

```json
{
    "type": "AdaptiveCard",
    "version": "1.5",
    "schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "body": [
        {
            "items": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "items": [
                                {
                                    "text": "Your Daily Wrap-Up",
                                    "type": "TextBlock",
                                    "size": "extraLarge"
                                }
                            ],
                            "width": "stretch"
                        },
                        {
                            "items": [
                                {
                                    "url": "https://img.icons8.com/3d-fluency/94/launched-rocket.png",
                                    "type": "Image",
                                    "width": "40px"
                                }
                            ],
                            "rtl": true,
                            "width": "auto"
                        }
                    ]
                }
            ],
            "type": "Container",
            "style": "emphasis",
            "bleed": true
        },
        {
            "spacing": "medium",
            "items": [
                {
                    "text": "**Some numbers for you**",
                    "type": "TextBlock",
                    "size": "medium"
                },
                {
                    "separator": true,
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "items": [
                                {
                                    "text": "_Total_",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "_Done by you_",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "_Done by other teams_",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "_Still open_",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "_Closed_",
                                    "type": "TextBlock"
                                }
                            ]
                        },
                        {
                            "spacing": "medium",
                            "items": [
                                {
                                    "text": "5",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "4",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "3",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "6",
                                    "type": "TextBlock"
                                },
                                {
                                    "text": "1",
                                    "type": "TextBlock"
                                }
                            ],
                            "rtl": true
                        }
                    ]
                }
            ],
            "type": "Container"
        },
        {
            "separator": true,
            "spacing": "extraLarge",
            "items": [
                {
                    "text": "**Detailed Results**",
                    "type": "TextBlock",
                    "size": "medium"
                }
            ],
            "type": "Container"
        },
        {
            "items": [
                {
                    "items": [
                        {
                            "id": "headline",
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "items": [
                                        {
                                            "text": "**Number**",
                                            "type": "TextBlock"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "text": "**Status**",
                                            "type": "TextBlock"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "text": "**Topic**",
                                            "type": "TextBlock"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "text": "",
                                            "type": "TextBlock"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "type": "Container",
                    "style": "emphasis",
                    "bleed": true
                },
                {
                    "items": [
                        {
                            "type": "ColumnSet",
                            "columns": [
                                {
                                    "items": [
                                        {
                                            "text": "12312",
                                            "type": "TextBlock"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "text": "done",
                                            "type": "TextBlock",
                                            "color": "good"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "text": "abc",
                                            "type": "TextBlock"
                                        }
                                    ]
                                },
                                {
                                    "items": [
                                        {
                                            "url": "https://adaptivecards.io/content/down.png",
                                            "type": "Image",
                                            "horizontalAlignment": "right",
                                            "width": "20px"
                                        }
                                    ],
                                    "selectAction": {
                                        "title": "More",
                                        "targetElements": [
                                            {
                                                "elementId": "toggle-me"
                                            }
                                        ],
                                        "type": "Action.ToggleVisibility"
                                    }
                                }
                            ]
                        }
                    ],
                    "type": "Container"
                },
                {
                    "items": [
                        {
                            "id": "toggle-me",
                            "isVisible": false,
                            "text": "_Here you gonna find more information about the whole topic_",
                            "type": "TextBlock",
                            "isSubtle": true,
                            "wrap": true
                        }
                    ],
                    "type": "Container"
                }
            ],
            "type": "Container"
        },
        {
            "items": [
                {
                    "text": "Icon used from: https://icons8.com/icon/vNXFqyQtOSbb/launch",
                    "type": "TextBlock",
                    "horizontalAlignment": "center",
                    "isSubtle": true,
                    "size": "small"
                }
            ],
            "type": "Container"
        }
    ]
}
```

</details>

### Validate schema

New components and fields are getting introduced every now and then. This means, if you are using an early version for a card and add fields, which are not compliant with it, you will have an invalid schema. To prevent you from exporting fields not yet supported by the card and target framework, a card validation can be performed for the expected [__target framework__](https://learn.microsoft.com/en-us/adaptive-cards/resources/partners#live) (see [__Library structure__](#library-structure) for more info). For MS Teams as the target framework, it would like like this:

```python
from adaptive_cards.validator import (
    CardValidatorFactory, 
    CardValidator, 
    Result, 
    Finding
)

...

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new() \
                                 .version(version) \
                                 .add_items([text_block, image]) \
                                 .create()

# generate a validator object for your required target framework
validator: CardValidator = CardValidatorFactory.create_validator_microsoft_teams()
result: Result = validator.validate(card)

print(f"Validation was successful: {result == Result.SUCCESS}")

# As it might come in handy in some situations, there is a separate class method
# which can be utilized to calculate the card size without running the full
# validation procedure
card_size: float = validator.card_size(card)
print(card_size)

# in case the validation failed, you can check the validation details by using the according method, 
# to get a full list of all findings occurred during validation.
details: list[Finding] = validator.details()

# please note, that the validation details are stored within the validator and will be overwritten,
# once a new validator.validation(card) execution is done with the same validator object. 

```

### Send card to MS Teams

Of course, you want to create those cards for a reason. So once you did that, you might want to send it to one of the compatible services like MS Teams. See the following example, how this can be done, assuming that all previously mentioned steps are done prior to that:

```python

...

from adaptive_cards.clients import TeamsClient
from requests import Response

...

# send card
webhook_url: str = "YOUR-URL"
client: TeamsClient = TeamsClient(webhook_url)
response: Response = client.send(card)

new_webhook_url: str = "YOUR-URL-OF-SECOND-CHANNEL"
client.set_webhook_url(new_webhook_url)
response: Response = client.send(card)

...

```

So far, there is only a MS Teams client available. If further services should be supported, give me some feedback by opening an Issue for instance.

Find further information about sending cards or creating Webhooks to/in MS Teams [__here__](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498).

## Examples

If you are interested in more comprehensive examples or the actual source code, have a look into the `examples` folder.

## Feature Roadmap

* [x] Add size check to schema validation
* [x] Add proper schema validation
* [x] Add further target framework validators
* [ ] Provide more examples
* [ ] Allow reading of json-like schemas

## Contribution

Feel free to create issues, fork the repository or even come up with a pull request. I am happy about any kind of contribution and would love
to hear your feedback!
