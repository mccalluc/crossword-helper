from collections import defaultdict


# def pretty_best_pairs(words):
#     '''
#     Returns a string representing the best alignments of a set of words.
#
#     # >>> words = {'aka', 'abba', 'book'}
#     # >>> print(pretty_best_pairs(words))
#     # book
#     #   book
#     # -----
#     # aka
#     #   book
#     # -----
#     # abba
#     #    book
#     '''
#     pairs = best_pairs(words)
#     return '\n-----\n'.join([
#         pretty_offset(word1, word2, offset, False)
#         for (word1, word2, offset) in pairs
#     ])


def pretty_offset(sequence, word, offset, swap):
    '''
    >>> words = ['boy', 'aka', 'abba', 'book', 'year', 'tab']
    >>> all_bigrams = bigrams(words)
    >>> sequence = 'oboe'

    >>> swap = True
    >>> offsets = best_words(sequence, words, all_bigrams, swap)
    >>> for (word, offset) in offsets:
    ...     print(pretty_offset(sequence, word, offset, swap))
    abba
      oboe

    >>> swap = False
    >>> offsets = best_words(sequence, words, all_bigrams, swap)
    >>> for (word, offset) in offsets:
    ...     print(pretty_offset(sequence, word, offset, swap))
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
        [padded_word, padded_sequence]
        if swap else
        [padded_sequence, padded_word]
    )


def best_pairs(words):
    '''
    Given a set of words, return the best pairs.

    >>> words = ['abcde', 'cdefg', 'efghi']
    >>> best_pairs(words)
    [('abcde', [('abcde', -1), ('cdefg', -3)]), ('cdefg', [('cdefg', -1)]), ('efghi', [('cdefg', 1)])]
    '''
    all_bigrams = bigrams(words)
    return [(word, best_words(word, words, all_bigrams)) for word in sorted(words)]


def best_words(sequence, words, all_bigrams, swap=True):
    '''
    Given a sequence of characters, and a list of words,
    and a dict of bigram frequencies,
    and a flag which indicates whether the word we seek is before
    or after the sequence,
    returns the word and an offset which produces the best bigrams.

    >>> words = {'boy', 'aka', 'abba', 'book', 'year', 'tab'}
    >>> all_bigrams = bigrams(words)
    >>> best_words('oboe', words, all_bigrams)
    [('abba', 2)]

    >>> best_words('oboe', words, all_bigrams, swap=False)
    [('book', 1)]

    >>> alpha = 'abcd'
    >>> best_words(alpha, {alpha}, bigrams({alpha}), swap=True)
    [('abcd', -1)]
    >>> best_words(alpha, {alpha}, bigrams({alpha}), swap=False)
    [('abcd', 1)]

    If order matters, supply a list.

    >>> words = ['abcde', 'cdefg', 'efghi']
    >>> best_words('abcde', words, bigrams(words))
    [('abcde', -1), ('cdefg', -3)]
    '''
    best_score = 0
    best_word_offsets = []
    for word in words:
        for offset, overlap in offset_overlaps(sequence, word):
            pair_bigrams = (
                alignment_bigrams(overlap, sequence)
                if swap else
                alignment_bigrams(sequence, overlap)
            )
            this_score = score(pair_bigrams, all_bigrams)
            if this_score > best_score:
                best_word_offsets = []
            if this_score >= best_score:
                best_score = this_score
                best_word_offsets.append((word, offset))
    return best_word_offsets


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
