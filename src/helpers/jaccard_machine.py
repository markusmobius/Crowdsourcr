from spacy.lang.en import English

class Jaccard:
    def __init__(self):
        self.nlp = English()

    def getTokens(self,text):
        """ takes a string, removes periods and commas and return a dictionary that maps each token 
        in the string to its frequency in the text"""
        doc = self.nlp(text.replace(".", "").replace(",", "").replace("?", "").replace("!", "").lower())
        tokens = {}
        for token in doc:
            if token.text in tokens:
                tokens[token.text] +=1
            else:
                tokens[token.text] =1
        return tokens

    def compare(self, tokens1,tokens2):
        ''' Inputs: tokens1 tokens2, two word bags
        Output: a float, the Jaccard similarity value'''
        overlap = 0
        for key in tokens1:
            if key in tokens2:
                if tokens2[key] > tokens1[key]:
                    overlap += tokens1[key]
                else:
                    overlap += tokens2[key]
        tokens1_size = sum(tokens1.values())
        tokens2_size = sum(tokens2.values())
        return 1.0*overlap / (tokens1_size + tokens2_size - overlap)