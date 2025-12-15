"""Example: simple card"""

from result import Result, is_ok

import adaptive_cards.types as types
from adaptive_cards.card import ActionOpenUrl, AdaptiveCard, TextBlock

text_block: TextBlock = TextBlock(
    id="text-id",
    text="Initial text",
)

action_open_url: ActionOpenUrl = ActionOpenUrl(
    id="action-id", url="any-url", title="title"
)

# build card
version: str = "1.4"
card: AdaptiveCard = (
    AdaptiveCard.new().add_item(text_block).add_action(action_open_url).create()
)

# update card item
update_result: Result[None, str] = card.update_item(
    id="text-id",
    text="New text",
    horizontal_alignment=types.HorizontalAlignment.CENTER,
    font_type=types.FontType.MONOSPACE,
)
assert is_ok(update_result)
print(card)

# update card action
update_result = card.update_action(id="action-id", url="new-url")
assert is_ok(update_result)
print(card)
