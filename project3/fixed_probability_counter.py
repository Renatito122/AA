from collections import defaultdict
import re
from utils import open_file
from random import random, seed


class FixedProbCounter():
    def __init__(self, fname="datasets/AssociationFootball.txt"):
        seed(98380)

        self.fname = fname

        self.fixed_probability = 1/32

    
    def __str__(self):
        return "Fixed Probability Counter with 1/32"


    '''Reads file in chunks
       counts the letters and stores the event
       gets the dictionary with the number of occurrences of each letter
       using a fixed probability of 1/32
    '''
    def count(self):
        self.letter_occur = defaultdict(int)

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            # removes all non-alphabetical chars
            for letter in chunk:
                if letter.isalpha():
                    # counts event with a fixed probability
                    if random() <= self.fixed_probability:
                        self.letter_occur[letter.upper()] += 1

        file.close


    def estimate_events(self):
        self.estimated_letter_occur = {}
        for letter, occur in self.letter_occur.items():
            self.estimated_letter_occur[letter] = int(occur * (1 / self.fixed_probability)) 