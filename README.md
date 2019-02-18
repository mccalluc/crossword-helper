# crossword-helper

Given a list of words, suggests good alignments for crossword puzzles.
Bigrams are generated from your input, so if an alignment is suggested,
there is at least one word in your input that could satisfy each overlapping position.
Better alignments are given first. Scores are subject to change.

```
$ echo $'january\nfebruary\nmarch\napril\nmay' | ./align.py
12:
     march
february
12:
    march
january
2:
 march
may
1:
       april
february
1:
      april
january
1:
 january
may
1:
  april
may
```
