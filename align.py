#!/usr/bin/env python

from collections import defaultdict, namedtuple
from sys import argv, stdin


def pretty_best_pairs(words):
    '''
    Returns a string representing the best alignments of a set of words.

    >>> words = ['abc', 'bcd']
    >>> print(pretty_best_pairs(words))
      bcd
    abc
    <BLANKLINE>
    abc
    bcd
    '''
    alignments = []
    for scored_pairs in best_pairs(words):
        for (pair, score) in scored_pairs.alignments:
            alignments.append((score, scored_pairs.word, pair[0], pair[1]))
    alignments.sort(key=lambda t: -t[0])
    return '\n\n'.join([
        pretty_offset(t[1], t[2], t[3], True) for t in alignments
    ])


def pretty_offset(sequence, word, offset, swap):
    '''
    >>> words = ['boy', 'aka', 'abba', 'book', 'year', 'tab']
    >>> all_bigrams = bigrams(words)
    >>> sequence = 'oboe'

    >>> swap = True
    >>> alignment_scores = best_words(sequence, words, all_bigrams, swap)
    >>> for alignment_score in alignment_scores:
    ...     (word, offset) = alignment_score.alignment
    ...     print(alignment_score.score, ':')
    ...     print(pretty_offset(sequence, word, offset, swap))
    1 :
     boy
    oboe
    4 :
    abba
      oboe
    1 :
       year
    oboe
    2 :
    tab
      oboe

    >>> swap = False
    >>> alignment_scores = best_words(sequence, words, all_bigrams, swap)
    >>> for alignment_score in alignment_scores:
    ...     (word, offset) = alignment_score.alignment
    ...     print('---')
    ...     print(pretty_offset(sequence, word, offset, swap))
    ---
      oboe
    boy
    ---
    oboe
       aka
    ---
    oboe
     aka
    ---
     oboe
    aka
    ---
    oboe
       abba
    ---
     oboe
    book
    ---
       oboe
    book
    '''
    padding = abs(offset) * ' '
    (padded_sequence, padded_word) = (
        (padding + sequence, word)
        if offset > 0 else
        (sequence, padding + word)
    )
    return '\n'.join(
        [str(padded_word), str(padded_sequence)]
        if swap else
        [str(padded_sequence), str(padded_word)]
    )


def best_pairs(words):
    '''
    Given a set of words, return the best pairs.

    >>> words = ['abcde', 'cdefg', 'efghi']
    >>> best = list(best_pairs(words))
    >>> len(best)
    3
    >>> best[0].word
    'abcde'
    >>> list(best[0].alignments)
    [ScoredAlignment(alignment=('cdefg', -3), score=4)]
    '''
    all_bigrams = bigrams(words)
    for word in sorted(words):
        yield ScoredPairs(
            word,
            best_words(word, [w for w in words if w != word], all_bigrams)
        )


ScoredPairs = namedtuple('ScoredPairs', ['word', 'alignments'])


def best_words(sequence, words, all_bigrams, swap=True):
    '''
    Given a sequence of characters, and a list of words,
    and a dict of bigram frequencies,
    and a flag which indicates whether the word we seek is before
    or after the sequence,
    returns word-offset pairs, along with their scores.

    >>> words = ['boy', 'aka', 'abba', 'book', 'year', 'tab']
    >>> all_bigrams = bigrams(words)
    >>> [(a.alignment, a.score) for a in
    ...  best_words('oboe', words, all_bigrams)]
    [(('boy', -1), 1), (('abba', 2), 4), (('year', -3), 1), (('tab', 2), 2)]

    >>> alpha = 'abcd'
    >>> [(a.alignment, a.score) for a in
    ...  best_words(alpha, {alpha}, bigrams({alpha}), swap=True)]
    [(('abcd', -1), 1)]
    >>> [(a.alignment, a.score) for a in
    ...  best_words(alpha, {alpha}, bigrams({alpha}), swap=False)]
    [(('abcd', 1), 1)]

    If order matters, supply a list.

    >>> words = ['abcde', 'cdefg', 'efghi']
    >>> [(a.alignment, a.score) for a in
    ...  best_words('abcde', words, bigrams(words))]
    [(('abcde', -1), 4), (('cdefg', -3), 4)]
    '''
    for word in words:
        for offset, overlap in offset_overlaps(sequence, word):
            pair_bigrams = (
                alignment_bigrams(overlap, sequence)
                if swap else
                alignment_bigrams(sequence, overlap)
            )
            this_score = score(pair_bigrams, all_bigrams)
            if this_score > 0:
                yield ScoredAlignment((word, offset), this_score)


