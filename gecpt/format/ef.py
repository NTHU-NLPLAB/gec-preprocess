# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from .edit import Edit


EF_EDIT_RE = re.compile(r'<change>(((?!<change>).)*?)</change>')
EF_TOKEN = (
    "<change><selection>{delete}</selection>"
    "<tag><symbol>{err_type}</symbol><correct>{insert}</correct></tag>"
    "</change>"
)


def parse_ef_token(content):
    soup = BeautifulSoup(content, 'lxml')
    # TODO: ".text" vs. ".decode_contents"
    original = soup.select_one('selection').decode_contents().strip()
    corrected = soup.select_one('tag correct').decode_contents().strip()
    error_type = soup.select_one('tag symbol').decode_contents().strip()

    # replace ` and ` to commas
    error_type = error_type.replace(' and ', ',')
    return Edit(original, corrected, error_type)


def gen_ef_token(edit: Edit):
    return EF_TOKEN.format(**edit._asdict())


def iter_ef_file(iterator):
    stack, in_text = [], False
    for line in map(str.strip, iterator):
        if line == '<text>':
            in_text = True
        elif line == '</text>':
            if stack:
                yield stack
            stack, in_text = [], False
        elif line and in_text:
            stack.append(line)
