# self_learning/learning_manager.py

from datetime import datetime


class LearningManager:

    def __init__(
        self,
        feedback_analyzer=None,
        auto_correction=None,
        long_term_memory=None,
        logger=None
    ):

        self.feedback_analyzer = (
            feedback_analyzer
        )

        self.auto_correction = (
            auto_correction
        )

        self.long_term_memory = (
            long_term_memory
        )

        self.logger = logger

        self.learning_history = []

    def process_interaction(
        self,
        user_message,
        ai_response,
        rating=None,
        feedback_text=""
    ):

        result = {

            "timestamp":
                datetime.now()
                .isoformat(),

            "user_message":
                user_message,

            "ai_response":
                ai_response
        }

        # Feedback Analysis

        if (
            self.feedback_analyzer
            and rating is not None
        ):

            feedback_result = (
                self.feedback_analyzer
                .add_feedback(
                    user_message,
                    ai_response,
                    rating,
                    feedback_text
                )
            )

            result[
                "feedback"
            ] = feedback_result

        # Auto Correction

        if self.auto_correction:

            correction_result = (
                self.auto_correction
                .create_correction(
                    user_message,
                    ai_response
                )
            )

            result[
                "correction"
            ] = correction_result

        # Long-Term Memory

        if self.long_term_memory:

            try:

                self.long_term_memory.add_memory(

                    content=(
                        f"Interaction: "
                        f"{user_message[:100]}"
                    ),

                    category="learning"
                )

            except Exception:
                pass

        self.learning_history.append(
            result
        )

        if self.logger:

            try:

                self.logger.info(
                    "LEARNING_MANAGER",
                    "Interaction processed"
                )

            except Exception:
                pass

        return result

    def generate_learning_report(
        self
    ):

        report = {

            "total_learning_events":
                len(
                    self.learning_history
                ),

            "generated_at":
                datetime.now()
                .isoformat()
        }

        if self.feedback_analyzer:

            report[
                "average_rating"
            ] = (
                self.feedback_analyzer
                .average_rating()
            )

        if self.auto_correction:

            report[
                "correction_stats"
            ] = (
                self.auto_correction
                .analyze_trends()
            )

        return report

    def recent_learning(
        self,
        limit=20
    ):

        return (
            self.learning_history[
                -limit:
            ]
        )

    def total_events(
        self
    ):

        return len(
            self.learning_history
        )

    def clear_learning_history(
        self
    ):

        self.learning_history = []


if __name__ == "__main__":

    manager = (
        LearningManager()
    )

    result = (
        manager.process_interaction(
            user_message=
                "What is AI?",

            ai_response=
                "AI means Artificial Intelligence."
        )
    )

    print(result)

    print(
        manager.generate_learning_report()
        )
