#!/usr/bin/python
# -*- coding: utf-8 -*-
from .diff import parse_diff_token, gen_diff_token, iter_diff, DIFF_EDIT_RE, diff_to_parallel
from .ef import parse_ef_token, gen_ef_token, iter_ef_file, EF_EDIT_RE
from .fce import parse_ns_token, gen_ns_token, iter_fce_file, FCE_EDIT_RE
from .m2 import parse_m2_token, gen_m2_token, iter_m2, parse_m2_record, iter_m2_file


__all__ = [
    'parse_diff_token', 'gen_diff_token', 'iter_diff', 'DIFF_EDIT_RE', 'diff_to_parallel',
    'parse_ef_token', 'gen_ef_token', 'iter_ef_file', 'EF_EDIT_RE',
    'parse_ns_token', 'gen_ns_token', 'iter_fce_file', 'FCE_EDIT_RE',
    'parse_m2_token', 'gen_m2_token', 'iter_m2', 'parse_m2_record', 'iter_m2_file',
    'convert_m2', 'convert_ef', 'convert_fce',
]


def convert_m2(sent, edits, to='diff', ignore_type=()):
    if to == 'diff':
        edit_token_func = gen_diff_token
    elif to == 'ef':
        edit_token_func = gen_ef_token
    elif to == 'fce':
        edit_token_func = gen_ns_token
    else:
        return ' '.join(iter_m2(sent, edits))
    return ' '.join(iter_m2(sent, edits, edit_token_func, ignore_type=ignore_type))


def convert_ef(text, to='diff', ignore_type=()):
    return _convert_xml_to(text, EF_EDIT_RE, parse_ef_token, to=to, ignore_type=ignore_type)


def convert_fce(text, to='diff', ignore_type=()):
    return _convert_xml_to(text, FCE_EDIT_RE, parse_ns_token, to=to, ignore_type=ignore_type)


def _convert_xml(xmltext, edit_re, parse_edit, edit_token_func, ignore_type=()):
    text = xmltext.strip()
    # nested edit
    while edit_re.search(text):
        change_tokens = {match.group(0) for match in edit_re.finditer(text)}
        for change_token in change_tokens:
            original, corrected, error_type = parse_edit(change_token)

            # try to flattern nested edits
            original = ' '.join(iter_diff(original, 'delete'))
            corrected = ' '.join(iter_diff(corrected, 'insert'))

            # if the error is to be ignored
            if any(t in ignore_type for t in error_type.split(',')):
                token = corrected
            else:
                token = edit_token_func(original, corrected, error_type)
            text = text.replace(change_token, f' {token} ')

    # remove consecutive spaces
    return ' '.join(filter(None, text.split(' ')))


def _convert_xml_to(xmltext, edit_re, parse_edit, to='diff', ignore_type=()):
    if to == 'diff':
        edit_token_func = gen_diff_token
    elif to == 'ef':
        edit_token_func = gen_ef_token
    elif to == 'fce':
        edit_token_func = gen_ns_token
    # else:
    #     edit_token_func = lambda *args: args[1]
    return _convert_xml(xmltext, edit_re, parse_edit, edit_token_func, ignore_type=())


def main(input_file, from_format, to, ignore_type=()):
    if from_format == 'ef':
        for paragraph in iter_ef_file(input_file):
            for text in paragraph:
                print(convert_ef(text, to=to, ignore_type=ignore_type))
    elif from_format == 'fce':
        for text in iter_fce_file(input_file):
            print(convert_fce(text, to=to, ignore_type=ignore_type))
    elif from_format == 'm2':
        for m2_records in iter_m2_file(input_file):
            for sent, edits in parse_m2_record(m2_records):
                print(convert_m2(sent, edits, to=to, ignore_type=ignore_type))
    elif from_format == 'parallel':
        # TODO: implement
        pass
    elif from_format == 'diff':
        # TODO: implement
        pass
    else:
        # TODO: throw exception
        pass
