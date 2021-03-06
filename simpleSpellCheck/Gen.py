'''
    Will generate combinations of mutated vowels and then repeated characters to generate a mispelled word given a source word. 

'''

import random

vowels = set(['a','e','i','o','u'])

def generate(word):
    """
    Given a word will generate:
        1) Bad vowel combinations 
            wake => weke
                    woka ...
        2) Letter repetition
            wake => wwwwake
                    waaaake ...
        3) All vowels wrongified
            wake => waeioukaeiou

    """
    v_combins = [word]#Add original
    items = find_vowel_combinations(word,0,0)
    v_combins.extend(items)
    combinations = generate_repeats(v_combins)
    wrong_vowels = generate_wrong_vowels(word) 
    combinations.extend(wrong_vowels)
    return combinations

def generate_wrong_vowels(word):
    """ One way to generate bad vowels """
    vowels = "aeiou"
    word = word.replace("u","a")
    word = word.replace("o","a")
    word = word.replace("i","a")
    word = word.replace("e","a")
    word = word.replace("a",vowels)
    return [word]
 
def vowel_combin(word,i,x,distance):
    possibles = []
    for vowel in vowels:
        if vowel != x:
            new_word = word[:i] + vowel + word[i+1:]
            possibles.append(new_word  )
            items = find_vowel_combinations(new_word,i+1,distance+1)
            possibles.extend(items)
    return possibles   

def find_vowel_combinations(word,start,distance):
    output = []
    for i,x in enumerate(word):
        if i < start:
            continue
        if x in vowels:
            items = vowel_combin(word,i,x,distance)
            output.extend(items)
    return output

def generate_repeats(list_of_words):
    combins = []
    combins.extend(list_of_words)
    for word in list_of_words:
        word_combs = []
        for i in reversed(range(len(word))):
            word_combs.extend(add_repeat(word,i))
    combins.extend(word_combs)
    return combins

def add_repeat(word,i):
    max_repeat = 3 #Max because I said so
    repeats = [word]
    while max_repeat > 0:
        new_word = word[:i] + (max_repeat*word[i]) + word[i:]
        repeats.append(new_word)
        max_repeat -= 1
    return repeats


words = []


    
def load_words(dictionary="/usr/share/dict/words"):
    with open(dictionary, 'r') as f:
        for line in f:
            if random.randint(0,100) < 1:    
                words.append(line.strip())

load_words()            
for word in words:
    possibles = generate(word)
    for item in possibles:
        print item
