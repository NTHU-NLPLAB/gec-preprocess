# -*- coding: utf-8 -*-
import fileinput

from .diff_format import iter_edit


def diff_to_parallel(iterable):
    for text in map(str.strip, iterable):
        src = list(iter_edit(text, 'delete'))
        tgt = list(iter_edit(text, 'insert'))
        yield src, tgt


def main(iterable, ignore_len=2):
    for src, tgt in diff_to_parallel(iterable, ignore_len=0):
        if len(src) > ignore_len and len(tgt) > ignore_len:
            print(' '.join(src), ' '.join(tgt), sep='\t')


if __name__ == '__main__':
    main(fileinput.input())

# cat diff.txt|python diff_to_parallel.py
