# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from .edit import Edit


FCE_EDIT_RE = re.compile(r'<NS type="\w+">(((?!<NS).)*?)</NS>')


def parse_ns_token(ns_token):
    ns_node = BeautifulSoup(ns_token, 'lxml-xml').NS
    assert ns_node is not None

    err_type = ns_node.attrs.get('type', '').strip()

    if ns_node.i is None and ns_node.c is None:
        # error is detected but not edited
        ori = cor = ns_node.decode_contents().strip()
    else:
        ori = ns_node.i.decode_contents().strip() if ns_node.i else ''
        cor = ns_node.c.decode_contents().strip() if ns_node.c else ''

    return Edit(ori, cor, err_type)


def gen_ns_token(edit: Edit):
    content = ''
    if edit.delete:
        content += f"<i>{edit.delete}</i>"
    if edit.insert:
        content += f"<c>{edit.insert}</c>"
    return f"<NS type=\"{edit.err_type}\">{content}</NS>"


def iter_fce_file(iterable):
    for line in map(str.strip, iterable):
        if line.startswith('<p>') and line.endswith('</p>'):
            yield line[3:-4]
