# Adaptive Cards

A thin python wrapper for creating [**Adaptive Cards**](https://adaptivecards.io/) easily on code level. 
See here for the official and [**binding scheme**](https://adaptivecards.io/explorer/). 


## About

This library is intended to provide a clear and simple interface for creating adaptive cards with only a few lines of code in a more robust way. The heavy usage of Python's typing library should
prevent one from creating invalid schemes and structures. Instead, creating cards should be intuitive and work like a breeze. 

Therefore, the implementation is following the builder pattern. Each Element, Container, Card, etc. is owner of a `new(...)` method, which can be used for creating an actual `Builder` object and must be called with values for all required fields. A builder contains all type-specific methods for creating and manipulating the target object. See below a simple example:

```python
version: str = "1.0"
card: AdaptiveCard = AdaptiveCard.new(version).body([element_1, element_2]).create()
```
After the building of the object is done, the `create(...)` method must be called in order to create the final object. In this case, the object will be of type `AdaptiveCard`.

