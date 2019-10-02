# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from .diff import gen_diff_token, iter_edit


EDIT_RE = re.compile('<change>(((?!<change>).)*?)</change>')


def parse_ef_change(content):
    soup = BeautifulSoup(content, 'lxml')
    original = soup.select_one('selection').decode_contents()
    corrected = soup.select_one('tag correct').decode_contents()
    error_type = soup.select_one('tag symbol').decode_contents()

    # try to flattern nested edits
    original = ' '.join(iter_edit(original.strip(), 'delete'))
    corrected = ' '.join(iter_edit(corrected.strip(), 'insert'))
    # replace ` and ` to commas
    error_type = error_type.replace(' and ', ',')
    return original, corrected, error_type


def ef_change_to_diff(change_token, ignore_type=()):
    original, corrected, error_type = parse_ef_change(change_token)

    # if the error is to be ignored
    if any(t in ignore_type for t in error_type.split(',')):
        token = corrected
    else:
        token = gen_diff_token(original, corrected, error_type)
    return f' {token} '


def ef_to_wdiff(text, ignore_type=('HL',)):
    # nested edit
    while EDIT_RE.search(text):
        change_tokens = {match.group(0) for match in EDIT_RE.finditer(text)}
        for change_token in change_tokens:
            diff_token = change_to_diff(change_token, ignore_type=ignore_type)
            text = text.replace(change_token, diff_token)

    # remove consecutive spaces
    return ' '.join(token for token in text.split(' ') if token)


def main(iterable):
    for text in map(str.strip, iterable):
        print(convert_to_wdiff(text, ignore_type))


if __name__ == '__main__':
    import sys
    ignore_type = set(sys.argv[1:])
    main(sys.stdin, ignore_type)
