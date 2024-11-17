"""Features to send adaptive cards to MS Teams Channels via web hooks.

## Resources

- [Adaptive Cards for Python](https://github.com/dennis6p/adaptive-cards-py)
- [Creating incoming web hooks with workflows](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498)
"""

from typing import Any
from dataclasses import asdict, dataclass
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
        content: dict[str, Any] = asdict(card)
        return {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": content,
        }

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
        payload = {"attachments": attachments}
        response = requests.post(
            self._webhook_url, headers=headers, json=payload, timeout=timeout
        )
        if response.status_code not in (200, 202):
            raise RuntimeError(
                f"Failed to send card: {response.status_code}, {response.text}"
            )
        return response
