"""Example: simple card"""
from adaptive_cards.elements import TextBlock
import adaptive_cards.card_types as types
from adaptive_cards.card import AdaptiveCard

text_block: TextBlock = TextBlock(
    text="It's your second card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

version: str = "1.4"
card: AdaptiveCard = AdaptiveCard.new().version(version).add_item(text_block).create()
output = card.to_json()
print(output)
