"""Hand-designed vectors teach similarity; they are not learned embeddings."""
import math


def dot(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have equal length")
    return sum(x * y for x, y in zip(a, b))


def cosine(a, b):
    denominator = math.sqrt(dot(a, a)) * math.sqrt(dot(b, b))
    if denominator == 0:
        raise ValueError("Cosine is undefined for a zero vector")
    return dot(a, b) / denominator


if __name__ == "__main__":
    query = [1, 0]
    documents = {"network guide": [1, 0], "database guide": [0, 1],
                 "mixed guide": [1, 1]}
    for name, vector in documents.items():
        print(f"{name}: dot={dot(query, vector):.3f}, cosine={cosine(query, vector):.3f}")
    print("Scaled network cosine:", cosine(query, [10, 0]))
