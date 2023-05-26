class Node:
    ''' A singular unit Node class to be used for our Trie data structure that incorporates every potential character '''

    def __init__(self):
        ''' 
        Initialises our instance variables for every made Node
        Every child node is a potential pathway that leads to another subsequent character stored in a particular sentence, this is how we will endeavour to autocomplete the functionality of our CatsTrie data structure.
        :INPUT: No Direct Input
        :OUTPUT: No Direct Return Output
        :TIME_COMPLEXITY: O(1)
        :SPACE_COMPLEXITY: O(1)
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
            :OUTPUT: No Direct Return Output
            :TIME_COMPLEXITY: O(NM) time complexity where N is the number of sentence in sentences & M is the number of characters in the longest sentence.
            :SPACE_COMPLEXITY: O(NM) space complexity where N is the number of sentence in sentences & M is the number of characters in the longest sentence.
        '''
        self.root = Node()  # The CatsTrie root

        #  For every sentence within the sentences input; use method add_sentence to add that sentence to our CatsTrie structure
        for sent in sentences:
            self.add_sentence(sent)

    def add_sentence(self, sentence):
        ''' At a high abstraction level this method adds a sentence to our CatsTrie structure.
            As it adds; every node in the CatsTrie data structure we will keep the sentence that has the smallest lexicographical order seen
            :INPUT:
                sentence:  a subsentence of the input list 'sentences' that is to be added to our structure
            :OUTPUT: No Direct Return Output
            :TIME_COMPLEXITY: O(NM) time complexity where N is the number of sentence in sentences & M is the number of characters in the longest sentence.
            :SPACE_COMPLEXITY: O(NM) space complexity where N is the number of sentence in sentences & M is the number of characters in the longest sentence.
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

        # At every node in the CatsTrie data structure we will keep the sentence that has the smallest lexicographical order seen
        # Set the current sentence to the current node if there has yet to be a sentence assigned to the node; otherwise if the current sentence is less than (lexicographically) than that of the sentence at the same node; update to reflect the smaller of the two
        if node.sentence is None:
            node.sentence = sentence
        else:
            if sentence < node.sentence:
                node.sentence = sentence

        # Lets propagate the occurence of the current sentence up our CatsTrie; to keep track of the most occurring sentence at each node.
        # Our temporary variable will be used to traverse the CatsTrie structure from the root to the corresponding nodes based on the characters of the current sentence.
        temp = self.root

        # So to get to every node; again we must iterate through every character in every sentence 
        for character in sentence:

            # And calculate its index 
            index = ord(character) - ord('a')

            # Then point to the next node in the path of the current sentence
            temp = temp.child[index]

            # Here at every node along the path, check if the occurrence of the current sentence (node.sentence_end_number) is greater than that of the known highest sentence occurrence known thus far (temp.maximum_occurrence_number). 
            # If it is; update the maximum_sentence and maximum_occurrence_number at this node; Similarly do this for when the current sentence is of equal occurrence but a smaller lexicographical order than that of the current maximum_sentence.
            if temp.maximum_occurrence_number < node.sentence_end_number or (temp.maximum_occurrence_number == node.sentence_end_number and temp.maximum_sentence > node.sentence):
                temp.maximum_occurrence_number = node.sentence_end_number
                temp.maximum_sentence = node.sentence

        # Once propagating through the temporary Trie, we perform a similar check at the root node of our self CatsTrie
        # Again if the current sentence's occurrence number is higher than that of the maximum_occurrence_number known to be recorded at the root, 
        # or if they have the same frequency but the current sentence has a smaller lexicographical order; update the root's maximum_occurrence_number and maximum_sentence to reflect that of the current sentence
        if self.root.maximum_occurrence_number < node.sentence_end_number or (self.root.maximum_occurrence_number == node.sentence_end_number and self.root.maximum_sentence > node.sentence):
            self.root.maximum_occurrence_number = node.sentence_end_number
            self.root.maximum_sentence = node.sentence

    def autoComplete(self, prompt):
        ''' Driver method to autocomplete a given prompt based on the Trie.
            :INPUT:
                prompt:  is a string with characters in the set of [a...z]. This string represents the incomplete sentence that is to be completed by the trie.
            :OUTPUT: node.maximum_sentence; A string reflecting that of the sentence that has the maximum occurrence that starts with the input prompt
            :TIME_COMPLEXITY: O(X+Y) time complexity where X is the length of the prompt & Y is the length of the most frequent sentence in sentences that begins with the prompt, O(X) where such sentence do not exist
            :SPACE_COMPLEXITY: O(NM) space complexity where N is the number of sentence in sentences & M is the number of characters in the longest sentence.
        '''
        # Beginning from the root node 
        node = self.root
        
        # Traverse through the Trie with regards to every character within the given prompt
        for char in prompt:

            # Get the index thats related to the current character in iteration
            index = ord(char) - ord('a')

            # If there is no child node for this character; return None as this is the case for where the prompt is not within the CatsTrie data structure
            if node.child[index] is None:
                return None
            
            # Point to the next child node 
            node = node.child[index]

        # Return the sentence that has the maximum occurrence that starts with the input prompt
        return node.maximum_sentence