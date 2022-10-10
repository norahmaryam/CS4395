from nltk import word_tokenize, sent_tokenize, ngrams
import pickle

import sys  # to get the system parameter

# calculate probabilities for each language and output results to file
def main():
    list_of_langs = calcProbabilities()
    printLangs(list_of_langs)
    computeAccuracy()

# calculate probabilities for each language
def calcProbabilities():
    # read the pickle files
    bigram_eng_dict = pickle.load(open('bigram_eng_dict.p', 'rb'))  # read binary
    unigram_eng_dict = pickle.load(open('unigram_eng_dict.p', 'rb'))  # read binary
    bigram_fra_dict = pickle.load(open('bigram_fra_dict.p', 'rb'))  # read binary
    unigram_fra_dict = pickle.load(open('unigram_fra_dict.p', 'rb'))  # read binary
    bigram_ita_dict = pickle.load(open('bigram_ita_dict.p', 'rb'))  # read binary
    unigram_ita_dict = pickle.load(open('unigram_ita_dict.p', 'rb'))  # read binary

    # open test file and read file
    fp_1 = sys.argv[1]
    with open(fp_1, 'r') as f:
        sentences = f.readlines() #read in file 
   
    p_laplace_eng = 1
    p_laplace_fra = 1
    p_laplace_ita = 1

    e = 0
    f = 0
    ita = 0

    e_d = 0
    f_d = 0
    i_d = 0

    list_of_langs = []

    v = len(unigram_eng_dict) + len(unigram_fra_dict) + len(unigram_ita_dict)
    
    # for each sentence, get unigrams and bigrams and calculate probability with laplace smoothing
    for sent in sentences:
        # tokenize sentence
        uni_training_text_tokens = word_tokenize(sent)
        # get bigrams of tokens
        bigram_text_tokens = list(ngrams(uni_training_text_tokens, 2))
        # for each bigram, calculate probability with formula (b + 1) / (u + v)
        for bigram in bigram_text_tokens:
            e = e + bigram_eng_dict[bigram] if bigram in bigram_eng_dict else 0
            f = f + bigram_fra_dict[bigram] if bigram in bigram_fra_dict else 0
            ita = ita + bigram_ita_dict[bigram] if bigram in bigram_ita_dict else 0
            
            e_d = e_d + unigram_eng_dict[bigram[0]] if bigram[0] in unigram_eng_dict else 0
            f_d = f_d + unigram_fra_dict[bigram[0]] if bigram[0] in unigram_fra_dict else 0
            i_d = i_d + unigram_ita_dict[bigram[0]] if bigram[0] in unigram_ita_dict else 0
            
            p_laplace_eng = p_laplace_eng * ((e + 1) / (e_d + v))
            p_laplace_fra = p_laplace_fra * ((f + 1) / (f_d + v))
            p_laplace_ita = p_laplace_ita * ((ita + 1) / (i_d + v))
            
        list_of_probs = [p_laplace_eng, p_laplace_fra, p_laplace_ita]
        # get language with highest probability
        index_max = max(range(len(list_of_probs)), key=list_of_probs.__getitem__)
        
        lang = ""
        # print language corresponding to index
        if index_max == 0:
            lang = "english"
        elif index_max == 1:
            lang = "french"
        else:
            lang = "italian"

        list_of_langs.append(lang)
        # reset probability with laplace smoothing
        p_laplace_eng = 1
        p_laplace_fra = 1
        p_laplace_ita = 1
    return list_of_langs

# print language with highest probability to text file
def printLangs(list_of_langs):
    with open('langs.txt', 'w') as f:
        for line in list_of_langs:
            f.write(line)
            f.write('\n')

# compute accuracy for predicting languages
def computeAccuracy():
    num_correct = 0
    # open solution file
    with open('LangId.sol') as f:
        sol_lines = f.readlines()
    # for each line, remove integer token at the beginning of the sentence
    for line in range(len(sol_lines)):
        line_to_modify = sol_lines[line]
        modified_line = line_to_modify.split(' ', 1)[1]
        # lowercase token
        sol_lines[line] = modified_line.lower()

    # open text file to output results 
    with open('langs.txt') as f:
        langs_lines = f.readlines()
    # if language predicted is correct, increase num_correct
    for line in range(len(sol_lines)):
        if sol_lines[line] == langs_lines[line]:
            num_correct += 1
        # if not correct, print line number of incorrectly predicted language to file
        else:
            with open('langs.txt', 'a') as f:
                f.write("Incorectly classified line: ")
                f.write(str(line))
                f.write('\n')
    # calculate accuracy
    accuracy = (num_correct / len(sol_lines)) * 100 
    # print accuracy to file
    with open('langs.txt', 'a') as f:
        f.write("Accuracy: " + str(accuracy) + "%")
    # print accuracy to console
    print("Accuracy: " + str( (num_correct / len(sol_lines)) * 100 ) + "%")

main()









