<<<<<<< HEAD
# adaptive-cards
An user-friendly python library for building adaptive cards on code level following the builder pattern
=======
# Adaptive Cards

A thin python wrapper for creating [**Adaptive Cards**](https://adaptivecards.io/) easily on code level. 
See here for the official and [**binding scheme**](https://adaptivecards.io/explorer/). 


## About

This library is intended to provide a clear and simple type interface for creating adaptive cards in a more robust way. The heavy usage of Python's `typing` library should prevent one from creating invalid schemes and structures. Instead, creating cards should be intuitive and work like a breeze. 

## Requirements

* Python 3.10+
* `dataclass_json`

## Usage

For a comprehensive introduction into the main ideas and patterns of adaptive cards, have a look on the [**official documentation**](https://docs.microsoft.com/en-us/adaptive-cards). I also recommend using the [**schema expolorer**](https://adaptivecards.io/explorer) page alongside the implementation, since the library's type system relies on these schemes.

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
card: AdaptiveCard = AdaptiveCard.new(version).add_item(text_box).add_item(image).create()
```
After the building of the object is done, the `create(...)` method must be called in order to create the final object. In this case, the object will be of type `AdaptiveCard`.

>>>>>>> 8fcbdc8... further implementation
