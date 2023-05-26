class Node:
    ''' A singular unit Node class to be used for our Trie data structure that incorporates every potential character '''

    def __init__(self):
        ''' 
        Initialises our instance variables for every made Node
        Every child node is a potential pathway that leads to another subsequent character stored in a particular sentence, this is how we will endeavour to autocomplete the functionality of our CatsTrie data structure.
        '''

        self.child = 26 * [None]  # We know node can have at most 26 children; where each child represents a potential character from the finite alphabet consisting of 'a' to 'z'.
        self.child = 26 * [None]  # We know node can have at most 26 children, where each child represents a potential character from the finite alphabet consisting of 'a' to 'z'. 
        self.sentence = None  # To store a potential sentence that could end at some node; helps our autocomplete functionality as it the variable will store the sentence leading to that node. Initialised to None to handle cases where the node does not mark a sentence end.
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

        #  For every sentence within the sentences input; use method add_sentence to add that sentence to our CatsTrie structure
        for sent in sentences:
            self.add_sentence(sent)

    def add_sentence(self, sentence):
        ''' A Method to add a sentence to our CatsTrie structure
            :INPUT:
                sentence:  a subsentence of the input list 'sentences' that is to be added to our structure
        '''
        # Beginning from our root node
        node = self.root  

        # Traverse our sentence of interest character by character
        for character in sentence:

            # For every individual character; assess the relative index that corresponds to the current character in iteration 
            # We can do this by using the ordinal ascii difference to map each character to a unique index in the range of our finite alphabet
            index = ord(character) - ord('a')

            # Should the child node for this particular character not yet exist; then create a node at that index
            if node.child[index] is None:
                node.child[index] = Node()

            # Point to the corresponding child node to that of the current character in iteration; setting up for next iteration where subsequent characters in the sentence are handled
            # Ultimately once every sentence within the input sentences is processed; we will have expanded upon our CatsTrie structure as we map every sentence to a potential pathway through our CatsTrie structure
            node = node.child[index]
        
        # The end of a sentence is reached once we have iterated through its characters; at this point we mark this in memory by incrementing our sentence_end_number count which allows us to track the number of sentences that finish at this particular node 
        node.sentence_end_number += 1

        # Keep the smallest lexicographical ordered sentence we have seen so far at each node in the Trie
        # As we will eventually endeavour to return the most occurring sentence that matches our prompt. Should sentences have the same number of occurrences; we'd want to return the sentence with the smallest lexicographical order
        if node.sentence is None:
            node.sentence = sentence
        else:
            if sentence < node.sentence:
                node.sentence = sentence