#!/usr/bin/env python
# coding: utf-8

import sys
import re


def parse(word):
    error = ''
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


def iter_diff(iterable):
    for line in map(str.strip, iterable):
        yield line.split(' ')


def main(iterable, select_type=tuple()):
    for line in iter_diff(iterable):
        print(multi_to_less(line, select_type))

select_type = tuple(sys.argv[1:])
main(sys.stdin, select_type)


# cat fce.dev.r.noun.txt | python multi_to_one.py R:NOUN

