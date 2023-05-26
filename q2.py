class Node:
    ''' A singular unit Node class to be used for our Trie data structure that incorporates every potential character '''

    def __init__(self):
        ''' Initialises our instance variables for every made Node '''

        self.child = 26 * [None]  # We know node can have at most 26 children; where each child represents a potential character from the finite alphabet consisting of 'a' to 'z'.
        self.sentence = None  # To store a potential sentence that could end at this node; Initialised to None to consider None case.
        self.maximum_sentence = ''  # To store the sentence that occurs most frequently within the subtree rooted from some node.
        self.sentence_end_number = 0  # Counts the number of ending sentences at some node.
        self.maximum_occurrence_number = 0  # Counts the maximum occurrence of a particular sentence within the subtree rooted at some node.

class CatsTrie:
    ''' A CatsTrie class that uses our Node class to incorporate cat sentences within a Trie data structure '''

    def __init__(self, sentences):
        ''' Uses our Node class to initialises our instance variables for every made CatsTrie structure 
            :INPUT: 
                sentences:  a list of timelines represented as a list of strings with:
                    N sentences, where N is a positive integer.
                    The longest sentence would have M characters, as mapped from the cat vocabulary. is a positive integer.
                    A cat word can occur more than once in a single sentence. For example, the string baacbb represents a valid sentence.
                    Assume that there is only a maximum of 26 unique cat words in total, represented as lower case characters from a to z.
        '''
        self.root = Node()  # The CatsTrie root

        #  For every sentence within the sentences input; add that sentence to our CatsTrie structure
        for sent in sentences:
            self.add_sentence(sent)