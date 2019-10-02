# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from .diff import gen_diff_token


EDIT_RE = re.compile(r'<NS type="\w+">(((?!<NS).)*?)</NS>')


def parse_ns_token(ns_token):
    soup = BeautifulSoup(ns_token, 'lxml-xml')
    err_type = soup.select_one('NS').attrs.get('type', '')
    i_node = soup.select_one('i')
    ori = i_node.text if i_node else ''
    c_node = soup.select_one('c')
    cor = c_node.text if c_node else ''
    return ori, cor, err_type


def ns_token_to_diff(ns_token, ignore_type=set()):
    original, corrected, error_type = parse_ns_token(ns_token)

    # if the error is to be ignored
    if any(t in ignore_type for t in error_type.split(',')):
        token = corrected
    else:
        token = gen_diff_token(original, corrected, error_type)
    return f' {token} '


def fce_to_wdiff(text, ignore_type=set()):
    while EDIT_RE.search(text):
        ns_tokens = {match.group(0) for match in EDIT_RE.finditer(text)}
        for ns_token in ns_tokens:
            diff_token = ns_token_to_diff(ns_token, ignore_type)
            text = text.replace(ns_token, diff_token)

    # remove consecutive spaces
    text = ' '.join(token for token in text.split(' ') if token)
    return text


def iter_fce(iterable):
    for line in iterable:
        if line.startswith('<p>') and line.endswith('</p>'):
            yield line[3:-4]


def main(iterable, ignore_type=set()):
    for text in iter_fce(map(str.strip, iterable)):
        print(fce_to_wdiff(text, ignore_type))


if __name__ == '__main__':
    import sys
    ignore_type = set(sys.argv[1:])
    main(sys.stdin, ignore_type)

# cat  | python -m gecdiff.format.fce_to_diff CE ID
