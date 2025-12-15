import pytest
from result import is_err, is_ok

from adaptive_cards.card import ActionSubmit, AdaptiveCard, InputText, TextBlock


class TestAdaptiveCard:
    @pytest.fixture(autouse=True)
    def sample_card_json(self):
        with open("tests/data/sample_card.json", "r") as f:
            return f.read()

    @pytest.fixture(autouse=True)
    def sample_card_small_json(self):
        with open("tests/data/sample_card_small.json", "r") as f:
            return f.read()

    def test_create_card(self):
        """Test creating a new AdaptiveCard and setting its version."""
        card = AdaptiveCard.new().version("1.2").create()
        assert card.type == "AdaptiveCard"
        assert card.version == "1.2"

    def test_create_card_from_file(self, sample_card_json):
        """Test creating an AdaptiveCard from a JSON file and checking its type, version, body, and actions."""
        card = AdaptiveCard.new().from_json(sample_card_json).create()
        assert card.type == "AdaptiveCard"
        assert card.version == "1.6"
        assert card.body is not None
        assert len(card.body) == 8

    def test_create_card_from_file_and_extend(self, sample_card_small_json):
        """Test creating an AdaptiveCard from a JSON file and adding an item afterwards."""
        card = (
            AdaptiveCard.new()
            .from_json(sample_card_small_json)
            .add_item(TextBlock(text="added_afterwards", id="added_afterwards"))
            .create()
        )
        assert len(card.body) == 2
        assert card._items.get("added_afterwards") is not None
        assert card._items["added_afterwards"].text == "added_afterwards"

    def test_create_card_from_file_and_update(self, sample_card_small_json):
        """Test creating an AdaptiveCard from a JSON file and updating an item's field afterwards."""
        card = AdaptiveCard.new().from_json(sample_card_small_json).create()
        assert len(card.body) == 1
        assert card._items.get("id_1") is not None
        assert card._items["id_1"].text == "Welcome to Adaptive Cards!"

        card.update_item("id_1", text="updated_text")
        assert card._items["id_1"].text == "updated_text"

    def test_create_card_from_file_all_items_found(self, sample_card_json):
        """Test that all items from the sample card are found by their IDs and types."""
        card = AdaptiveCard.new().from_json(sample_card_json).create()
        items: dict[str, str] = {
            "id_2": "Container",
            "id_3": "ColumnSet",
            "id_4": "Column",
            "id_5": "TextBlock",
            "id_6": "Column",
            "id_7": "Image",
            "id_8": "Container",
            "id_9": "ColumnSet",
            "id_10": "Column",
            "id_11": "TextBlock",
            "id_12": "Column",
            "id_15": "TextBlock",
            "id_16": "FactSet",
            "id_23": "Container",
            "id_24": "TextBlock",
            "id_28": "Container",
            "id_29": "Container",
            "id_30": "TextBlock",
            "id_31": "Container",
            "id_32": "Input.Text",
            "id_33": "Container",
            "id_34": "ColumnSet",
            "id_35": "Column",
            "id_38": "ColumnSet",
            "id_39": "Column",
            "id_40": "TextBlock",
            "id_41": "TextBlock",
            "id_42": "TextBlock",
            "id_43": "Column",
            "id_44": "TextBlock",
            "id_45": "TextBlock",
            "id_46": "TextBlock",
            "id_47": "Column",
            "id_48": "Container",
            "id_49": "ColumnSet",
            "id_50": "Column",
            "id_51": "TextBlock",
            "id_52": "Column",
            "id_53": "TextBlock",
            "id_54": "Column",
            "id_58": "Container",
            "id_59": "TextBlock",
            "id_60": "TextBlock",
            "id_61": "Container",
            "id_66": "Input.Text",
        }

        assert len(card._items.keys()) == len(items.keys())
        for id, item in card._items.items():
            assert items.get(id) is not None
            assert items[id] == item.type

    def test_create_card_from_file_all_actions_found(self, sample_card_json):
        """Test that all actions from the sample card are found by their IDs and types."""
        card = AdaptiveCard.new().from_json(sample_card_json).create()
        actions: dict[str, str] = {
            "id_13": "ActionSet",
            "id_14": "Action.OpenUrl",
            "id_25": "ActionSet",
            "id_26": "Action.ShowCard",
            "id_36": "ActionSet",
            "id_37": "Action.Submit",
            "id_55": "ActionSet",
            "id_56": "Action.ShowCard",
            "id_62": "ActionSet",
            "id_63": "Action.Submit",
            "id_64": "Action.ShowCard",
            "id_67": "Action.Submit",
        }

        assert len(card._actions.keys()) == len(actions.keys())
        for id, action in card._actions.items():
            assert actions.get(id) is not None
            assert actions[id] == action.type

    def test_add_item(self):
        """Test adding an input item to the card body."""
        input_text: InputText = InputText(id="test", label="test")
        card: AdaptiveCard = AdaptiveCard.new().add_item(input_text).create()
        assert card.body is not None
        assert input_text in card.body

    def test_update_item_new_card_success(self):
        """Test updating an item's field value successfully."""
        input_text: InputText = InputText(id="id_1", label="test")
        card = AdaptiveCard.new().add_item(input_text).version("1.3").create()
        input_text_updated: InputText = InputText(id="id_1", label="updated")
        card_updated = (
            AdaptiveCard.new().add_item(input_text_updated).version("1.3").create()
        )
        result = card.update_item("id_1", label="updated")
        assert is_ok(result)
        assert card_updated == card

    def test_update_item_from_json_success(self, sample_card_json):
        """Test updating an item's field value successfully."""
        card = AdaptiveCard.new().from_json(sample_card_json).create()
        assert card._items["id_40"].text == "Total Expense Amount \t"

        result = card.update_item("id_40", text="Updated TextBlock")
        assert is_ok(result)
        assert card._items["id_40"].text == "Updated TextBlock"

    def test_update_item_not_found(self):
        """Test updating an item with a non-existent id returns an error."""
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
        """Test updating an item with a non-existent field returns an error."""
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
        """Test updating an item with a wrong value type returns an error."""
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
        """Test adding an action to the card."""
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card: AdaptiveCard = AdaptiveCard.new().add_action(action_submit).create()
        assert card.actions is not None
        assert action_submit in card.actions

    def test_add_actions(self):
        """Test adding multiple actions to the card."""
        action_submit1: ActionSubmit = ActionSubmit(id="action1", title="Submit1")
        action_submit2: ActionSubmit = ActionSubmit(id="action2", title="Submit2")
        card: AdaptiveCard = (
            AdaptiveCard.new().add_actions([action_submit1, action_submit2]).create()
        )
        assert card.actions is not None
        assert action_submit1 in card.actions
        assert action_submit2 in card.actions

    def test_update_action_success(self):
        """Test updating an action's field value successfully."""
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()
        result = card.update_action("action1", title="Updated Submit")
        assert is_ok(result)
        assert card._actions["action1"].title == "Updated Submit"

    def test_update_action_element_not_found(self):
        """Test updating an action with a non-existent id returns an error."""
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()
        result = card.update_action("wrong-id", title="Updated Submit")
        assert is_err(result)

    def test_update_action_field_not_found(self):
        """Test updating an action with a non-existent field returns an error."""
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()
        result = card.update_action("action1", wrong_field="Updated Submit")
        assert is_err(result)

    def test_update_action_wrong_value_type(self):
        """Test updating an action with a wrong value type returns an error."""
        action_submit: ActionSubmit = ActionSubmit(id="action1", title="Submit")
        card = AdaptiveCard.new().add_action(action_submit).version("1.3").create()
        result = card.update_action("action1", title=123)
        assert is_err(result)
