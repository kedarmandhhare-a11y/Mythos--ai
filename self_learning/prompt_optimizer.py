# self_learning/prompt_optimizer.py

from datetime import datetime


class PromptOptimizer:

    def __init__(
        self,
        logger=None,
        mistake_database=None
    ):

        self.logger = logger
        self.mistake_database = (
            mistake_database
        )

        self.optimization_history = []

    def optimize_prompt(
        self,
        user_prompt
    ):

        optimized = (
            user_prompt.strip()
        )

        if len(
            optimized
        ) < 10:

            optimized += (
                "\nProvide a detailed answer."
            )

        record = {

            "timestamp":
                datetime.now()
                .isoformat(),

            "original":
                user_prompt,

            "optimized":
                optimized
        }

        self.optimization_history.append(
            record
        )

        if self.logger:

            try:

                self.logger.info(
                    "PROMPT_OPTIMIZER",
                    "Prompt optimized"
                )

            except Exception:
                pass

        return optimized

    def learn_from_mistakes(
        self
    ):

        if not (
            self.mistake_database
        ):

            return []

        try:

            stats = (
                self.mistake_database
                .get_issue_stats()
            )

            suggestions = []

            for (
                issue,
                count
            ) in stats.items():

                if issue == (
                    "response_too_short"
                ):

                    suggestions.append(
                        (
                            "Encourage detailed "
                            "responses"
                        )
                    )

                elif issue == (
                    "empty_response"
                ):

                    suggestions.append(
                        (
                            "Improve prompt "
                            "clarity"
                        )
                    )

            return suggestions

        except Exception:

            return []

    def generate_strategy(
        self
    ):

        suggestions = (
            self.learn_from_mistakes()
        )

        return {

            "generated_at":
                datetime.now()
                .isoformat(),

            "suggestions":
                suggestions
        }

    def total_optimizations(
        self
    ):

        return len(
            self.optimization_history
        )

    def recent_optimizations(
        self,
        limit=20
    ):

        return (
            self.optimization_history[
                -limit:
            ]
        )

    def clear_history(
        self
    ):

        self.optimization_history = []


if __name__ == "__main__":

    optimizer = (
        PromptOptimizer()
    )

    result = (
        optimizer.optimize_prompt(
            "What is AI"
        )
    )

    print(result)

    print(
        optimizer.generate_strategy()
            )
