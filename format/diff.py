# -*- coding: utf-8 -*-
import re


EDIT_RE = re.compile(r'(\[-(?P<delete>[^ ]*?)-\]|\{\+(?P<insert>[^ ]*?)\+\})+(\((?P<type>[^)]+)\))?')


def gen_diff_token(delete, insert, err_type=None, space_escape='\u3000'):
    diff_token = ''
    if delete:
        diff_token += f"[-{space_escape.join(delete.split())}-]"
    if insert:
        diff_token += f"{{+{space_escape.join(insert.split())}+}}"
    if diff_token and err_type:
        diff_token += f"({space_escape.join(err_type.split())})"
    return diff_token


def parse_diff_token(edit_token):
    match = EDIT_RE.match(edit_token)
    assert match, f'"{edit_token}" is not a valid edit token'
    delete, insert, err_type = match.group('delete'), match.group('insert'), match.group('type')
    delete = ' '.join(delete.split()) if delete else ''
    insert = ' '.join(insert.split()) if insert else ''
    err_type = ' '.join(err_type.split()) if err_type else ''
    return delete, insert, err_type


def iter_edit(text, iter_type, skip_empty=True):
    index = ('delete', 'insert', 'error').index(iter_type)
    for token in filter(None, text.split(' ')):
        if token.startswith('{+') or token.startswith('[-'):
            items = parse_diff_token(token)
        else:
            items = (token, token, None)

        if not skip_empty or items[index]:
            yield items[index]
