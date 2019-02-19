# crossword-helper

## `align.py`

Given a list of words, suggests good alignments.
Bigrams are generated from your input, so if an alignment is suggested,
there is at least one word in your input that could satisfy each overlapping position.
Better alignments are given first.

```
$ ./align.py fixtures/months.txt | head -n8
 november
december

     march
february

    march
january
```

## `transpose.py`

Transpose blocks separated by blank lines.

```
$ python -c 'print("abc\nxyz\n\nax\nby\ncz")' | ./transpose.py
ax
by
cz

abc
xyz
```
