# crossword-helper

## `align.py`

Given a list of words, suggests good alignments.
Bigrams are generated from your input, so if an alignment is suggested,
there is at least one word in your input that could satisfy each overlapping position.
Better alignments are given first.

```
$ echo $'january\nfebruary\nmarch\napril\nmay' | ./align.py
     march
february

    march
january

 march
may

       april
february

      april
january

 january
may

  april
may
```

## `transpose.py`

Transpose blocks separated by blank lines.

```
$ echo $'abc\nxyz\n\nax\nby\ncz' | ./transpose.py
ax
by
cz

abc
xyz
```
