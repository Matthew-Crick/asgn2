class Node:
    def __init__(self):
        self.children = [None]*26
        self.end_count = 0
        self.sentence = None
        self.max_count = 0
        self.max_sentence = ''

class CatsTrie:
    pass