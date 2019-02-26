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

def compute_dfa(dfa, x):
    """Uses the DFA to compute (x mod m) in base b"""
    states = [(0, 0)]

    for d in x:
        s = states[-1]
        states.append(dfa[s[0]][s[1]][d])

    return states

def main(args):
    b = int(args[1])
    m = int(args[2])
    i = int(args[3])
    x = list(map(int, args[4:]))

    initial, repeating = get_pattern(b, m)
    print(initial)
    print(repeating)

    dfa = gen_dfa_classifier(b, m, initial, repeating)
    for j in range(len(dfa)):
        for k in range(len(dfa[j])):
            print("(%d, %d) %s" % (j, k, str(dfa[j][k])))
    print(len(dfa) * len(dfa[0]))

    states = compute_dfa(dfa, x)
    print(str(states))

    if states[-1][1] == i:
        print("accept")
    else:
        print("reject")

main(sys.argv)
