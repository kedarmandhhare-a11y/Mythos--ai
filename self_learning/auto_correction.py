# self_learning/auto_correction.py

from datetime import datetime


class AutoCorrectionEngine:

    def __init__(
        self,
        logger=None,
        long_term_memory=None
    ):

        self.logger = logger
        self.long_term_memory = long_term_memory

        self.corrections = []

    def detect_issue(
        self,
        user_message,
        ai_response
    ):

        issues = []

        if not ai_response:
            issues.append(
                "empty_response"
            )

        if len(ai_response) < 10:
            issues.append(
                "response_too_short"
            )

        if (
            "error" in
            ai_response.lower()
        ):
            issues.append(
                "possible_error"
            )

        return issues

    def create_correction(
        self,
        user_message,
        ai_response
    ):

        issues = self.detect_issue(
            user_message,
            ai_response
        )

        correction = {

            "timestamp":
                datetime.now()
                .isoformat(),

            "user_message":
                user_message,

            "ai_response":
                ai_response,

            "issues":
                issues,

            "status":
                (
                    "needs_review"
                    if issues
                    else
                    "ok"
                )
        }

        self.corrections.append(
            correction
        )

        if (
            self.long_term_memory
            and issues
        ):

            try:

                self.long_term_memory.add_memory(
                    content=(
                        f"Issue: {issues}"
                    ),
                    category=(
                        "auto_correction"
                    )
                )

            except Exception:
                pass

        if self.logger:

            try:

                self.logger.info(
                    "AUTO_CORRECTION",
                    (
                        f"Detected "
                        f"{len(issues)} "
                        f"issues"
                    )
                )

            except Exception:
                pass

        return correction

    def get_corrections(self):

        return self.corrections

    def get_recent(
        self,
        limit=20
    ):

        return self.corrections[
            -limit:
        ]

    def total_corrections(
        self
    ):

        return len(
            self.corrections
        )

    def clear(self):

        self.corrections = []

    def analyze_trends(
        self
    ):

        stats = {

            "empty_response":
                0,

            "response_too_short":
                0,

            "possible_error":
                0
        }

        for item in (
            self.corrections
        ):

            for issue in (
                item["issues"]
            ):

                if issue in stats:
                    stats[
                        issue
                    ] += 1

        return stats


if __name__ == "__main__":

    engine = (
        AutoCorrectionEngine()
    )

    result = (
        engine.create_correction(
            "What is AI?",
            "AI"
        )
    )

    print(result)

    print(
        engine.analyze_trends()
      )
