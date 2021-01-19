#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import deque, defaultdict

from .diff import gen_diff_token


def parse_annotation(line):
    position, err_type, correction, _, _, annotator = line[2:].split('|||')
    start, end = [int(index) for index in position.split()]
    annotator = int(annotator)
    correction = correction.strip()
    return start, end, err_type, correction, annotator


def parse_m2(lines):
    def iter_records(iterable):
        stack = deque()
        for line in map(str.strip, iterable):
            if line:
                stack.append(line)
            else:
                yield tuple(stack)
                stack.clear()
        assert len(stack) == 0

    for sentence, *editstr in iter_records(lines):
        assert sentence.startswith('S ')
        assert all(edit.startswith('A ') for edit in editstr)
        sentence = sentence[2:].strip()
        edits = defaultdict(deque)
        for *info, annotator in map(parse_annotation, editstr):
            edits[annotator].append(tuple(info))
        yield sentence, edits


def m2_to_diff(sent, edits):
    tokens = sent.split()
    last = 0
    # TODO: handle muti-annotator
    for start, end, err_type, correction in edits:
        if last < start:
            yield ' '.join(tokens[last:start])
        original = ' '.join(tokens[start:end])
        yield gen_diff_token(original, correction, err_type)
        last = end
    if last < len(tokens):
        yield ' '.join(tokens[last:])


def main(iterator):
    for sent, annotation in parse_m2(iterator):
        if len(annotation) == 0:
            print(sent)
        for annotator, edits in annotation.items():
            print(' '.join(m2_to_diff(sent, edits)))


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())

# cat official-2014.1.m2 | python m2_to_diff.py
