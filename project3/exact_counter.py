from collections import defaultdict
import re
from utils import open_file


class ExactCounter():
    def __init__(self, fname="datasets/AssociationFootball.txt"):
        self.fname = fname

    
    def __str__(self):
        return "Exact Counter"


    '''Reads file in chunks
       counts the letters and stores the event
       gets the dictionary with the exact number of occurrences of each letter
    '''
    def count(self):
        self.letter_occur = defaultdict(int)

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            for letter in chunk:
                if letter.isalpha():
                    self.letter_occur[letter.upper()] += 1
        file.close


    def top_k_letters(self, k=10):
        return {letter: occur for letter, occur in \
            sorted(self.letter_occur.items(), key=lambda x: x[1], reverse=True)[:k]}

    def top_letters(self):
        self.letter_occur = defaultdict(int)

        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            for letter in chunk:
                if letter.isalpha():
                    self.letter_occur[letter.upper()] += 1
        file.close

        return dict(sorted(self.letter_occur.items(), key=lambda item: item[1], reverse=True))