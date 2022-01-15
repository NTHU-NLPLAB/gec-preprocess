# -*- coding: utf-8 -*-
from operator import itemgetter
from copy import copy
import re

from .edit import Edit


DIFF_EDIT_RE = re.compile(r'(\[-(?P<delete>.*?)-\]|\{\+(?P<insert>.*?)\+\})+(\((?P<type>.*?)\))?')


def parse_diff_token(token):
    match = token if type(token) is re.Match else DIFF_EDIT_RE.match(token)
    assert match, f'"{token}" is not a valid edit token'
    delete, insert, err_type = match.group('delete'), match.group('insert'), match.group('type')
    delete = ' '.join(delete.split()) if delete else ''
    insert = ' '.join(insert.split()) if insert else ''
    err_type = ' '.join(err_type.split()) if err_type else ''
    return Edit(delete, insert, err_type)


def _gen_diff_iter(delete, insert, err_type=None, space_escape='\u3000'):
    if delete:
        yield f"[-{space_escape.join(delete.split())}-]"
    if insert:
        yield f"{{+{space_escape.join(insert.split())}+}}"
    if (delete or insert) and err_type:
        yield f"({space_escape.join(err_type.split())})"


def gen_diff_token(edit: Edit, space_escape='\u3000'):
    return ''.join(_gen_diff_iter(**edit._asdict(), space_escape=space_escape))


def iter_diff_text(text):
    def __iter():
        last = 0
        for match in DIFF_EDIT_RE.finditer(text):
            yield text[last:match.start()]
            yield parse_diff_token(match)
            last = match.end()
        yield text[last:]

    return filter(None, __iter())


def _iter_diff(text, edit_token_function=copy):
    # split into tokens
    tokens = text.split(' ') if type(text) is str else text
    # skip empty tokens
    for token in filter(None, tokens):
        if token.startswith(('{+', '[-')):
            yield edit_token_function(parse_diff_token(token))
        else:
            yield token


def iter_diff(iterable, edit_token_function=copy, skip_empty=True):
    result = _iter_diff(iterable, edit_token_function)
    if skip_empty:
        return filter(None, result)
    else:
        return result


def diff_to_parallel(text, return_list=False):
    text = text.strip()
    before, after = iter_diff(text, itemgetter(0)), iter_diff(text, itemgetter(1))
    if return_list:
        return tuple(before), tuple(after)
    else:
        return ' '.join(before), ' '.join(after)
