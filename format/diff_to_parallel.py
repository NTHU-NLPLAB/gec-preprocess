# -*- coding: utf-8 -*-
import fileinput

from .diff_format import iter_edit


def diff_to_parallel(text, return_list=False):
    if return_list:
        return tuple(iter_edit(text, 'delete')), tuple(iter_edit(text, 'insert'))
    else:
        return ' '.join(iter_edit(text, 'delete')), ' '.join(iter_edit(text, 'insert'))


def main(iterable, ignore_len=2):
    for text in map(str.strip, iterable):
        src, tgt = diff_to_parallel(text, return_list=True)
        if len(src) > ignore_len and len(tgt) > ignore_len:
            print(' '.join(src), ' '.join(tgt), sep='\t')


if __name__ == '__main__':
    main(fileinput.input())

# cat diff.txt|python diff_to_parallel.py
