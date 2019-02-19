#!/usr/bin/env python

from sys import argv
import subprocess

# This has been done before, but the modules languished in python2-land.
# None seem to be currently supported.
#
# https://pythonhosted.org/doctest2/
#   Can't load dependencies.
# https://github.com/wapcaplet/doctest2
#   Stub project.
# https://bitbucket.org/michilu/shell-doctest
#   Python2 syntax.


def teststring(input_output):
    lines = input_output.splitlines()
    while len(lines):
        line = lines.pop(0)
        if line[0:2] == '$ ':
            command = line[2:]
            result = subprocess.run(
                command, shell=True,
                check=True, capture_output=True, text=True)
            actual_lines = result.stdout.splitlines()
            for actual_line in actual_lines:
                expected_line = lines.pop(0)
                if actual_line != expected_line:
                    raise Exception(
                        'Expected "{}"; got "{}".\nFull output:\n{}'.format(
                            expected_line,
                            actual_line,
                            '\n'.join(actual_lines)))


def testfile(filename):
    with open(filename) as f:
        return teststring(f.read())


if __name__ == '__main__':
    if len(argv) != 2:
        raise Exception('Expected one argument')
    testfile(argv[1])
