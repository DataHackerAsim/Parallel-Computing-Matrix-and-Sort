#!/usr/bin/env python3
import random
import sys

def generate_matrix(rows, cols):
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append("{:.4f}".format(random.random()))
        matrix.append(" ".join(row))
    return matrix

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 random_float_matrix.py <rows> <cols>")
        sys.exit(1)

    try:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
    except Exception as e:
        print("Invalid input:", e)
        sys.exit(1)

    matrix = generate_matrix(rows, cols)

    for row in matrix:
        print(row)

if __name__ == "__main__":
    main()
