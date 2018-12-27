from collections import defaultdict
from math import log2

def best_word(sequence, words, on_top=True):
    '''
    Given a sequence of characters, and a list of words,
    and a flag which indicates whether the word we seek is above
    or below the sequence,
    returns the word and an offset which produces the best bigrams.
    
    >>> best_word('c', ['cat', 'hat'], False)
    ('cat', -1)
    '''
    bg = bigrams(words)
    best_score = 0
    best_word = None
    best_offset = None
    for word in words:
        for offset, overlap in offset_overlaps(sequence, word):
            pass
            
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
    '''
    padding = ' ' * (len(sequence) - 1)
    padded_word = padding + word + padding
    return [
        padded_word[offset:offset + len(sequence)]
        for offset in range(len(padded_word) - 2)
    ]
    
def bigrams(words):
    '''
    Returns a dict of bigram counts in the set of words.
    
    >>> bg = bigrams(['cat', 'mat'])
    >>> bg['ca']
    1
    >>> bg['at']
    2
    >>> bg['zz']
    0
    '''
    counts = defaultdict(int)
    for word in words:
        for i in range(len(word)):
            counts[word[i:i+2]] += 1
    return counts
    
def combine_counts(counts):
    '''
    Given a set of counts, returns an aggregate score.
    (For now, it's the geometric mean.)
    
    >>> combine_counts([2,0])
    0.0
    >>> combine_counts([2,2])
    2.0
    >>> combine_counts([1,2,4])
    2.0
    '''
    if 0 in counts:
        return 0.0
    logs = [log2(count) for count in counts]
    return 2 ** (sum(logs) / len(logs))
