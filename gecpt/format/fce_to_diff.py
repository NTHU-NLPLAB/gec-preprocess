# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from .diff import gen_diff_token, iter_edit


EDIT_RE = re.compile(r'<NS type="\w+">(((?!<NS).)*?)</NS>')


def parse_ns_token(ns_token):
    ns_node = BeautifulSoup(ns_token, 'lxml-xml').NS
    assert ns_node is not None

    err_type = ns_node.attrs.get('type', '')

    if ns_node.i is None and ns_node.c is None:
        # error is detected but not edited
        ori = cor = ns_node.decode_contents()
    else:
        ori = ns_node.i.decode_contents() if ns_node.i else ''
        cor = ns_node.c.decode_contents() if ns_node.c else ''

    return ori, cor, err_type


def ns_token_to_diff(ns_token, ignore_type=()):
    original, corrected, error_type = parse_ns_token(ns_token)

    # try to flattern nested edits
    original = ' '.join(iter_edit(original.strip(), 'delete'))
    corrected = ' '.join(iter_edit(corrected.strip(), 'insert'))

    # if the error is to be ignored
    if any(t in ignore_type for t in error_type.split(',')):
        token = corrected
    # if error is detected but not edited
    # elif original == corrected:
    #     token = original
    else:
        token = gen_diff_token(original, corrected, error_type)
    # add space to separate tokens
    return f' {token} '


def fce_to_wdiff(text, ignore_type=()):
    while EDIT_RE.search(text):
        ns_tokens = {match.group(0) for match in EDIT_RE.finditer(text)}
        for ns_token in ns_tokens:
            diff_token = ns_token_to_diff(ns_token, ignore_type)
            text = text.replace(ns_token, diff_token)

    # remove consecutive spaces
    text = ' '.join(token for token in text.split(' ') if token)
    return text


def iter_fce(iterable):
    for line in map(str.strip, iterable):
        if line.startswith('<p>') and line.endswith('</p>'):
            yield line[3:-4]


def main(iterable, ignore_type=()):
    for text in iter_fce(iterable):
        print(fce_to_wdiff(text, ignore_type))


if __name__ == '__main__':
    # import sys
    # ignore_type = set(sys.argv[1:])
    # main(sys.stdin, ignore_type=ignore_type)
    import fileinput
    main(fileinput.input())

# cat  | python fce_to_diff.py CE ID
