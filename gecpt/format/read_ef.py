# -*- coding: utf-8 -*-


def iter_ef_writings(iterator):
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


def main(iterable):
    for texts in iter_ef_writings(iterable):
        for text in texts:
            print(text)


if __name__ == '__main__':
    import fileinput
    main(fileinput.input())

# cat EF201403_selection7.xml | python read_ef.py