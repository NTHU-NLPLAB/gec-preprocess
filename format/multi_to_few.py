#!/usr/bin/env python
# coding: utf-8
import sys
import re


def parse(word):
    correction = ''
    error_correction, error_type = word.rsplit('(', 1)

    if error_type.startswith('M'):
        correction = error_correction[2:-2]
    if error_type.startswith('R'):
        correction = error_correction.split('-]{+')[1][:-2]

    return correction


def simplify(word, select_types):
    if not re.search(r'\w\)', word):
        return word
    elif word[:-1].endswith(select_types):
        return word
    else:
        return parse(word)


def multi_to_less(line, select_types):
    simplified_line = ' '.join(simplify(word, select_types) for word in line)
    simplified_line = simplified_line.replace('  ', ' ')
    return simplified_line


def main(iterable, select_types=()):
    for line in map(str.strip, iterable):
        tokens = line.split(' ')
        print(multi_to_less(tokens, select_types))


if __name__ == "__main__":
    select_types = tuple(sys.argv[1:])
    main(sys.stdin, select_types)

# cat fce.dev.r.noun.txt | python multi_to_one.py R:NOUN
