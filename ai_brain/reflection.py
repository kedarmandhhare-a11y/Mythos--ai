# ai_brain/reflection.py

from datetime import datetime


class ReflectionEngine:

    def __init__(
        self,
        chat_memory=None,
        long_term_memory=None
    ):

        self.chat_memory = chat_memory
        self.long_term_memory = long_term_memory

    def analyze_response(
        self,
        user_message,
        ai_response
    ):

        analysis = {
            "timestamp":
                datetime.now().isoformat(),

            "user_message":
                user_message,

            "ai_response":
                ai_response,

            "response_length":
                len(ai_response),

            "status":
                "analyzed"
        }

        return analysis

    def generate_reflection(
        self,
        user_message,
        ai_response
    ):

        reflection = {
            "strengths": [],
            "improvements": [],
            "score": 0
        }

        if len(ai_response) > 50:

            reflection[
                "strengths"
            ].append(
                "Detailed response"
            )

            reflection["score"] += 30

        else:

            reflection[
                "improvements"
            ].append(
                "Response too short"
            )

        if "I don't know" not in ai_response:

            reflection[
                "strengths"
            ].append(
                "Attempted answer"
            )

            reflection["score"] += 20

        if len(ai_response) > 200:

            reflection["score"] += 20

        if reflection["score"] > 100:
            reflection["score"] = 100

        return reflection

    def save_learning(
        self,
        user_message,
        ai_response
    ):

        if not self.long_term_memory:
            return

        reflection = (
            self.generate_reflection(
                user_message,
                ai_response
            )
        )

        self.long_term_memory.add_memory(
            content=(
                f"Reflection Score: "
                f"{reflection['score']}"
            ),
            category="reflection"
        )

    def review_conversation(self):

        if not self.chat_memory:
            return []

        messages = (
            self.chat_memory
            .get_recent_messages(20)
        )

        reviews = []

        for msg in messages:

            reviews.append(
                {
                    "role":
                    msg.get(
                        "role",
                        "unknown"
                    ),

                    "content":
                    msg.get(
                        "content",
                        ""
                    )[:100]
                }
            )

        return reviews

    def full_reflection(
        self,
        user_message,
        ai_response
    ):

        analysis = (
            self.analyze_response(
                user_message,
                ai_response
            )
        )

        reflection = (
            self.generate_reflection(
                user_message,
                ai_response
            )
        )

        return {
            "analysis":
                analysis,

            "reflection":
                reflection
        }


if __name__ == "__main__":

    engine = ReflectionEngine()

    result = (
        engine.full_reflection(
            "What is AI?",
            "Artificial Intelligence is a field of computer science."
        )
    )

    print(result)
