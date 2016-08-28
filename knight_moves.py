# INSTRUCTIONS
#
# python knight_moves.py [word_length]
#
# If word length is not provided, the default value of 10 is used

import sys

word_len = int(sys.argv[1]) if len(sys.argv) > 1 else 10

kp = [
    ['a',  'b', 'c', 'd',  'e' ],
    ['f',  'g', 'h', 'i',  'j' ],
    ['k',  'l', 'm', 'n',  'o' ],
    [None, '1', '2', '3',  None]
]

MAX_X = len(kp[0])
MAX_Y = len(kp)

kseq = 'abcdefghijklmno123'
transitions = {}

def load_transitions(keypad):
    '''Build the transition matrix, a mapping of characters to a list
       of the next legal character

    '''
    for x in range(0,MAX_X):
        for y in range(0,MAX_Y):
            r = keypad[y]
            k = r[x]
            if not k:
                continue
            if not k in transitions:
                transitions[k] = []
            for dx in [-2, -1, 1, 2]:
                if abs(dx) == 2:
                    dyr = [-1, 1]
                elif abs(dx) == 1:
                    dyr = [-2, 2]
                for dy in dyr:
                    tx = x + dx
                    ty = y + dy
                    if 0 <= tx and tx < MAX_X and 0 <= ty and ty < MAX_Y:
                        r = keypad[ty]
                        tk = r[tx]
                        if tk:
                            transitions[k].append(tk)

load_transitions(kp)

# store computed results here for fast access
# {(f, l, len): n}
#  f: first key of phone number
#  l: last key of phone number
#  len: length of phone number
#  n: number of valid phone numbers beginning with f, ending with l, of length n
tbl = {}

call_count = 0
def count_words(f, l, n):
    '''A memoized counter of words beginning with f(irst), ending in
    l(ast), of length n.  The cost of count_words is proportional to
    the size of the memo table tbl, times the cost of building the
    table. Tbl size is n * size(f,l), where size(f,l) is the number of
    transitions from f to l, or the count of transitions in the
    transition matrix. Taking a measurement, table size is about 320
    * n. The cost of adding an entry to the table is O(n), so the cost
    of the algorithm is O(n**2).

    '''
    global call_count
    call_count += 1
    k = (f, l, n)
    if not k in tbl:
        tbl[k] = 0
        # fill out the table, from length 2 to length n
        for nn in range(2, n+1):
            if nn == 2 and l in transitions[f]:
                # base case: length is 2 and you can get to l from f
                # there is only one word for a pair, so set (f, l, 2) -> 1
                tbl[(f, l, nn)] = 1
            else:
                # Length is 3 or more. Sum up the counts for for length
                # nn-1, for each transition char that can follow f
                tbl[(f, l, nn)] = 0
                for c in transitions[f]:
                    tbl[(f, l, nn)] += count_words(c, l, nn - 1)
    return tbl[k]

def add_char(prefix):
    # create a list of words beginning with prefix and ending with the
    # transitions associated to the last char of the prefix
    # e.g. add_char("b") -> ["bk", "bm", "bi"]
    return map(lambda x: prefix+x, transitions[prefix[-1]])

from collections import deque
def word_gen(n):
    '''Generate all the words of length n that conform to the rules of
    the problem. This runs with exponential complexity (C**n for some
    constant C), so it's only used to test counts for values of n up
    to 10.

    '''
    q = deque(kseq) # initialize the queue with words of length 1
    while len(q) > 0:
        w = q.popleft() # shift the current word from the queue
        if len(w) < n:
            # if the word is too short, then enqueue words with w as a
            # prefix and transition chars as the last character
            q.extend(add_char(w))
        else:
            # the word is the required length, return it
            yield w

def count_all(n):
    '''Counts all words of length n using the fast memoized
    count_words() above. The complexity is O(n**2), holding the keypad
    and transition rules constant. This calls count_words m**2 times,
    where m is the size of the keypad (18 here). Count_words itself is
    O(n**2 * t), so the total cost of the count is O(n**2 * t * m**2), where t
    is the nuber of transitions in the transition matrix.

    '''
    rval = 0
    if n < 1:
        return 0
    if n == 1:
        return len(kseq)
    for f in kseq:
        for l in kseq:
            rval += count_words(f, l, n)
    return rval

print count_all(word_len)
#print "word_len: %s, call_count %s, call_count_avg: %s, table size: %s, avg: %s" % (word_len, call_count, float(call_count)/(word_len**2), len(tbl), float(len(tbl))/word_len)

if word_len < 11:
    c = 0
    for w in word_gen(word_len):
        c += 1
    print c
