"""
This package provides small components for building adaptive cards compliant to 
the current interface definite with Python. 

[Schema Explorer](https://adaptivecards.io/explorer/)

This `__init__.py` file exposes key components of the package for easier access:

By importing the package, the following modulesare directly available:
    - [actions, card_types, card, client, containers, elements, inputs, utils, validation]

This module also initializes the package and ensures that any necessary 
configuration or setup is performed.
"""

from adaptive_cards.actions import *
from adaptive_cards.card_types import *
from adaptive_cards.card import *
from adaptive_cards.client import *
from adaptive_cards.containers import *
from adaptive_cards.elements import *
from adaptive_cards.inputs import *
from adaptive_cards.utils import *
from adaptive_cards.validation import *
