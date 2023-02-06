from collections import defaultdict
from utils import open_file

class LossyCounter():

    def __init__(self, fname="datasets/AssociationFootball.txt", epsilon=5e-3):
        self.n = 0
        self._count = defaultdict(int)
        self.bucket_id = {}
        self.fname = fname
        self.epsilon = epsilon
        self.current_bucket_id = 1


    def __str__(self):
        return "Lossy Counter"


    def getCount(self, item):
        'Return the number of the item'
        return self._count[item]


    def getBucketId(self, item):
        'Return the bucket id corresponding to the item'
        return self.bucket_id[item]


    def addCount(self, item):
        'Add item for counting'
        self.n += 1
        if item not in self._count:
            self.bucket_id[item] = self.current_bucket_id - 1

        self._count[item] += 1

        if self.n % int(1 / self.epsilon) == 0:
            self.trim()
            self.current_bucket_id += 1


    def getIter_with_threshold_rate(self, threshold_rate):
        return self.getIter(threshold_rate * self.n)


    def trim(self):
        'trim data which does not fit the criteria'
        for item, total in list(self._count.items()):
            if total <= self.current_bucket_id - self.bucket_id[item]:
                del self._count[item]
                del self.bucket_id[item]


    def getIter(self, threshold_count):
        self.trim()
        for item, total in self._count.items():
            if total >= threshold_count - self.epsilon * self.n:
                yield (item, total)
            else:
                raise StopIteration


    def count(self):

        stream = ''
        file = open_file(self.fname, 'r')

        # reads chunk by chunk
        while chunk := file.read(1024):
            for letter in chunk:
                if letter.isalpha():
                    stream += letter.upper()
                    
        self.n = len(stream)

        for l in stream:
            self.addCount(l)

        result = {}
        for item, count in sorted(self.getIter(10), key=lambda x: x[1], reverse=True): #, self.getBucketId(item))
            result[item] = count

        return result

