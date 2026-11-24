"""One synthetic attention query; not a complete transformer or explanation tool."""
import math
from day05_vectors import dot


def attention(query, keys, values):
    if not keys or len(keys) != len(values):
        raise ValueError("Provide one value per key")
    dimension = len(query)
    if dimension == 0 or any(len(k) != dimension for k in keys):
        raise ValueError("Query and keys must share a non-zero dimension")
    if not values[0] or any(len(v) != len(values[0]) for v in values):
        raise ValueError("Values must share a non-zero dimension")
    scores = [dot(query, key) / math.sqrt(dimension) for key in keys]
    largest = max(scores)
    exponents = [math.exp(score - largest) for score in scores]
    total = sum(exponents)
    weights = [number / total for number in exponents]
    output = [sum(w * value[j] for w, value in zip(weights, values))
              for j in range(len(values[0]))]
    return scores, weights, output


if __name__ == "__main__":
    scores, weights, output = attention([1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 20]])
    print("scores:", [round(x, 4) for x in scores])
    print("weights:", [round(x, 4) for x in weights])
    print("output:", [round(x, 4) for x in output])
