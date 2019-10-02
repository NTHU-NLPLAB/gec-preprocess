#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import deque
from itertools import chain

from .sent_tokenize_lm import sent_tokenize, word_tokenize
from .utils import recover_quotewords
from ..format.utils import restore_line_break, nested_html_unescape, normalize_hash
from ..format.diff import parse_diff_token, gen_diff_token


def tokenize_edit(edit_token):
    delete, insert, err_type = parse_diff_token(edit_token)
    # normalize line breaks in edit tokens and space for segmenting
    delete = restore_line_break(nested_html_unescape(delete), replacement=' <br> ')
    insert = restore_line_break(nested_html_unescape(insert), replacement=' <br> ')
    # tokenize text in edit token
    delete = word_tokenize(delete, return_str=True)
    insert = word_tokenize(insert, return_str=True)
    return gen_diff_token(delete, insert, err_type)


def mask_edits(text):
    edits = deque()
    tokens = deque()

    for token in text.split(' '):
        token = token.strip()
        if token.startswith('{+') or token.startswith('[-'):
            tokens.append('{}')
            edits.append(tokenize_edit(token))
        elif token:
            # add space around hash tokens for segmenting
            token = token.replace('###', ' ### ')
            # add space to parentheses for segmenting
            token = token.replace('(', ' ( ').replace(')', ' ) ')
            # escape braces `{}`
            token = token.replace('{', ' {{ ').replace('}', ' }} ')
            tokens.append(token)

    return ' '.join(' '.join(tokens).split()), edits


def tokenize_doc(text):
    # mask edit tokens first to avoid being segmented
    # I have {+a+} pen. => I have {} pen.
    text_masked, edits = mask_edits(text)

    # unescape html and restore line breaks
    text_masked = restore_line_break(nested_html_unescape(text_masked))

    paragraphs = map(str.strip, text_masked.splitlines())
    # tokenize paragraph
    paragraphs = map(sent_tokenize, paragraphs)
    # chain lines in all paragraphs
    sents = chain(*paragraphs)

    # restore masked edit
    return '\n'.join(sents).format(*edits).splitlines()


def tokenize_diff_text(text):
    text = normalize_hash(text)
    text = recover_quotewords(text)
    return tokenize_doc(text)


def main(iterable):
    for doc in iterable:
        for sentence in tokenize_doc(doc):
            print(sentence)


if __name__ == '__main__':
    import logging
    import fileinput
    logging.basicConfig(level=logging.INFO)
    main(map(str.strip, fileinput.input()))
