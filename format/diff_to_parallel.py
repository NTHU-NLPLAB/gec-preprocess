# -*- coding: utf-8 -*-
from .diff import iter_edit


def diff_to_parallel(text, return_list=False):
    text = text.strip()
    if return_list:
        return tuple(iter_edit(text, 'delete')), tuple(iter_edit(text, 'insert'))
    else:
        return ' '.join(iter_edit(text, 'delete')), ' '.join(iter_edit(text, 'insert'))


def main(iterable, ignore_len=2):
    for text in iterable:
        src, tgt = diff_to_parallel(text, return_list=True)
        if len(src) > ignore_len and len(tgt) > ignore_len:
            print(' '.join(src), ' '.join(tgt), sep='\t')


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())

# cat diff.txt | python diff_to_parallel.py
