"""Features to send adaptive cards to MS Teams Channels via web hooks.

## Resources

- [Adaptive Cards for Python](https://github.com/dennis6p/adaptive-cards-py)
- [Creating incoming web hooks with workflows](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498)
"""  # pylint: disable=line-too-long

from http import HTTPStatus
from typing import Any

import requests
from requests import Response

from adaptive_cards.card import AdaptiveCard


class TeamsClient:
    """Client class for sending adaptive card objects to MS Teams via webhooks"""

    def __init__(self, webhook_url: str) -> None:
        self._webhook_url: str = webhook_url
        """URL the client should communicate with"""

    @staticmethod
    def _create_attachment(card: AdaptiveCard) -> dict:
        """
        Create an attachment from an AdaptiveCard.

        Args:
            card (AdaptiveCard): The AdaptiveCard to create an attachment from.

        Returns:
            dict: A dictionary representing the attachment.
        """
        content: dict[str, Any] = card.to_dict()
        return {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": content,
        }

    def webhook_url(self) -> str:
        """
        Returns webhook URL the current client has been initialized with

        Returns:
            str: _description_
        """
        return self._webhook_url

    def set_webhook_url(self, webhook_url: str) -> None:
        """
        Update webhook URL the client should use when sending a card

        Args:
            webhook_url (str): Webhook URL
        """
        self._webhook_url = webhook_url

    def send(self, *cards: AdaptiveCard, timeout: int = 1000) -> Response:
        """
        Send the payload of one or multiple cards to a via Microsoft Teams webhook.

        Args:
            cards (tuple[AdaptiveCard, ...]: Card objecs supposed to be sent
            timeout (int): Upper request timeout limit

        Returns:
            Response: Response object from the webhook request.

        Raises:
            ValueError: If no webhook URL or no cards are provided.
            RuntimeError: If the request to the webhook fails.
        """
        if not self._webhook_url:
            raise ValueError("No webhook URL provided.")
        if not cards:
            raise ValueError("No cards provided.")

        headers = {"Content-Type": "application/json"}
        attachments = [self._create_attachment(card) for card in cards]
        payload = {"type": "message", "attachments": attachments}
        response = requests.post(
            self._webhook_url, headers=headers, json=payload, timeout=timeout
        )
        if response.status_code not in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
            raise RuntimeError(
                f"Failed to send card: {response.status_code}, {response.text}"
            )
        return response
