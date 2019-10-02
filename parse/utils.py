#!/usr/bin/python
# -*- coding: utf-8 -*-


RECOVER_ITEM = [
    ("n 't ", "n't ")
]


def recover_quotewords(text):
    for before, after in RECOVER_ITEM:
        text = text.replace(before, after)
    return text
