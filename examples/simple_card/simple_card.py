"""Example: simple card"""

from requests import Response
from adaptive_cards.elements import TextBlock
import adaptive_cards.card_types as types
from adaptive_cards.card import AdaptiveCard
from adaptive_cards.validation import SchemaValidator, Result
from adaptive_cards.client import TeamsClient


text_block: TextBlock = TextBlock(
    text="It's your second card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

# build card
version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new().version(version).add_item(text_block).create()

# validate card
validator: SchemaValidator = SchemaValidator()
result: Result = validator.validate(card)

print(f"Validation was successful: {result == Result.SUCCESS}")

# send card
webhook_url: str = "YOUR-URL"
client: TeamsClient = TeamsClient(webhook_url)
response: Response = client.send(card)
