# ai_brain/router.py

from datetime import datetime


class AIRouter:

    def __init__(
        self,
        context_builder=None,
        reflection_engine=None,
        openai_client=None,
        gemini_client=None,
        claude_client=None
    ):

        self.context_builder = context_builder
        self.reflection_engine = reflection_engine

        self.openai_client = openai_client
        self.gemini_client = gemini_client
        self.claude_client = claude_client

    def select_model(
        self,
        user_message
    ):

        message = user_message.lower()

        if "code" in message:
            return "openai"

        if "analysis" in message:
            return "claude"

        if "research" in message:
            return "gemini"

        return "openai"

    def build_prompt(
        self,
        user_message
    ):

        if self.context_builder:

            return (
                self.context_builder
                .build_prompt(
                    user_message
                )
            )

        return user_message

    def call_openai(
        self,
        prompt
    ):

        if not self.openai_client:

            return (
                "OpenAI client "
                "not connected."
            )

        return (
            self.openai_client
            .generate(prompt)
        )

    def call_gemini(
        self,
        prompt
    ):

        if not self.gemini_client:

            return (
                "Gemini client "
                "not connected."
            )

        return (
            self.gemini_client
            .generate(prompt)
        )

    def call_claude(
        self,
        prompt
    ):

        if not self.claude_client:

            return (
                "Claude client "
                "not connected."
            )

        return (
            self.claude_client
            .generate(prompt)
        )

    def generate_response(
        self,
        user_message
    ):

        prompt = (
            self.build_prompt(
                user_message
            )
        )

        selected_model = (
            self.select_model(
                user_message
            )
        )

        if selected_model == "openai":

            response = (
                self.call_openai(
                    prompt
                )
            )

        elif selected_model == "gemini":

            response = (
                self.call_gemini(
                    prompt
                )
            )

        elif selected_model == "claude":

            response = (
                self.call_claude(
                    prompt
                )
            )

        else:

            response = (
                "No model selected."
            )

        reflection = None

        if self.reflection_engine:

            reflection = (
                self.reflection_engine
                .full_reflection(
                    user_message,
                    response
                )
            )

        return {
            "timestamp":
                datetime.now()
                .isoformat(),

            "model":
                selected_model,

            "response":
                response,

            "reflection":
                reflection
        }

    def route(
        self,
        user_message
    ):

        return (
            self.generate_response(
                user_message
            )
        )


# TEST

if __name__ == "__main__":

    class DummyAI:

        def generate(
            self,
            prompt
        ):

            return (
                "Dummy AI Response"
            )

    router = AIRouter(
        openai_client=DummyAI(),
        gemini_client=DummyAI(),
        claude_client=DummyAI()
    )

    result = router.route(
        "Write Python code"
    )

    print(result)
