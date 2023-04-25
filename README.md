# Adaptive Cards

A thin Python wrapper for creating [**Adaptive Cards**](https://adaptivecards.io/) easily on code level. The deep integration of Python's `typing` package prevents you from creating invalid schemes and guides you while creating visual apealing cards. 

If you are interested in the general concepts of adaptive cards and want to dig a bit deeper, have a look into the [**official documentation**](https://learn.microsoft.com/en-us/adaptive-cards/) or start a jump start and get used to the [**schema**](https://adaptivecards.io/explorer/).

💡 **Please note**
<br>This library is still in progress and is lacking some features. However, missing fractions are planned to be added soon. 

## About

This library is intended to provide a clear and simple interface for creating adaptive cards with only a few lines of code in a more robust way. The heavy usage of Python's typing library should
prevent one from creating invalid schemes and structures. Instead, creating cards should be intuitive and work like a breeze. 

For a comprehensive introduction into the main ideas and patterns of adaptive cards, have a look on the [**official documentation**](https://docs.microsoft.com/en-us/adaptive-cards). I also recommend using the [**schema explorer**](https://adaptivecards.io/explorer) page alongside the implementation, since the library's type system relies on these schemes.

💡 **Please note**
<br>It's highly recommended to turn on the **type check** capabilities for Python in your editor. This will serve you with direct feedback about the structures you create. If you are trying to assign values of incompatible types, your editor will mark it as such and yells at you right in the moment you are about to do so.

## Features

+ Type annotated components based on Python's **dataclasses**
+ Schema validation for version compatibility
+ Simple `JSON` export
+ Compliant with the official structures and ideas

## Requirements

* Python 3.10+
* `dataclasses-json`

## Library structure

**Adaptive cards** can consist of different kind of components. The four main categories beside the actual cards are **Elements**, **Containers**, **Actions** and **Inputs**. You can find all available components for each category within the corresponding file. The `AdaptiveCard` is defined in `cards.py`.

In addition to that, some fields of certain components are of custom types. These types are living inside the `card_types.py` file. For instance, if you are about to assign a color to a `TextBlock`, the field `color` will only accept a value of type `Colors`, which is implemented in the aforementioned Python file.

To perform validation on a fully initialized card, one can make use of the `SchemaValidator` class. Similar to the whole library, this class provides a simple interface with only on method. The validation currently checks whether all used fields are compliant with the overall card version

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
    text="It's your second card"
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
card: AdaptiveCard = AdaptiveCard.new(version) \
                                 .add_item(text_block) \
                                 .create()
```

Find your final layout below.

![simple card](examples/simple_card/simple_card.jpg)

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
    text="It's your third card"
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

image: Image = Image(url="https://adaptivecards.io/content/bf-logo.png")

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new(version) \
                                 .add_items([text_block, image]) \
                                 .create()

# Alternatively, you can also chain multiple add_item(...) functions:
# card = AdaptiveCard.new(version) \
#                    .add_item(text_block) \
#                    .add_item(image) \
#                    .create()


with open("path/to/out/file.json", "w+") as f:
    f.write(card.to_json())
```

This will result in a card like shown below.

![simple card](examples/simple_card/simple_card_2.jpg)

### Validate schema

New components and fields are getting introduced every now and then. This means, if you are using an early version for a card and add fields, which are not compliant with it, you will have an invalid schema. To prevent you from exporting fields not yet supported by the card and target framework, a schema validation can be performed. It's as simple as that:

```Python
from adaptive_cards.validator import SchemaValidator, Result

...

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new(version) \
                                 .add_items([text_block, image]) \
                                 .create()

validator: SchemaValidator = SchemaValidator()
result: Result = validator.validate(card)

print(f"Validation was successful: {result == Result.SUCCESS}")

```

## Examples

If you are interested in more comprehensive examples, have a look into the `examples` folder (coming soon!) or visit the samples page of the official documentation. 

## Roadmap

+ 🔎 More complete valdidation
+ 🚀 Better examples
+ 📕 Comprehensive documentation on code level
+ 🐍 Ready to use Python package
