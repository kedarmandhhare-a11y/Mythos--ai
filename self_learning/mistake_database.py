# self_learning/mistake_database.py

import json
import os
from datetime import datetime


class MistakeDatabase:

    def __init__(
        self,
        database_file="mistake_database.json"
    ):

        self.database_file = database_file
        self.mistakes = []

        self.load_database()

    def add_mistake(
        self,
        user_message,
        ai_response,
        issue_type,
        correction=""
    ):

        record = {

            "id":
                len(self.mistakes) + 1,

            "timestamp":
                datetime.now()
                .isoformat(),

            "user_message":
                user_message,

            "ai_response":
                ai_response,

            "issue_type":
                issue_type,

            "correction":
                correction
        }

        self.mistakes.append(
            record
        )

        self.save_database()

        return record

    def get_all_mistakes(
        self
    ):

        return self.mistakes

    def total_mistakes(
        self
    ):

        return len(
            self.mistakes
        )

    def search_mistakes(
        self,
        keyword
    ):

        keyword = keyword.lower()

        results = []

        for item in self.mistakes:

            if (
                keyword in
                item["user_message"]
                .lower()

                or

                keyword in
                item["ai_response"]
                .lower()

                or

                keyword in
                item["issue_type"]
                .lower()
            ):

                results.append(
                    item
                )

        return results

    def get_issue_stats(
        self
    ):

        stats = {}

        for item in self.mistakes:

            issue = item[
                "issue_type"
            ]

            stats[
                issue
            ] = (
                stats.get(
                    issue,
                    0
                ) + 1
            )

        return stats

    def recent_mistakes(
        self,
        limit=20
    ):

        return self.mistakes[
            -limit:
        ]

    def delete_mistake(
        self,
        mistake_id
    ):

        self.mistakes = [

            item

            for item
            in self.mistakes

            if item["id"]
            != mistake_id
        ]

        self.save_database()

    def clear_database(
        self
    ):

        self.mistakes = []

        self.save_database()

    def save_database(
        self
    ):

        try:

            with open(
                self.database_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.mistakes,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as error:

            print(
                "Save Error:",
                error
            )

    def load_database(
        self
    ):

        try:

            if os.path.exists(
                self.database_file
            ):

                with open(
                    self.database_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.mistakes = (
                        json.load(
                            file
                        )
                    )

        except Exception as error:

            print(
                "Load Error:",
                error
            )

            self.mistakes = []


if __name__ == "__main__":

    db = MistakeDatabase()

    db.add_mistake(

        user_message=
            "What is AI?",

        ai_response=
            "AI",

        issue_type=
            "response_too_short",

        correction=
            "Provide detailed answer"
    )

    print(
        "Total:",
        db.total_mistakes()
    )

    print(
        db.get_issue_stats()
      )
