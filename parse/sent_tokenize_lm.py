#!/usr/bin/python
# -*- coding: utf-8 -*-
from itertools import chain, combinations
import kenlm
import string
import os
import re
import fileinput
import logging

from .spacy_tokenize import word_tokenize
from nltk import sent_tokenize as nltk_sent_tokenize
from nltk import wordpunct_tokenize


SEP_RE = re.compile(r'((\s*[\.\!\?])+(\s*[\"\'\,])*)+')
MASK_RE = re.compile(r'\s*\{\}\s*')


def _nltk_sent_tokenize(text):
    # sent tokenize using existing tokenizer first
    sents = nltk_sent_tokenize(text)
    # recover bad tokenization in nltk when faced with 3 or more ! and ?
    if len(sents) > 1 and sents[-1].strip() in ('!', '?'):
        sents[-2] += sents[-1]
        del sents[-1]
    return sents


def _sent_tokenize(text):
    text = text.strip()
    sep_indice = [m.end() for m in SEP_RE.finditer(text) if m.start() > 0 and len(m.group(0).strip()) > 1]
    return separate_text(text, sep_indice, tokenize_word=False)


def pre_tokenize_normalize(text):
    text = text.strip()
    # add space to the last sent separator match
    end_sep = [m.group(0) for m in SEP_RE.finditer(text) if m.end() == len(text)]
    if end_sep:
        # right-most replace
        text = f' {end_sep[0]}'.join(text.rsplit(end_sep[0], 1))
    # add space between numeric sequences and commas
    text = re.sub(r'([^ 0-9\+\-]),', r'\g<1> ,', text)
    # add space after commas
    text = re.sub(r'( ,)([^ ])', r' \g<1> \g<2>', text)
    return text


# capitalize and tokenize
def capitokenize(text, return_list=False):
    text = pre_tokenize_normalize(text)
    tokens = word_tokenize(text.strip())
    if tokens:
        for ch in tokens[0]:
            if ch in string.ascii_letters:
                tokens[0] = tokens[0].replace(ch, ch.upper(), 1)
                break
    return tokens if return_list else ' '.join(tokens)


def separate_text(text, indice, tokenize_word=True):
    # assume the indice is already sorted
    # indice = sorted(indice)
    sep_indice = [0, *indice] if indice and indice[-1] == len(text) else [0, *indice, None]
    texts = (text[start:end].strip() for start, end in zip(sep_indice, sep_indice[1:]))
    return list(map(capitokenize, texts) if tokenize_word else texts)


def sent_score(text, word_tokenized=True):
    text = text if word_tokenized else capitokenize(text)
    # remove masked tokens
    text = MASK_RE.sub(' ', text)
    text = ' '.join(wordpunct_tokenize(text))
    score = lm.score(text)
    logging.info(f'{score}: {text}')
    return score


def sents_score(sents, word_tokenized=True):
    return sum(sent_score(sent, word_tokenized) for sent in sents)


def try_sep_all(text, tokenize_word=True):
    sep_indice = [m.end() for m in SEP_RE.finditer(text) if m.start() > 0]
    # sep_indice.remove(len(text))
    # generate possible combinations of cut
    sep_candidates = chain(*(combinations(sep_indice, n+1) for n in range(len(sep_indice))))
    candidates = [separate_text(text, sep_indice, tokenize_word) for sep_indice in sep_candidates]
    return max(candidates, key=sents_score)


def try_sep(text, index, tokenize_word=True):
    # f_sent, r_sent = capitokenize(text[:index]), capitokenize(text[index:])
    sents = separate_text(text, [index], tokenize_word)

    if sents_score(sents, tokenize_word) + 1 > sent_score(text, False):
        yield sents[0]
        text = sents[-1]
        index = 0

    for sent in seperate_sents(text, index, tokenize_word):
        yield sent


def seperate_sents(text, start=0, tokenize_word=True):
    text = text.strip()
    m = SEP_RE.search(text, start)
    if not m or m.end() == len(text):
        yield capitokenize(text) if tokenize_word else text
    elif m.start() == 0:
        for sent in seperate_sents(text, m.end(), tokenize_word):
            yield sent
    else:
        for sent in try_sep(text, m.end(), tokenize_word):
            yield sent


def sent_tokenize(text, tokenize_word=True, pre_sent_tokenize=None):
    text = text.strip()
    sents = pre_sent_tokenize(text) if pre_sent_tokenize else [text]

    for sent in sents:
        # aggresively tokenize sentences and validate using LM
        for sent_candidate in seperate_sents(sent, tokenize_word=tokenize_word):
            yield sent_candidate


lm = kenlm.Model(os.environ.get('KENLM_MODEL', 'bnc.punct.bin'))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    for line in map(str.strip, fileinput.input()):
        for sent in sent_tokenize(line):
            print(sent)
