#!/usr/bin/env python3
# Arman Siddique 115960558

import sys


def get_pattern(b, m):
    """Gets the initial and repeating part of the sequence (b^0 mod m), (b^1 mod m), ..."""

    seq = [1]
    for i in range(1000):
        next = seq[-1] * b % m
        if next in seq:
            return (seq[:seq.index(next)], seq[seq.index(next):])
        seq.append(next)

    return ([], [])


def gen_dfa_classifier(b, m, initial, repeating):
    """Generates a DFA classifier for mod m and base b"""

    dfa = [[[] for j in range(m)] for i in range(len(initial) + len(repeating))]

    # Initial part
    for j,n in enumerate(initial):
        for k in range(m):
            for a in range(b):
                # j = weight index, k = classifier value, a = input digit
                dfa[j][k].append((j + 1, (k + a * n) % m))

    # Repeating part (except last element)
    for j,n in enumerate(repeating[:-1]):
        for k in range(m):
            for a in range(b):
                dfa[j + len(initial)][k].append((j + len(initial) + 1, (k + a * n) % m))

    # Last repeating element
    for k in range(m):
        for a in range(b):
            dfa[len(initial) + len(repeating) - 1][k].append((len(initial), (k + a * repeating[-1]) % m))

    return dfa


def main(args):
    b = int(args[1])
    m = int(args[2])
    i = int(args[3])
    x = args[3]

    initial, repeating = get_pattern(b, m)
    print(initial)
    print(repeating)

    dfa = gen_dfa_classifier(b, m, initial, repeating)
    for i in range(len(dfa)):
        for j in range(len(dfa[i])):
            print("(%d, %d) %s" % (i, j, str(dfa[i][j])))


main(sys.argv)
