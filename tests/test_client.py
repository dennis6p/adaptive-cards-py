from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from adaptive_cards.card import AdaptiveCard, TextBlock
from adaptive_cards.client import TeamsClient

# filepath: src/adaptive_cards/test_client.py


class TestTeamsClient:
    @patch("adaptive_cards.client.requests.post")
    def test_send_single_card_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_post.return_value = mock_response

        client = TeamsClient("http://example.com/webhook")
        card = AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()
        response = client.send(card)

        assert response.status_code == HTTPStatus.OK
        mock_post.assert_called_once()

    @patch("adaptive_cards.client.requests.post")
    def test_send_multiple_cards_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.ACCEPTED
        mock_post.return_value = mock_response

        client = TeamsClient("http://example.com/webhook")
        card1 = AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()
        card2 = AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()
        response = client.send(card1, card2)

        assert response.status_code == HTTPStatus.ACCEPTED
        mock_post.assert_called_once()

    def test_send_no_webhook_url(self):
        client = TeamsClient("")
        card = AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()

        with pytest.raises(ValueError, match="No webhook URL provided."):
            client.send(card)

    def test_send_no_cards_provided(self):
        client = TeamsClient("http://example.com/webhook")

        with pytest.raises(ValueError, match="No cards provided."):
            client.send()

    @patch("adaptive_cards.client.requests.post")
    def test_send_failed_request(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.BAD_REQUEST
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        client = TeamsClient("http://example.com/webhook")
        card = AdaptiveCard.new().add_item(TextBlock(text="Test Card")).create()

        with pytest.raises(RuntimeError, match="Failed to send card: 400, Bad Request"):
            client.send(card)
