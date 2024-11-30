# test_math_operations.py
import unittest
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

import adaptive_cards.card_types as types
import adaptive_cards.utils as utils
from adaptive_cards import (
    AdaptiveCard,
    TextBlock,
)
from adaptive_cards.validation import (
    CardValidator,
    CardValidatorFactory,
    Result,
    ValidationFailure,
)


class TestAdaptiveCard(unittest.TestCase):
    def test_card_validator_ms_teams_validate_success(self) -> None:
        """Run test for simple card"""
        validator: CardValidator = CardValidatorFactory.create_validator_ms_teams()
        card: AdaptiveCard = (
            AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()
        )
        self.assertEqual(validator.validate(card), Result.SUCCESS)
        self.assertEqual(len(validator.details()), 0)

    def test_validate_failure_empty_body(self) -> None:
        validator: CardValidator = CardValidatorFactory.create_validator_ms_teams()
        card: AdaptiveCard = AdaptiveCard.new().create()
        self.assertEqual(validator.validate(card), Result.FAILURE)
        self.assertEqual(len(validator.details()), 1)
        self.assertEqual(validator.details()[0].failure, ValidationFailure.EMPTY_CARD)

    def test_validate_failure_invalid_field_version(self) -> None:
        validator: CardValidator = CardValidatorFactory.create_validator_ms_teams()
        card: AdaptiveCard = (
            AdaptiveCard.new()
            .version("1.0")
            .add_item(TextBlock(text="Test Card", font_type=types.FontType.MONOSPACE))
            .create()
        )
        self.assertEqual(validator.validate(card), Result.FAILURE)
        self.assertEqual(len(validator.details()), 1)
        self.assertEqual(
            validator.details()[0].failure, ValidationFailure.INVALID_FIELD_VERSION
        )

    def test_validate_failure_invalid_schema(self) -> None:
        validator: CardValidator = CardValidatorFactory.create_validator_ms_teams()

        @dataclass_json
        @dataclass
        class InvalidClass:
            some_field: int | None = field(
                default=None, metadata=utils.get_metadata("1.0")
            )

        card: AdaptiveCard = (
            AdaptiveCard.new().version("1.0").add_item(InvalidClass(1)).create()  #
        )
        self.assertEqual(validator.validate(card), Result.FAILURE)
        self.assertEqual(len(validator.details()), 1)
        self.assertEqual(
            validator.details()[0].failure, ValidationFailure.INVALID_SCHEMA
        )

    def test_validate_failure_size_limit_exceeded(self) -> None:
        validator: CardValidator = CardValidatorFactory.create_validator_ms_teams()

        card: AdaptiveCard = (
            AdaptiveCard.new()
            .version("1.0")
            .add_items([TextBlock(text="TestCard") for i in range(660)])
            .create()  #
        )

        self.assertTrue(validator.card_size(card) < 28)
        self.assertEqual(validator.validate(card), Result.SUCCESS)

        card = (
            AdaptiveCard.new()
            .version("1.0")
            .add_items([TextBlock(text="TestCard") for i in range(670)])
            .create()  #
        )
        self.assertTrue(validator.card_size(card) > 28)
        self.assertEqual(validator.validate(card), Result.FAILURE)
        self.assertEqual(len(validator.details()), 1)
        self.assertEqual(
            validator.details()[0].failure, ValidationFailure.SIZE_LIMIT_EXCEEDED
        )


if __name__ == "__main__":
    unittest.main()