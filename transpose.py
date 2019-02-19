#!/usr/bin/env python

from sys import argv, stdin


def transpose(lines):
    '''
    >>> transpose(['  x', ' ay', '1bz', '2c', '3'])
    ['  123', ' abc ', 'xyz  ']
    '''
    max_len = max([len(s) for s in lines])
    padded_lines = [line.ljust(max_len) for line in lines]
    return [
        ''.join([line[col] for line in padded_lines])
        for col in range(max_len)
    ]


if __name__ == '__main__':
    if len(argv) > 2:
        raise Exception('At most one argument allowed')
    with open(argv[1]) if len(argv) == 2 else stdin as f:
        block = []
        for line in f.readlines():
            line = line.strip()
            if line:
                block.append(line)
            else:
                print('\n'.join(transpose(block)))
                print()
                block = []
        print('\n'.join(transpose(block)))
