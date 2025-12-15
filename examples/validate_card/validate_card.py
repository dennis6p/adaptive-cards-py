from result import Result, is_ok

import adaptive_cards.types as types
from adaptive_cards.card import AdaptiveCard, TextBlock
from adaptive_cards.validation import CardValidator, CardValidatorFactory, Finding

text_block: TextBlock = TextBlock(
    text="It's your second card",
    color=types.Colors.ACCENT,
    size=types.FontSize.EXTRA_LARGE,
    horizontal_alignment=types.HorizontalAlignment.CENTER,
)

version: str = "1.4"
card: AdaptiveCard = (
    AdaptiveCard.new().version(version).add_items([text_block]).create()
)

validator: CardValidator = CardValidatorFactory.create_validator_microsoft_teams()
result: Result[None, str] = validator.validate(card)

print(f"Validation was successful: {is_ok(result)}")

card_size: float = validator.card_size(card)
print(card_size)

details: list[Finding] = validator.details()
assert len(details) == 0
