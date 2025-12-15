"""Example: simple card"""

from requests import Response
from result import Result, is_ok

import adaptive_cards.types as types
from adaptive_cards.card import AdaptiveCard, TextBlock
from adaptive_cards.client import TeamsClient
from adaptive_cards.validation import CardValidator, CardValidatorFactory

text_block: TextBlock = TextBlock(
    text="It's your second card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

# build card
version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new().add_item(text_block).create()

# validate card
validator: CardValidator = CardValidatorFactory.create_validator_microsoft_teams()
result: Result = validator.validate(card)

print(f"Validation was successful: {is_ok(result)}")

# send card
webhook_url: str = "YOUR-URL"
client: TeamsClient = TeamsClient(webhook_url)
response: Response = client.send(card)
