# ai_brain/context_builder.py

from datetime import datetime


class ContextBuilder:

    def __init__(
        self,
        chat_memory,
        long_term_memory
    ):

        self.chat_memory = chat_memory
        self.long_term_memory = long_term_memory

    def build_context(
        self,
        user_message,
        recent_limit=15,
        memory_limit=10
    ):

        recent_chat = (
            self.chat_memory
            .get_recent_messages(
                recent_limit
            )
        )

        long_memories = (
            self.long_term_memory
            .get_recent_memories(
                memory_limit
            )
        )

        context = {
            "timestamp":
                datetime.now()
                .isoformat(),

            "user_message":
                user_message,

            "recent_chat":
                recent_chat,

            "long_term_memory":
                long_memories
        }

        return context

    def build_prompt(
        self,
        user_message
    ):

        context = self.build_context(
            user_message
        )

        prompt = ""

        prompt += (
            "=== LONG TERM MEMORY ===\n"
        )

        for memory in (
            context[
                "long_term_memory"
            ]
        ):

            prompt += (
                f"- "
                f"{memory['content']}\n"
            )

        prompt += "\n"

        prompt += (
            "=== RECENT CHAT ===\n"
        )

        for message in (
            context[
                "recent_chat"
            ]
        ):

            prompt += (
                f"["
                f"{message['role']}"
                f"] "
                f"{message['content']}\n"
            )

        prompt += "\n"

        prompt += (
            "=== USER MESSAGE ===\n"
        )

        prompt += (
            user_message
        )

        return prompt

    def export_context(
        self,
        user_message
    ):

        return self.build_context(
            user_message
        )


# TEST

if __name__ == "__main__":

    class DummyChat:

        def get_recent_messages(
            self,
            limit
        ):

            return [
                {
                    "role":
                    "user",

                    "content":
                    "Hello"
                },

                {
                    "role":
                    "assistant",

                    "content":
                    "Hi"
                }
            ]

    class DummyMemory:

        def get_recent_memories(
            self,
            limit
        ):

            return [
                {
                    "content":
                    "User likes AI"
                }
            ]

    builder = ContextBuilder(
        DummyChat(),
        DummyMemory()
    )

    prompt = (
        builder.build_prompt(
            "Tell me about AI"
        )
    )

    print(prompt)