ScoredAlignment = namedtuple('ScoredAlignment', ['alignment', 'score'])


def score(pair_bigrams, all_bigrams):
    '''
    Returns an aggregate score for a set of bigrams,
    against a defaultdict of all bigrams.
    Bigrams with spaces are ignored.

    >>> all_bigrams = defaultdict(int, {'ab': 1, 'cd': 4})
    >>> score(['ab', 'a ', ' a'], all_bigrams)
    1
    >>> score(['ab', 'cd'], all_bigrams)
    4
    >>> score(['ab', 'cd', 'xy'], all_bigrams)
    0
    '''
    counts = [all_bigrams[bg] for bg in pair_bigrams if ' ' not in bg]
    return combine_counts(counts)


def combine_counts(counts):
    '''
    Given a set of counts, returns an aggregate score.

    >>> combine_counts([2,0])
    0
    >>> combine_counts([2,2])
    4
    >>> combine_counts([1,2,4])
    8
    '''
    product = 1
    for count in counts:
        product *= count
    return product


def alignment_bigrams(a_str, b_str):
    '''
    Given two strings of equal length,
    return the bigrams of their alignment.

    >>> alignment_bigrams('abc', 'xyz')
    ['ax', 'by', 'cz']
    '''
    return [a + b for a, b in zip(a_str, b_str)]


def offset_overlaps(sequence, word):
    '''
    Return offsets and overlaps of word against sequence.

    >>> list(offset_overlaps('abc','xy'))
    [(-2, '  x'), (-1, ' xy'), (0, 'xy '), (1, 'y  ')]

    >>> list(offset_overlaps('a','xyz'))
    [(0, 'x'), (1, 'y'), (2, 'z')]
    '''
    for i, overlap in enumerate(overlaps(sequence, word)):
        yield (i - len(sequence) + 1, overlap)


def overlaps(sequence, word):
    '''
    Returns all the possible alignments of word against sequence.

    >>> list(overlaps('hat', 'cat'))
    ['  c', ' ca', 'cat', 'at ', 't  ']

    >>> list(overlaps('x', 'abcdefg'))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    >>> list(overlaps('abc', 'x'))
    ['  x', ' x ', 'x  ']
    '''
    word_padding = ' ' * (len(sequence) - 1)
    padded_word = word_padding + word + word_padding
    for offset in range(len(word) + len(sequence) - 1):
        yield padded_word[offset:offset + len(sequence)]


def bigrams(words):
    '''
    Returns a dict of bigram counts in the set of words.

    >>> bg = bigrams(['cat', 'mat'])
    >>> bg['ca']
    1
    >>> bg['at']
    2
    >>> dict(bg)
    {'ca': 1, 'at': 2, 'ma': 1}
    '''
    counts = defaultdict(int)
    for word in words:
        for i in range(len(word) - 1):
            counts[word[i:i+2]] += 1
    return counts


if __name__ == '__main__':
    if len(argv) > 2:
        raise Exception('At most one argument allowed')
    with open(argv[1]) if len(argv) == 2 else stdin as f:
        lines = [line.strip() for line in f.readlines()]
        print(pretty_best_pairs(lines))
