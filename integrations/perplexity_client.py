# integrations/perplexity_client.py

import os
import requests


class PerplexityClient:

    def __init__(self):

        self.api_key = os.getenv(
            "PERPLEXITY_API_KEY"
        )

        self.model = os.getenv(
            "PERPLEXITY_MODEL",
            "sonar-pro"
        )

        self.base_url = (
            "https://api.perplexity.ai/chat/completions"
        )

    def generate(
        self,
        prompt,
        system_prompt="You are Mythos AI.",
        temperature=0.7,
        max_tokens=1000
    ):

        if not self.api_key:

            return (
                "Perplexity API Key not found."
            )

        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json"
        }

        payload = {

            "model":
                self.model,

            "messages": [

                {
                    "role":
                    "system",

                    "content":
                    system_prompt
                },

                {
                    "role":
                    "user",

                    "content":
                    prompt
                }
            ],

            "temperature":
                temperature,

            "max_tokens":
                max_tokens
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
                data["choices"][0]
                ["message"]["content"]
            )

        except Exception as error:

            return (
                f"Perplexity Error: {error}"
            )

    def health_check(self):

        return bool(
            self.api_key
        )


if __name__ == "__main__":

    client = PerplexityClient()

    result = client.generate(
        "Explain Artificial Intelligence"
    )

    print(result)
