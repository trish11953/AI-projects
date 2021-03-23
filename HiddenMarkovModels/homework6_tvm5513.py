############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Trisha Mandal"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.


############################################################
# Section 1: Hidden Markov Models
############################################################


def load_corpus(path):
    loadedcorpus = open(path, 'r')

    sol = []

    for thread in loadedcorpus.readlines():
        thread = thread.strip().split(" ")

        lenthread = len(thread)

        for i in range(0, lenthread):
            tup = tuple(thread[i].split("="))
            thread[i] = tup
        sol.append(thread[:])

    return sol


class Tagger(object):

    def __init__(self, sentences):
        self.sentences = sentences
        self.tag = {"NOUN": 0,
                    "VERB": 0,
                    "ADJ": 0,
                    "ADV": 0,
                    "PRON": 0,
                    "DET": 0,
                    "ADP": 0,
                    "NUM": 0,
                    "CONJ": 0,
                    "PRT": 0,
                    ".": 0,
                    "X": 0}
        partsofspeech=["NOUN","VERB","ADJ","ADV","PRON","DET","ADP","NUM","CONJ","PRT",".","X"]
        self.partsofspeechtransition = {}
        postrans = self.partsofspeechtransition

        for tg in partsofspeech:
            for j in partsofspeech:
                self.partsofspeechtransition[tuple([tg, j])] = 0

        self.sample, tags, pairs = {}, [], {}
        sumtotal, sumtrans, laplace, check = 0, 0, 1e-10, 0

        possibleoutcomes = len(self.tag)
        pairs = self.tag.copy()

        for line in self.sentences:
            check, pos01 = check + 1, line[0][1]

            if pos01 in self.tag:
                self.tag[pos01], sumtotal = self.tag[pos01] + 1, sumtotal + 1

            samplekeys = self.sample.keys()
            for tok in line:

                if tok not in samplekeys:
                    self.sample[tok] = 1

                elif tok in samplekeys:
                    self.sample[tok] = self.sample[tok] + 1

                t1 = tok[1]
                if t1 in pairs:
                    pairs[t1] = pairs[t1] + 1

                tags.append(t1)

        for t in self.tag:
            smtn, denom = self.tag[t] + laplace, sumtotal + possibleoutcomes*laplace
            self.tag[t] = smtn / denom

        ran = len(tags) - 1
        for tg in range(0, ran):
            tpair = tuple([tags[tg], tags[tg+1]])
            if tpair in postrans:
                postrans[tpair], sumtrans = postrans[tpair] + 1, sumtrans + 1

        for value in postrans:
            smtn, denom = laplace + postrans[value], len(postrans) * laplace + sumtrans
            postrans[value] = smtn / denom

        for k, tpair in self.sample.items():
            if k[1] in pairs:
                smtn, denom = self.sample[k] + laplace, pairs[k[1]] + (laplace * 12)
                self.sample[k] = smtn / denom

    def most_probable_tags(self, tokens):
        l, sol = [], []

        for t in tokens:
            minor = []
            lm = len(minor)

            if lm == 0:
                minor += [[(t, 'X'), 0]]

            allkeys = self.sample.keys()
            for k in allkeys:
                if t == k[0]:
                    minor += [[k, self.sample[k]]]

            m = max(minor, key=lambda p: p[1])
            l += [m]
        return [t[0][1] for t in l]

    def viterbi_tags(self, tokens):

        alpha, loc, toptag, laplace, gettag, getsamp = {}, {}, [], 1e-10, self.tag, self.sample

        for value in gettag:
            first, tuple1 = (tokens[0], value),  (0, value)

            if first not in getsamp:
                alpha[tuple1] = laplace
            if first in getsamp:
                p1, p2 = gettag[value], getsamp[first]
                alpha[tuple1] = p1 * p2

        for i in range(1, len(tokens)):

            for value in gettag:
                result, lasttag, tuple1 = 0, "X",(i, value)

                for t in gettag:
                    probability, getpos, tuple2 = 0, self.partsofspeechtransition, (t, value)

                    if tuple2 in getpos:
                        p1, p2 = alpha[(i - 1, t)], getpos[(t, value)]
                        probability = p1 * p2

                    if result < probability:
                        result, lasttag = probability, t

                tuple3 = (tokens[i], value)
                alpha[tuple1] = result * getsamp[tuple3] if tuple3 in getsamp else laplace * result
                loc[(i, value)] = lasttag

        for i in range(0, len(tokens)):
            result, lasttag = 0, "X"
            for val in gettag:
                if alpha[(i, val)] > result:
                    result, lasttag = alpha[(i, val)], val
            toptag += [lasttag]

        tokl = len(tokens) - 1
        for j in range(tokl, 0, -1):
            toptag[j - 1] = loc[(j, toptag[j])]

        return toptag


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I did this assignment in 16 hours 
"""

feedback_question_2 = """
The init and viterbi tags was a little challenging to write
"""

feedback_question_3 = """
I enjoyed this topic and have learned that Hidden Markov Models will be used in higher concepts.
It also had a bit of the previous assignment so that was good.  
"""

