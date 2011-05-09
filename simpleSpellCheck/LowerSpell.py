#!/usr/bin/python
"""
    Relies on the existance of /usr/share/dict/words to load a default dict.
    One can modify the code to pass in a new location to a dict at the bottom
    where load_dict() becomes load_dict('/path/to/awesometown')

    Handles three mispellings:
        1) Case (upper/lower) errors: "inSIDE" => "inside"
        2) Repeated letters: "jjoobbb" => "job"
        3) Incorrect vowels: "weke" => "wake"

    And a combination of them:
        "CUNsperrICY" => "conspiracy"
        "weeeeeeeeke" => "wake" (Wrong vowel, then repeated)
        "waeiouuioka" => "woke" (Repeated vowel, then vowel wrongified)

    Tested on 32bit Ubuntu 10.04 & 11.04
    Python 2.6.5 & 2.7.1

"""

vowels = set(['a','e','i','o','u'])

class Node:
    def __init__(self, value=None):
        self.children = {}
        self.word = ""
        self.letter = value

    #helper for recursion
    def add_word(self, word):
        self.add_word_recur(word,word)

    def add_word_recur(self, full_word, word_left):
        if word_left == "":
            self.word = full_word
            return

        key = word_left[0]
        rest = word_left[1:]

        if key not in self.children:
            self.children[key] = Node(key)

        self.children[key].add_word_recur(full_word, rest)

    def find_fuzzy(self, word):
        matches = self.find_fuzzy_matches(word.lower())
#        if not matches:
#            matches = self.find_fuzzy_matches(word.upper())
#        if not matches and len(word) > 1:
#            new_word = word[0].upper() + word[1:].lower()
#            matches = self.find_fuzzy_matches(new_word)
#        if not matches



        if matches:
            return reduce(lambda x,y: x if x[0] <= y[0] else y, matches)[1]
        else:
            return 'NO SUGGESTIONS'

    def find_fuzzy_matches(self, word):
        if word == "":
            if self.word:
                return [(0,self.word)]
            else:
                return []

        key = word[0]
        rest = word[1:]
        
        matches = []
        if key in self.children:
            matches = self.children[key].find_fuzzy_matches(rest)
        matches = [m for m in matches if m] #remove None's
        #Short-Circuit opportunity: We have a match!
        if len(matches) > 0:
            return matches

        fuzzy_matches = []
        #Try descending via mutated vowels
        #Handle: wuka -> wake
        if key in vowels:
            for v in vowels:
                if v != key:
                    if v in self.children:
                        m = self.children[v].find_fuzzy_matches(rest)
                        fuzzy_matches.extend(m)

        # try with repeated letters or repeated vowels removed
        # Handle: wakkkke -> wake
        #         weeeeeeke -> wake
        #         waeaoiooika -> wake
        vowel_repeat = (key in vowels and rest != "" and rest[0] in vowels)
        if self.letter == key or vowel_repeat:
            m = self.find_fuzzy_matches(rest)
            fuzzy_matches.extend(m)

        # remove None's
        fuzzy_matches = [m for m in fuzzy_matches if m]

        # calculate edit distance of our fuzzy matches
        adjustd_fuzzy_matches = [(distance+1,w) for distance,w in fuzzy_matches]
        return adjustd_fuzzy_matches
        

dict_tree = Node()

def load_dict(words="/usr/share/dict/words"):
    with open(words, 'r') as f:
        for line in f:
            dict_tree.add_word(line.strip().lower())

#TODO Need to write a test harness to generate words to look up, can use removed code from before
#

print "Loading dictionary at /usr/share/dict/words ..."
load_dict()
print "Loaded. Cntrl-C or Cntrl-D will kill program."
words = ["mateg",
         "mate",
         "ren",
         "zee",
         "zoot",
         "mATe",
         "matte",
         "mattte",
         "mmmattte",
         "CUNsperrICY",
         "weke",
         "jjoobbb",
         "inSIDE",
         "peepple",
         "weeeeka",
         "laaaan",
         "sheeeeeep",
         "meeeeeeen",
         "weaoike",
         "sheeple"]
#for w in words:
#     print w,dict_tree.find_fuzzy(w)

while(True):
    word = raw_input("> ")
    print word,dict_tree.find_fuzzy(word)