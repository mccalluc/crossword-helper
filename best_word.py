from collections import defaultdict
from math import log2

def best_word(sequence, words, on_top=True):
    '''
    Given a sequence of characters, and a list of words,
    and a flag which indicates whether the word we seek is above
    or below the sequence,
    returns the word and an offset which produces the best bigrams.
    
    >>> words = {'boy', 'aka', 'abba', 'book', 'year', 'tab'}
    >>> best_word('oboe', words)
    ('abba', 2)
    
    >>> best_word('oboe', words, on_top=False)
    ('book', 1)
    '''
    all_bigrams = bigrams(words)
    best_score = 0
    best_word = None
    best_offset = None
    for word in words:
        for offset, overlap in offset_overlaps(sequence, word):
            pair_bigrams = (
                alignment_bigrams(overlap, sequence)
                if on_top else
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
    0.0
    >>> score(['ab', 'cd'], all_bigrams)
    2.0
    >>> score(['ab', 'cd', 'xy'], all_bigrams)
    -inf
    '''
    counts = [all_bigrams[bg] for bg in pair_bigrams if ' ' not in bg]
    return combine_counts(counts)

def combine_counts(counts):
    '''
    Given a set of counts, returns an aggregate score.
    
    >>> combine_counts([2,0])
    -inf
    >>> combine_counts([2,2])
    2.0
    >>> combine_counts([1,2,4])
    3.0
    '''
    if 0 in counts:
        return -float('inf')
    logs = [log2(count) for count in counts]
    return sum(logs)    
            
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
