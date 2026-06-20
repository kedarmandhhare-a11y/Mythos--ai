# self_learning/feedback_analyzer.py

from datetime import datetime


class FeedbackAnalyzer:

    def __init__(
        self,
        logger=None,
        long_term_memory=None
    ):

        self.logger = logger
        self.long_term_memory = long_term_memory

        self.feedback_records = []

    def add_feedback(
        self,
        user_message,
        ai_response,
        rating,
        feedback_text=""
    ):

        record = {

            "timestamp":
                datetime.now()
                .isoformat(),

            "user_message":
                user_message,

            "ai_response":
                ai_response,

            "rating":
                rating,

            "feedback":
                feedback_text
        }

        self.feedback_records.append(
            record
        )

        if (
            self.long_term_memory
        ):

            try:

                self.long_term_memory.add_memory(
                    content=(
                        f"Feedback Rating: "
                        f"{rating}"
                    ),
                    category=(
                        "feedback"
                    )
                )

            except Exception:
                pass

        if self.logger:

            try:

                self.logger.info(
                    "FEEDBACK",
                    (
                        f"Rating={rating}"
                    )
                )

            except Exception:
                pass

        return record

    def average_rating(
        self
    ):

        if not self.feedback_records:
            return 0

        total = sum(
            item["rating"]
            for item in self.feedback_records
        )

        return round(
            total /
            len(
                self.feedback_records
            ),
            2
        )

    def get_positive_feedback(
        self
    ):

        return [

            item

            for item in
            self.feedback_records

            if item["rating"] >= 4
        ]

    def get_negative_feedback(
        self
    ):

        return [

            item

            for item in
            self.feedback_records

            if item["rating"] <= 2
        ]

    def generate_improvement_report(
        self
    ):

        positive = len(
            self.get_positive_feedback()
        )

        negative = len(
            self.get_negative_feedback()
        )

        average = (
            self.average_rating()
        )

        report = {

            "total_feedback":
                len(
                    self.feedback_records
                ),

            "average_rating":
                average,

            "positive":
                positive,

            "negative":
                negative
        }

        if average < 3:

            report[
                "recommendation"
            ] = (
                "Improve response quality"
            )

        elif average < 4:

            report[
                "recommendation"
            ] = (
                "Needs optimization"
            )

        else:

            report[
                "recommendation"
            ] = (
                "Performance good"
            )

        return report

    def recent_feedback(
        self,
        limit=20
    ):

        return (
            self.feedback_records[
                -limit:
            ]
        )

    def clear(
        self
    ):

        self.feedback_records = []

    def total_feedback(
        self
    ):

        return len(
            self.feedback_records
        )


if __name__ == "__main__":

    analyzer = (
        FeedbackAnalyzer()
    )

    analyzer.add_feedback(
        "What is AI?",
        "AI is Artificial Intelligence.",
        5,
        "Very good answer"
    )

    analyzer.add_feedback(
        "Explain Python",
        "Python",
        2,
        "Too short"
    )

    print(
        analyzer.generate_improvement_report()
          )
