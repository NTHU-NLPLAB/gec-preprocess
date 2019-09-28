# -*- coding: utf-8 -*-
import re


EDIT_RE = re.compile(r'(\[-(?P<delete>[^ ]*?)-\]|\{\+(?P<insert>[^ ]*?)\+\})+(\((?P<type>[A-Za-z,]+)\))?')


def gen_diff_token(delete, insert, err_type='', space_escape='\u3000'):
    diff_token = ''
    if delete:
        diff_token += f"[-{delete.replace(' ', space_escape)}-]"
    if insert:
        diff_token += f"{{+{insert.replace(' ', space_escape)}+}}"
    if diff_token and err_type:
        diff_token += f"({err_type.replace(' ', space_escape)})"
    return diff_token


def parse_diff_token(edit_token, space_escape='\u3000'):
    match = EDIT_RE.match(edit_token)
    assert match, f'"{edit_token}" is not a valid edit token'
    delete, insert, err_type = match.group('delete') or '', match.group('insert') or '', match.group('type') or ''
    delete = delete.replace(space_escape, ' ')
    insert = insert.replace(space_escape, ' ')
    err_type = err_type.replace(space_escape, ' ')
    return delete, insert, err_type


def iter_edit(text, iter_type):
    index = ('delete', 'insert', 'error').index(iter_type)
    for token in text.split(' '):
        if token.startswith('{+') or token.startswith('[-'):
            items = parse_diff_token(token)
            if items[index]:
                yield items[index]
        else:
            yield token
