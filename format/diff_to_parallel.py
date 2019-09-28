# -*- coding: utf-8 -*-
import fileinput
import sys

from .diff_format import iter_edit


def main(ignore_len=0):
    for line in fileinput.input():
        text = line.strip()
        src = list(iter_edit(text, 'delete'))
        tgt = list(iter_edit(text, 'insert'))

        if len(src) > ignore_len and len(tgt) > ignore_len:
            print(' '.join(src), file=sys.stderr)
            print(' '.join(tgt))


if __name__ == '__main__':
    main()

# cat diff.txt|python diff_to_parallel.py 1>trg.txt 2>src.txt
