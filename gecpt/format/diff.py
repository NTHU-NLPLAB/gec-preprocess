# -*- coding: utf-8 -*-
import re


DIFF_EDIT_RE = re.compile(r'(\[-(?P<delete>[^ ]*?)-\]|\{\+(?P<insert>[^ ]*?)\+\})+(\((?P<type>[^)]+)\))?')


def parse_diff_token(edit_token):
    match = DIFF_EDIT_RE.match(edit_token)
    assert match, f'"{edit_token}" is not a valid edit token'
    delete, insert, err_type = match.group('delete'), match.group('insert'), match.group('type')
    delete = ' '.join(delete.split()) if delete else ''
    insert = ' '.join(insert.split()) if insert else ''
    err_type = ' '.join(err_type.split()) if err_type else ''
    return delete, insert, err_type


def _gen_diff_iter(delete, insert, err_type=None, space_escape='\u3000'):
    if delete:
        yield f"[-{space_escape.join(delete.split())}-]"
    if insert:
        yield f"{{+{space_escape.join(insert.split())}+}}"
    if delete and insert and err_type:
        yield f"({space_escape.join(err_type.split())})"


def gen_diff_token(delete, insert, err_type=None, space_escape='\u3000'):
    return ''.join(_gen_diff_iter(delete, insert, err_type, space_escape))


def _iter_diff(iterable, iter_type):
    index = ('delete', 'insert', 'error').index(iter_type)
    # split into tokens
    tokens = iterable.split(' ') if type(iterable) is str else iterable
    # skip empty tokens
    for token in filter(None, tokens):
        if token.startswith(('{+', '[-')):
            yield parse_diff_token(token)[index]
        else:
            yield token if index < 2 else None


def iter_diff(iterable, iter_type, skip_empty=True):
    if skip_empty:
        return filter(None, _iter_diff(iterable, iter_type))
    else:
        return _iter_diff(iterable, iter_type)


def diff_to_parallel(text, return_list=False):
    text = text.strip()
    before, after = iter_diff(text, 'delete'), iter_diff(text, 'insert')
    if return_list:
        return tuple(before), tuple(after)
    else:
        return ' '.join(before), ' '.join(after)
