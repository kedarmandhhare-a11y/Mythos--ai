# integrations/claude_client.py

import os
import requests


class ClaudeClient:

    def __init__(self):

        self.api_key = os.getenv(
            "CLAUDE_API_KEY"
        )

        self.model = (
            "claude-3-5-sonnet"
        )

        self.base_url = (
            "https://api.anthropic.com/v1/messages"
        )

    def generate(
        self,
        prompt,
        max_tokens=1000
    ):

        if not self.api_key:

            return (
                "Claude API Key not found."
            )

        headers = {
            "x-api-key":
                self.api_key,

            "anthropic-version":
                "2023-06-01",

            "content-type":
                "application/json"
        }

        payload = {

            "model":
                self.model,

            "max_tokens":
                max_tokens,

            "messages": [
                {
                    "role":
                        "user",

                    "content":
                        prompt
                }
            ]
        }

        try:

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            return (
                data["content"][0]["text"]
            )

        except Exception as error:

            return (
                f"Claude Error: {error}"
            )


if __name__ == "__main__":

    client = ClaudeClient()

    result = client.generate(
        "Explain Artificial Intelligence"
    )

    print(result)
