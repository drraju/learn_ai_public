"""Offline WORD-PIECE toy: these counts are NOT real model token counts."""
text = "Do not restart checkout until the incident lead approves"
pieces = text.split()
print("Toy word pieces:", pieces)
print("Toy count:", len(pieces))
print("Unsafe first-five-piece truncation:", " ".join(pieces[:5]))
print("Illustrative evidence budget:", 100 - 15 - 10 - 25)
