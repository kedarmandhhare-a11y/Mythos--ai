# integrations/openai_client.py

import os

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class OpenAIClient:

    def __init__(self):

        self.api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o"
        )

        self.client = None

        if (
            OpenAI is not None
            and self.api_key
        ):

            self.client = OpenAI(
                api_key=self.api_key
            )

    def generate(
        self,
        prompt,
        system_prompt=(
            "You are Mythos AI."
        ),
        temperature=0.7,
        max_tokens=1000
    ):

        if not self.api_key:

            return (
                "OpenAI API Key not found."
            )

        if self.client is None:

            return (
                "OpenAI SDK not installed."
            )

        try:

            response = (
                self.client.chat.completions.create(
                    model=self.model,

                    messages=[
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

                    temperature=
                        temperature,

                    max_tokens=
                        max_tokens
                )
            )

            return (
                response
                .choices[0]
                .message
                .content
            )

        except Exception as error:

            return (
                f"OpenAI Error: "
                f"{error}"
            )

    def health_check(self):

        if not self.api_key:

            return False

        return True


if __name__ == "__main__":

    client = OpenAIClient()

    result = client.generate(
        "Explain Artificial Intelligence"
    )

    print(result)
