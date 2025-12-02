import sys
import random

if len(sys.argv) != 3:
    print("Usage: python random_float_matrix.py <rows> <cols>")
    sys.exit(1)

try:
    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
except ValueError:
    print("Error: Rows and Cols must be integers.")
    sys.exit(1)

# Generate matrix: rows lines, tab-separated columns
for i in range(rows):
    line = []
    for j in range(cols):
        # random.random() gives a float between 0.0 and 1.0
        line.append(f"{random.random():.4f}")
    print("\t".join(line))
