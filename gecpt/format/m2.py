#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import deque
from itertools import groupby
from operator import itemgetter

M2_TOKEN = "{start} {end}|||{err_type}|||{correction}|||{unk1}}|||{unk2}|||{annotator}"


def parse_m2_token(line):
    position, err_type, correction, _, _, annotator = line[2:].split('|||')
    start, end = (int(index) for index in position.split())
    annotator = int(annotator)
    correction = correction.strip()
    return start, end, err_type, correction, annotator


def gen_m2_token(start, end, err_type, correction, annotator, unk1='REQUIRED', unk2='-NONE-'):
    return M2_TOKEN.format(start=start, end=end, err_type=err_type, correction=correction,
                           unk1=unk1, unk2=unk2, annotator=annotator)


def iter_m2(sent, edits, edit_token_func, ignore_type=()):
    # split into tokens if sent is str
    tokens = sent.split() if type(sent) == str else sent
    last = 0
    for start, end, err_type, correction, annotator in edits:
        if start < 0 or end < 0 or err_type == 'noop':
            continue
        if last < start:
            yield ' '.join(tokens[last:start])

        if any(t in ignore_type for t in err_type.split(',')):
            yield correction
        else:
            original = ' '.join(tokens[start:end])
            yield edit_token_func(original, correction, err_type)
        last = end
    if last < len(tokens):
        yield ' '.join(tokens[last:])


def parse_m2_record(m2_record):
    sentence, *edit_strings = m2_record
    assert sentence.startswith('S ')
    assert all(edit_str.startswith('A ') for edit_str in edit_strings)
    sentence = sentence[2:].strip()

    annotations = map(parse_m2_token, edit_strings)
    annotations = sorted(annotations, key=itemgetter(-1))
    for annotator, edits in groupby(annotations, key=itemgetter(-1)):
        yield sentence, edits


def iter_m2_file(iterable):
    stack = deque()
    for line in map(str.strip, iterable):
        if line:
            stack.append(line)
        elif stack:
            yield tuple(stack)
            stack.clear()
    assert len(stack) == 0


if __name__ == "__main__":
    import fileinput

    for m2_records in iter_m2_file(fileinput.input()):
        for sent, edits in parse_m2_record(m2_records):
            print(sent)
            for edit in edits:
                print('>>', *edit)
            print()
