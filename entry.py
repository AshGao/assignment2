import urllib.request
import pickle
import re
from thefuzz import fuzz
import numpy as np
from numpy import random
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

def get_save_text():
    '''define a function that will get the ebook from gutenberg in plain-text, remove the titlepreprocess into a list of paragraphs and save'''
    url="https://www.gutenberg.org/cache/epub/67507/pg67507.txt"
    response = urllib.request.urlopen(url)
    original_text = response.read().decode('utf-8') # get the ebook 'Cheating the Junk-Pile: The Purchase and Maintenance of Household Equipments' from gutenberg
    text_split = original_text.split('\n')# preprocess the original txt: filter out '\n' and empty blocks
    result_text = []
    for sub_text in text_split:
        paragraph = sub_text.strip().lower()
        result_text.append(paragraph)
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments.pickle", 'wb') as f:
        pickle.dump(result_text[1:], f)



def split_word():
    '''define a function split each paragraph from ebook into a long list of words and save'''
    word_list = []
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments.pickle", 'rb') as f:  # load original paragrahs from pickle file
        reloaded_text = pickle.load(f)
        pat = '[a-z]+'
        for paragraph in reloaded_text:
            word_list.extend(re.findall(pat, paragraph))
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments_words.pickle", 'wb') as f: # save the word list into a pickle file
        pickle.dump(word_list, f)



def build_freq_dict():
    '''define a function compute the words frequency in the ebook'''
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments_words.pickle", 'rb') as f:
        word_list = pickle.load(f)
    stop_words_list = []
    words_freq_dict = dict()
    with open("stopwords.txt", 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            stop_words_list.append(line)
    for words in word_list:
        if words in stop_words_list:
            continue
        if words not in words_freq_dict.keys():
            words_freq_dict[words] = 1
            continue
        words_freq_dict[words] += 1
    words_freq_stat = sorted(words_freq_dict.items(), key=lambda x: x[1], reverse=True)
    return words_freq_stat


def compute_the_similarity(sentence_1, sentence_2, is_partial=True):
    if is_partial:
        similarity = fuzz.partial_ratio(sentence_1, sentence_2)
    else:
        similarity = fuzz.ratio(sentence_1, sentence_2)
    return similarity

def most_sim_sen():
    """"Define a function that can return the most similar sentence in the text when you input a sentence"""
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments.pickle", 'rb') as f:
        reloaded_text = pickle.load(f)
        intput_sentence = input().strip()
        most_sim_sen = ''
        max_sim = -1
    for sentence in reloaded_text:
        sim = compute_the_similarity(intput_sentence, sentence, is_partial=False)
        if sim > max_sim:
            max_sim = sim
            most_sim_sen = sentence
    print("The most similar sentence in the ebook is:", most_sim_sen)
    print("The similarity is: ", max_sim)



def cluster(words_freq):
    """define a function that returns a text cluster analysis plot when input words requence data of the text"""
    top_3_words = [words_freq[0][0], words_freq[1][0], words_freq[2][0]]
    the_selected_sentences = []
    with open("saved_pickles/The_Purchase_and_Maintenance_of_Household_Equipments.pickle", 'rb') as f:
        reloaded_text = pickle.load(f)
    for sentence in reloaded_text:
        if len(the_selected_sentences) == 10:
            break
        for word in top_3_words:
            if word in sentence:
                the_selected_sentences.append(sentence)
                break

    sim_mat = np.zeros((10, 10))
    for i in range(10):
        sen_1 = the_selected_sentences[i]
        for j in range(i, 10):
            sen_2 = the_selected_sentences[j]
            sim = compute_the_similarity(sen_1, sen_2)
            sim_mat[i, j] = sim / 100
    sim_mat = sim_mat + sim_mat.T - np.eye(10)
    dis_sim = 1 - sim_mat
    # compute the embedding
    coord = MDS(dissimilarity='precomputed').fit_transform(dis_sim)
    plt.scatter(coord[:, 0], coord[:, 1])
    # Label the points
    for i in range(coord.shape[0]):
        plt.annotate(str(i), (coord[i, :]))
    plt.title("Text Cluster(n=10)")
    plt.show()

def main():
    get_save_text()
    split_word()
    print("------------1.Words frequency statistics------------")
    words_frequency = build_freq_dict()
    print("The 10 most frequent appeared words are:")
    for word, freq in words_frequency[:10]:
        print('%-20s%-20d' % (word, freq))
    print('\n')
    print("------------2.Text similarity analysis------------")
    print("Please input a sentence:")
    most_sim_sen()
    print('\n')
    print("------------3.Text clustering analysis------------")
    cluster(words_frequency)

if __name__ == '__main__':
    main()