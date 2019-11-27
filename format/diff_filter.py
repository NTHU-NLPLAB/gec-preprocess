#!/usr/bin/env python
# coding: utf-8
import sys

from .diff import parse_diff_token


def diff_filter_iter(tokens, select_types=()):
    for token in tokens:
        if token.startswith(('{+', '[-')):
            _, insert, err_type = parse_diff_token(token)
            if err_type in select_types:
                yield token
            elif insert:
                yield insert
        else:
            yield token


def diff_filter(line, select_types=()):
    tokens = line.split(' ')
    return ' '.join(diff_filter_iter(tokens, select_types))


def main(iterable, select_types=()):
    for line in map(str.strip, iterable):
        print(diff_filter(line, select_types))


if __name__ == "__main__":
    select_types = tuple(sys.argv[1:])
    main(sys.stdin, select_types=select_types)

# cat fce.dev.r.noun.txt | python multi_to_one.py R:NOUN
