# foundation/long_term_memory.py

import json
import os
from datetime import datetime


class LongTermMemory:

    def __init__(
        self,
        memory_file="long_term_memory.json"
    ):

        self.memory_file = memory_file
        self.memories = []

        self.load()

    def add_memory(
        self,
        content,
        category="general"
    ):

        memory = {
            "content": content,
            "category": category,
            "created_at": datetime.now().isoformat()
        }

        self.memories.append(memory)

        self.save()

        return memory

    def get_all_memories(self):

        return self.memories

    def get_recent_memories(
        self,
        limit=20
    ):

        return self.memories[-limit:]

    def search(
        self,
        keyword
    ):

        keyword = keyword.lower()

        results = []

        for memory in self.memories:

            if keyword in memory[
                "content"
            ].lower():

                results.append(memory)

        return results

    def get_by_category(
        self,
        category
    ):

        results = []

        for memory in self.memories:

            if memory[
                "category"
            ] == category:

                results.append(memory)

        return results

    def delete_memory(
        self,
        index
    ):

        if (
            index >= 0
            and index < len(
                self.memories
            )
        ):

            deleted = self.memories.pop(
                index
            )

            self.save()

            return deleted

        return None

    def clear_memory(self):

        self.memories = []

        self.save()

    def total_memories(self):

        return len(
            self.memories
        )

    def save(self):

        try:

            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.memories,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as error:

            print(
                "Save Error:",
                error
            )

    def load(self):

        try:

            if os.path.exists(
                self.memory_file
            ):

                with open(
                    self.memory_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    self.memories = json.load(
                        file
                    )

        except Exception as error:

            print(
                "Load Error:",
                error
            )

            self.memories = []


if __name__ == "__main__":

    memory = LongTermMemory()

    memory.add_memory(
        "User likes AI startups",
        "user_profile"
    )

    memory.add_memory(
        "Interested in SaaS business",
        "business"
    )

    print(
        "Total Memories:",
        memory.total_memories()
    )

    print(
        memory.search("AI")
      )
