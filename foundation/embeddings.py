# foundation/embeddings.py

import hashlib
import math


class EmbeddingEngine:

    def __init__(self, dimension=64):
        self.dimension = dimension

    def text_to_embedding(self, text):

        text = text.lower().strip()

        vector = [0.0] * self.dimension

        words = text.split()

        for word in words:

            h = hashlib.sha256(
                word.encode()
            ).hexdigest()

            value = int(h, 16)

            index = value % self.dimension

            vector[index] += 1.0

        return self.normalize(vector)

    def normalize(self, vector):

        magnitude = math.sqrt(
            sum(x * x for x in vector)
        )

        if magnitude == 0:
            return vector

        return [
            x / magnitude
            for x in vector
        ]

    def cosine_similarity(
        self,
        vector1,
        vector2
    ):

        dot = sum(
            a * b
            for a, b in zip(
                vector1,
                vector2
            )
        )

        mag1 = math.sqrt(
            sum(x * x for x in vector1)
        )

        mag2 = math.sqrt(
            sum(x * x for x in vector2)
        )

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot / (mag1 * mag2)

    def compare_texts(
        self,
        text1,
        text2
    ):

        emb1 = self.text_to_embedding(
            text1
        )

        emb2 = self.text_to_embedding(
            text2
        )

        return self.cosine_similarity(
            emb1,
            emb2
        )


if __name__ == "__main__":

    engine = EmbeddingEngine()

    text1 = "Artificial Intelligence"
    text2 = "AI and Machine Learning"

    score = engine.compare_texts(
        text1,
        text2
    )

    print(
        "Similarity:",
        score
      )
