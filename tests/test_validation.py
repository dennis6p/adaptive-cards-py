"""Tests for validation module"""

from pydantic import BaseModel, Field
from result import is_err, is_ok

from adaptive_cards import utils
from adaptive_cards.card import AdaptiveCard, TextBlock
from adaptive_cards.types import FontType
from adaptive_cards.validation import (
    CardValidator,
    CardValidatorFactory,
    ValidationFailure,
)


class TestCardValidation:
    def test_card_validator_ms_teams_validate_success(self):
        """Test validation for ms teams"""
        validator: CardValidator = (
            CardValidatorFactory.create_validator_microsoft_teams()
        )
        card: AdaptiveCard = (
            AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()
        )
        assert is_ok(validator.validate(card))
        assert len(validator.details()) == 0

    def test_validate_failure_empty_body(self):
        """Test validation for ms teams"""
        validator: CardValidator = (
            CardValidatorFactory.create_validator_microsoft_teams()
        )
        card: AdaptiveCard = AdaptiveCard.new().create()
        assert is_err(validator.validate(card))
        assert len(validator.details()) == 1
        assert validator.details()[0].failure == ValidationFailure.EMPTY_CARD

    def test_validate_failure_invalid_field_version(self):
        """Test validation for ms teams"""
        validator: CardValidator = (
            CardValidatorFactory.create_validator_microsoft_teams()
        )

        # should fail as font_type is available only card schemas > 1.2
        text_block = TextBlock(text="Test Card", font_type=FontType.MONOSPACE)
        card: AdaptiveCard = (
            AdaptiveCard.new().version("1.0").add_item(text_block).create()
        )
        assert is_err(validator.validate(card, debug=True))
        assert len(validator.details()) == 1
        assert validator.details()[0].failure == ValidationFailure.INVALID_FIELD_VERSION

    def test_validate_failure_invalid_schema(self):
        """Test validation for ms teams"""
        validator: CardValidator = (
            CardValidatorFactory.create_validator_microsoft_teams()
        )

        class InvalidClass(BaseModel):
            """Invalid class"""

            some_field: int | None = Field(
                default=None, json_schema_extra=utils.get_metadata("1.0")
            )

        card: AdaptiveCard = (
            AdaptiveCard.new()
            .version("1.0")
            .add_item(InvalidClass(some_field=1))  # type: ignore
            .create()
        )
        assert is_err(validator.validate(card))
        assert len(validator.details()) == 1
        assert validator.details()[0].failure == ValidationFailure.INVALID_SCHEMA

    def test_validate_failure_size_limit_exceeded(self):
        """Test validation for ms teams"""
        validator: CardValidator = (
            CardValidatorFactory.create_validator_microsoft_teams()
        )

        card: AdaptiveCard = (
            AdaptiveCard.new()
            .version("1.0")
            .add_items([TextBlock(text="TestCard") for i in range(730)])
            .create()
        )

        assert validator.card_size(card) < 28
        assert is_ok(validator.validate(card))

        card = (
            AdaptiveCard.new()
            .version("1.0")
            .add_items([TextBlock(text="TestCard") for i in range(740)])
            .create()
        )
        assert validator.card_size(card) > 28
        assert is_err(validator.validate(card))
        assert len(validator.details()) == 1
        assert validator.details()[0].failure == ValidationFailure.SIZE_LIMIT_EXCEEDED
