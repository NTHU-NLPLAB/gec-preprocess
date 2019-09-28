# -*- coding: utf-8 -*-
import re
import sys
from bs4 import BeautifulSoup

from ..utils import restore_xml_escape


edit_re = re.compile(r'<NS type="\w+">(((?!<NS).)*?)</NS>')


def parse_edit(ns_token):
    soup = BeautifulSoup(ns_token, 'lxml-xml')
    err_type = soup.select_one('NS').attrs.get('type', '')
    i_node = soup.select_one('i')
    ori = i_node.text if i_node else ''
    c_node = soup.select_one('c')
    cor = c_node.text if c_node else ''
    return ori, cor, err_type


def gen_edit_token(ori, cor, err_type):
    edit_token = ''

    # format
    ori = ori.strip().replace(' ', '\u3000')
    cor = cor.strip().replace(' ', '\u3000')
    err_type = err_type.replace(' and ', ',')

    if ori:  # delete
        edit_token += f'[-{ori}//{err_type}-]'
    if cor:  # insert
        edit_token += f'{{+{cor}//{err_type}+}}'
    return edit_token


def fce_to_wdiff(text, ignore_type=[]):
    while edit_re.search(text):
        for match in edit_re.finditer(text):
            ns_token = match.group(0)
            ori, cor, err_type = parse_edit(ns_token)
            edit_token = gen_edit_token(ori, cor, err_type)
            text = text.replace(ns_token, f' {edit_token} ')

    # remove consecutive spaces
    text = ' '.join(token for token in text.split(' ') if token)
    # restore escaped symbols
    text = restore_xml_escape(text)
    return text


def main():
    ignore_type = set(sys.argv[1:])

    for line in sys.stdin:
        line = line.strip()
        if line.startswith('<p>') and line.endswith('</p>'):
            paragraph = line[3:-4]
            print(fce_to_wdiff(paragraph, ignore_type))


if __name__ == '__main__':
    main()
