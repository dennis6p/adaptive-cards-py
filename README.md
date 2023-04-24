# Adaptive Cards

A thin python wrapper for creating [**Adaptive Cards**](https://adaptivecards.io/) easily on code level. 
See here for the official and [**binding scheme**](https://adaptivecards.io/explorer/). 

**Please note:** This library is still in progress on not yet ready for real world usage. The code as well 
as the documentation are missing substantial parts. They are planned to be added soon. 


## About

This library is intended to provide a clear and simple interface for creating adaptive cards with only a few lines of code in a more robust way. The heavy usage of Python's typing library should
prevent one from creating invalid schemes and structures. Instead, creating cards should be intuitive and work like a breeze. 

## Requirements

* Python 3.10+
* `dataclasses-json`

## Usage

For a comprehensive introduction into the main ideas and patterns of adaptive cards, have a look on the [**official documentation**](https://docs.microsoft.com/en-us/adaptive-cards). I also recommend using the [**schema explorer**](https://adaptivecards.io/explorer) page alongside the implementation, since the library's type system relies on these schemes.

>  I recommend turning on the type check for python in your editor. This will provide you with all benefits of the implemented type annotations and yells at you, if you are trying to assign values of incompatible types.  

For instance, a simple `TextBlock` lives in the `element` module and can be used after it's import.

```python
from adaptive_cards.elements import TextBlock

text_block: TextBlock = TextBlock(text="Hello World")

```

An image can be created like this.

```python
from adaptive_cards.elements import Image

image: Image = Image(url="http://some-url.com")

```

For every **element**, **action**, **container** or **input** you can define, there are some required fields and some optional ones. Make sure to provide all required information. Again, have a look on the official documentation for an overview. 

Assuming we are done for now, we can create our first card. Let's put everything together. 

```python
version: str = "1.0"
card: AdaptiveCard = AdaptiveCard.new(version).body([element_1, element_2]).create()
```
After the building of the object is done, the `create(...)` method must be called in order to create the final object. In this case, the object will be of type `AdaptiveCard`.

Since the common format is `json`, the `AdaptiveCard` provides an `to_json()` method, 
which you can use to create a formatted string. 

```python
with open("<path/to/your/file.json>", "w") as f:
    f.write(card.to_json())
```

The card is ready to be used with any of the compatible apps (e.g. MS Teams) now. 
Please keep in mind, that not all features and versions are available for every platform.
[**Here**](https://learn.microsoft.com/en-us/adaptive-cards/resources/partners), you can find more information about it. 

## Examples

Have a look in the examples folder. 

## Roadmap

+ More complete valdidation
+ More and better examples
+ Documentation on code level
+ Ready to use Python package
