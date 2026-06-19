# integrations/gemini_client.py

import os
import requests


class GeminiClient:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        self.model = (
            "gemini-2.5-pro"
        )

        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models"
        )

    def generate(
        self,
        prompt
    ):

        if not self.api_key:

            return (
                "Gemini API Key not found."
            )

        url = (
            f"{self.base_url}/"
            f"{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        try:

            response = requests.post(
                url,
                json=payload,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            return (
                data["candidates"][0]
                ["content"]["parts"][0]
                ["text"]
            )

        except Exception as error:

            return (
                f"Gemini Error: {error}"
            )


if __name__ == "__main__":

    client = GeminiClient()

    result = client.generate(
        "Explain Artificial Intelligence"
    )

    print(result)
