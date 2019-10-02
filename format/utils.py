#!/usr/bin/python
# -*- coding: utf-8 -*-
import html
import re


HASH_RE = re.compile(r'#(#|\s|-|\(|\))+#')
NEWLINE_RE = re.compile(r'<br>|<br/>|<br\s+/>|\r\n|\n|\r|\v|\f|\u2028|\u2029')


def nested_html_unescape(text):
    text, unescaped = html.unescape(text), text
    while text != unescaped:
        text, unescaped = html.unescape(text), text
    return text


def restore_line_break(text, replacement='\n'):
    return NEWLINE_RE.sub(replacement, text).strip()


def normalize_hash(text, replacement='###'):
    return HASH_RE.sub(replacement, text)


def restore_escaped_symbols(text):
    while '&amp;' in text:
        text = text.replace('&amp;', '&')
    text = text.replace('&nbsp;', ' ')
    return text


def restore_xml_escape(text):
    while '&amp;' in text:
        text = text.replace('&amp;', '&')
    text = text.replace('&quote;', '"')
    text = text.replace('&quot;', '"')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text
