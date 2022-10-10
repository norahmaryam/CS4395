from nltk import word_tokenize, ngrams
from collections import Counter
import pickle

import sys  # to get the system parameter 

# create bigram and unigram dictionaries for english, french, and italian text
def bigramAndUnigramDicts(filename): 
  with open(filename, 'r') as f:
    content = f.read() #read in file 
    processed_content = content.replace('\n', '') #remove new lines
    tokens = word_tokenize(processed_content) # tokenize text
    bigrams = ngrams(tokens, 2) # creeate bigrams
    unique_bigrams = set(bigrams) # get unique bigrams
    unigrams = tokens # get unigrams
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)} # create dict of unigrams and their counts
    bigram_dict = dict(Counter(unique_bigrams)) # create dict of bigrams and their counts
    return bigram_dict, unigram_dict

# main function
if __name__ == '__main__':
    # if sys arg is not entered, prompt user for appropriate file name
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        # takes in each file as sys arg and return bigram/unigram dicts
        fp_1 = sys.argv[1]
        bigrams_eng_dict, unigrams_eng_dict = bigramAndUnigramDicts(fp_1)
        fp_2 = sys.argv[2]
        bigrams_fra_dict, unigrams_fra_dict = bigramAndUnigramDicts(fp_2)
        fp_3 = sys.argv[3]
        bigrams_ita_dict, unigrams_ita_dict = bigramAndUnigramDicts(fp_3)

        # save each bigram and unigram dict in pickle file
        pickle.dump(bigrams_eng_dict, open('bigram_eng_dict.p', 'wb'))  # write binary
        pickle.dump(unigrams_eng_dict, open('unigram_eng_dict.p', 'wb'))  # write binary
        pickle.dump(bigrams_fra_dict, open('bigram_fra_dict.p', 'wb'))  # write binary
        pickle.dump(unigrams_fra_dict, open('unigram_fra_dict.p', 'wb'))  # write binary
        pickle.dump(bigrams_ita_dict, open('bigram_ita_dict.p', 'wb'))  # write binary
        pickle.dump(unigrams_ita_dict, open('unigram_ita_dict.p', 'wb'))  # write binary
       

