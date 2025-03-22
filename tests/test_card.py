from adaptive_cards.card import AdaptiveCard
from adaptive_cards.inputs import InputText
from result import is_ok, is_err
from adaptive_cards.actions import ActionSubmit


class TestAdaptiveCard:
    def test_create_card(self):
        card = AdaptiveCard.new().version("1.2").create()
        assert card.type == "AdaptiveCard"
        assert card.version == "1.2"

    def test_add_item(self):
        input_text: InputText = InputText(id="test", label="test")
        card: AdaptiveCard = AdaptiveCard.new().add_item(input_text).create()
        assert card.body is not None
        assert input_text in card.body

    def test_update_item_success(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = (
            AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()
        )

        result = card.update_item("id", label="updated")

        assert is_ok(result)
        assert card_updated == card

    def test_update_item_not_found(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = (
            AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()
        )

        result = card.update_item("wrong-id", label="updated")

        assert is_err(result)
        assert card_updated != card

    def test_update_item_field_not_found(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = (
            AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()
        )

        result = card.update_item("id", wrong_field="updated")

        assert is_err(result)
        assert card_updated != card

    def test_update_item_wrong_value_type(self):
        input_text: InputText = InputText(id="id", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()

        input_text_updated: InputText = InputText(id="id", label="updated")
        card_updated = (
            AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()
        )

        result = card.update_item("id", label=1)

        assert is_err(result)
        assert card_updated != card

    def test_add_action(self):
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card: AdaptiveCard = AdaptiveCard.new().add_action(action_submit).create()
        assert card.actions is not None
        assert action_submit in card.actions

    def test_add_actions(self):
        action_submit1: ActionSubmit = ActionSubmit(id="action1", title="Submit1")
        action_submit2: ActionSubmit = ActionSubmit(id="action2", title="Submit2")
        card: AdaptiveCard = (
            AdaptiveCard.new().add_actions([action_submit1, action_submit2]).create()
        )
        assert card.actions is not None
        assert action_submit1 in card.actions
        assert action_submit2 in card.actions

    def test_update_action_success(self):
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()

        result = card.update_action("action1", title="Updated Submit")

        assert is_ok(result)
        assert card._actions["action1"].title == "Updated Submit"

    def test_update_action_element_not_found(self):
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()

        result = card.update_action("wrong-id", title="Updated Submit")

        assert is_err(result)

    def test_update_action_field_not_found(self):
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()

        result = card.update_action("action1", wrong_field="Updated Submit")

        assert is_err(result)

    def test_update_action_wrong_value_type(self):
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()

        result = card.update_action("action1", title=123)

        assert is_err(result)
