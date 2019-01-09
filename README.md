# crossword-helper

Given a list of words, suggests good alignments for crossword puzzles.
Bigrams are generated from your input, so if an alignment is suggested,
there is at least one word in your input that could satisfy each overlapping position.
Better alignments are given first. Scores are subject to change.

```
$ grep '^...$' /usr/share/dict/words | ./align.py | head
29400:
taa
ann
29400:
ara
nan
25725:
aha
non
```
