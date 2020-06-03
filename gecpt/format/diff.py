# -*- coding: utf-8 -*-
from operator import itemgetter
import re

from .edit import Edit


DIFF_EDIT_RE = re.compile(r'(\[-(?P<delete>[^ ]*?)-\]|\{\+(?P<insert>[^ ]*?)\+\})+(\((?P<type>[^)]+)\))?')


def parse_diff_token(edit_token):
    match = DIFF_EDIT_RE.match(edit_token)
    assert match, f'"{edit_token}" is not a valid edit token'
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
    if delete and insert and err_type:
        yield f"({space_escape.join(err_type.split())})"


def gen_diff_token(edit: Edit, space_escape='\u3000'):
    return ''.join(_gen_diff_iter(**edit._asdict(), space_escape=space_escape))


def _iter_diff(text, edit_token_function):
    # split into tokens
    tokens = text.split(' ') if type(text) is str else text
    # skip empty tokens
    for token in filter(None, tokens):
        if token.startswith(('{+', '[-')):
            yield edit_token_function(parse_diff_token(token))
        else:
            yield token


def iter_diff(iterable, edit_token_function, skip_empty=True):
    if skip_empty:
        return filter(None, _iter_diff(iterable, edit_token_function))
    else:
        return _iter_diff(iterable, edit_token_function)


def diff_to_parallel(text, return_list=False):
    text = text.strip()
    before, after = iter_diff(text, itemgetter(0)), iter_diff(text, itemgetter(1))
    if return_list:
        return tuple(before), tuple(after)
    else:
        return ' '.join(before), ' '.join(after)
