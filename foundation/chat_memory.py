# foundation/chat_memory.py

import json
import os
from datetime import datetime


class ChatMemory:

    def __init__(
        self,
        memory_file="memory.json",
        max_messages=500
    ):
        self.memory_file = memory_file
        self.max_messages = max_messages
        self.messages = []

        self.load_memory()

    def add_message(self, role, content):

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        self.messages.append(message)

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

        self.save_memory()

    def get_messages(self):
        return self.messages

    def get_recent_messages(self, limit=20):
        return self.messages[-limit:]

    def get_last_message(self):
        if not self.messages:
            return None
        return self.messages[-1]

    def count(self):
        return len(self.messages)

    def clear(self):
        self.messages = []
        self.save_memory()

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for msg in self.messages:
            if keyword in msg["content"].lower():
                results.append(msg)

        return results

    def save_memory(self):

        try:
            with open(
                self.memory_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    self.messages,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as e:
            print("Save Error:", e)

    def load_memory(self):

        try:

            if os.path.exists(self.memory_file):

                with open(
                    self.memory_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.messages = json.load(f)

        except Exception as e:
            print("Load Error:", e)
            self.messages = []

    def export_memory(self):

        return {
            "total_messages": len(self.messages),
            "messages": self.messages
        }


# TEST

if __name__ == "__main__":

    memory = ChatMemory()

    memory.add_message(
        "user",
        "Hello Mythos"
    )

    memory.add_message(
        "assistant",
        "Hello, how can I help you?"
    )

    print(
        "Total Messages:",
        memory.count()
    )

    print(
        memory.get_recent_messages()
  )
