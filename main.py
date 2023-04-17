from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import TextBlock, Media, MediaSource, Image
from adaptive_cards.containers import Container, ColumnSet, Column, FactSet, Fact
from adaptive_cards.card_types import *
from adaptive_cards.actions import ActionOpenUrl

url: str = "https://www.youtube.com/hashtag/werkstatteinrichten"
action_open_url: ActionOpenUrl = ActionOpenUrl(
    title="This is just a test", url=url
)

text_block_1 = TextBlock(
    text="This is just a test",
    font_type=FontType.MONOSPACE
)

image = Media(
    sources=[
        MediaSource(url=url),
        MediaSource(url="http://google.com")
    ]
)

card = AdaptiveCard.new() \
                   .add_item(text_block_1) \
                   .add_item(image) \
                   .add_action(action_open_url) \
                   .create()
  

  
with open("text.json", "w+") as f:
    f.write(card.to_json())

