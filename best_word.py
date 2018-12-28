from collections import defaultdict
from math import log2


def pretty(sequence, words, swap=True):
    '''
    Returns a string representing an alignment of sequence
    against one word.

    # >>> words = {'boy', 'aka', 'abba', 'book', 'year', 'tab'}
    # >>> print(pretty('oboe', words, swap=True))
    # abba
    #   oboe
    # >>> print(pretty('oboe', words, swap=False))
    #  oboe
    # book
    '''
    all_bigrams = bigrams(words)
    (word, offset) = best_word(sequence, words, all_bigrams, swap)
    padding = abs(offset) * ' '
    (padded_sequence, padded_word) = (
        (padding + sequence, word)
        if offset > 0 else
        (sequence, padding + word)
    )
    return '\n'.join(
        [padded_word, padded_sequence]
        if swap else
        [padded_sequence, padded_word]
    )


def best_word(sequence, words, all_bigrams, swap=True):
    '''
    Given a sequence of characters, and a list of words,
    and a dict of bigram frequencies,
    and a flag which indicates whether the word we seek is before
    or after the sequence,
    returns the word and an offset which produces the best bigrams.

    >>> words = {'boy', 'aka', 'abba', 'book', 'year', 'tab'}
    >>> all_bigrams = bigrams(words)
    >>> best_word('oboe', words, all_bigrams)
    ('abba', 2)

    >>> best_word('oboe', words, all_bigrams, swap=False)
    ('book', 1)

    >>> alpha = 'abcd'
    >>> best_word(alpha, {alpha}, bigrams({alpha}), swap=True)
    ('abcd', -1)
    >>> best_word(alpha, {alpha}, bigrams({alpha}), swap=False)
    ('abcd', 1)
    '''
    best_score = 0
    best_word = None
    best_offset = None
    for word in words:
        for offset, overlap in offset_overlaps(sequence, word):
            pair_bigrams = (
                alignment_bigrams(overlap, sequence)
                if swap else
                alignment_bigrams(sequence, overlap)
            )
            this_score = score(pair_bigrams, all_bigrams)
            if this_score > best_score:
                best_score = this_score
                best_word = word
                best_offset = offset
    return (best_word, best_offset)


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

    >>> offset_overlaps('abc','xy')
    [(-2, '  x'), (-1, ' xy'), (0, 'xy '), (1, 'y  ')]

    >>> offset_overlaps('a','xyz')
    [(0, 'x'), (1, 'y'), (2, 'z')]
    '''
    return [
        (i - len(sequence) + 1, overlap)
        for i, overlap in enumerate(overlaps(sequence, word))
    ]


def overlaps(sequence, word):
    '''
    Returns all the possible alignments of word against sequence.

    >>> overlaps('hat', 'cat')
    ['  c', ' ca', 'cat', 'at ', 't  ']

    >>> overlaps('x', 'abcdefg')
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    >>> overlaps('abc', 'x')
    ['  x', ' x ', 'x  ']
    '''
    word_padding = ' ' * (len(sequence) - 1)
    padded_word = word_padding + word + word_padding
    return [
        padded_word[offset:offset + len(sequence)]
        for offset in range(len(word) + len(sequence) - 1)
    ]


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
