# -*- coding: utf-8 -*-
import fileinput


def iter_writings(iterator):
    stack = []
    in_text = False
    for line in iterator:
        line = line.strip()
        if line == '<text>':
            in_text = True
        elif line == '</text>':
            if stack:
                yield stack
            stack = []
            in_text = False
        elif line and in_text:
            stack.append(line)


if __name__ == '__main__':
    for texts in iter_writings(fileinput.input()):
        for text in texts:
            print(text)
