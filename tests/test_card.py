from cProfile import label
import pytest
from adaptive_cards.card import AdaptiveCard, AdaptiveCardBuilder
from adaptive_cards.inputs import InputText
from result import is_ok


class TestAdaptiveCard:
    def test_create_card(self):
        card = AdaptiveCard.new().type("AdaptiveCard").version("1.2").create()
        assert card.type == "AdaptiveCard"
        assert card.version == "1.2"

    def test_add_item(self):
        input_text: InputText = InputText(id="test", label="test")
        card: AdaptiveCard = AdaptiveCard.new().add_item(input_text).create()
        assert card.body is not None
        assert input_text in card.body

    def test_update_card_success(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()

        result = card.update("id", label="updated")

        assert is_ok(result)
        assert card_updated == card

    def test_update_card_element_not_found(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()

        result = card.update("wrong-id", label="updated")

        assert not is_ok(result)
        assert card_updated != card

    def test_update_card_field_not_found(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()

        result = card.update("wrong-id", wrong_field="updated")

        assert not is_ok(result)
        assert card_updated != card

    def test_update_card_wrong_value_type(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()

        result = card.update("wrong-id", wrong_field=1)

        assert not is_ok(result)
        assert card_updated != card
