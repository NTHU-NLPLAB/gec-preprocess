#!/usr/bin/python
# -*- coding: utf-8 -*-

RESERVED_TOKENS = (
    "{}", "{{", "}}", "###", "<br/>", "<br>", "<br />", "'m", "'s", "'ll", "'ve", "'d", "'clock", "'re", "'t"
)


def init_tokenizer():
    # import spacy
    # import os
    from spacy.lang.en import English
    from spacy.attrs import ORTH
    # nlp = spacy.load(os.environ.get('SPACY_MODEL', 'en'), disable=['tagger', 'ner'])
    # TODO: this may have compatibility issue
    tokenizer = English().Defaults.create_tokenizer()
    #  add special segmenting case for spacy tokenizer
    tokenizer.add_special_case('I.',  [{ORTH: "I"}, {ORTH: "."}])
    for token in RESERVED_TOKENS:
        tokenizer.add_special_case(token, [{ORTH: token}])
    return tokenizer


def word_tokenize(text, return_list=True, return_str=False):
    return_list = False if return_str else return_list
    # remove consective spaces
    text = ' '.join(text.split())
    tokens = (token.text for token in _tokenizer(text))
    return list(tokens) if return_list else ' '.join(tokens)


def sent_tokenize(text):
    return [sent.text.strip() for sent in _tokenizer(text).sents]


_tokenizer = init_tokenizer()
