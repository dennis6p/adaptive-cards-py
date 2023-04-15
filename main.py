from src.cards import AdaptiveCard
from src.card_elements import TextBlock, Media, MediaSource
from src.card_containers import Container, ColumnSet, Column, FactSet, Fact
from src.card_types import Colors, VerticalAlignment, ContainerStyle, FontType

url = "https://adaptivecards.io/content/cats/1.png"

text_block_1 = TextBlock.new("This is just a test") \
                        .color(Colors.DARK) \
                        .font_type(FontType.MONOSPACE) \
                        .create()

text_block_2 = TextBlock.new("product 2").color(Colors.GOOD).create()

column_1 = Column.new().items([text_block_1]).create()
column_2 = Column.new().items([text_block_2]).create()
column_set = ColumnSet.new().columns([column_1, column_2]).create()

fact_1 = Fact.new(title="first fact", value="1").create()
fact_2 = Fact.new(title="second fact", value="2").create()
fact_set = FactSet.new([fact_1, fact_2]).create()


card = AdaptiveCard.new() \
                   .add_item(column_set) \
                   .add_item(fact_set) \
                   .create()
  

  
with open("text.json", "w+") as f:
    f.write(card.to_json())

