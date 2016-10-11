import document_parsing as dp
import glob
from copy import deepcopy
from math import log


class Category:
    def __init__(self, path, stop_words, learning_fraction):
        # Keeping path for easy access
        self.category_dir = path

        # Getting files for learning set and test set
        files = glob.glob(path + "\\*")
        files_to_learn = learning_fraction*len(files)
        learning_set = []
        self.test_set = []
        for i in range(len(files)):
            if i < files_to_learn:
                learning_set.append(files[i])
            else:
                self.test_set.append(files[i])

        parsed_documents = dp.make_dict_from_documents(learning_set, stop_words)
        self.number_of_words = parsed_documents[0]
        self.word_dict = parsed_documents[1]

        self.category_prob = 0.0
        self.vocabulary = {}
        self.def_prob_for_word = 0.0

    def calc_word_prob(self, vocabulary, category_prob):
        # Keep in object for use in check_if_document_fits
        self.category_prob = category_prob

        # Deepcopy to avoid getting reference
        self.vocabulary = deepcopy(vocabulary)

        # Default probability for words in the vocabulary but not in the category learning set
        self.number_of_words += len(vocabulary)
        self.def_prob_for_word = 1.0/self.number_of_words

        # Calculating probability of a word given the category.
        # Only iterating over words found in the category as all other words will have known values
        for word in self.word_dict:
            p = (self.word_dict[word] + 1.0)/self.number_of_words
            self.vocabulary[word] = p

    # Calculating value p. High p means document likely fits the category
    def check_if_document_fits(self, words_in_document):
        p = self.category_prob
        for word in words_in_document:
            try:
                # Word is in vocabulary, but not in this category
                if self.vocabulary[word] == 0:
                    p += log(self.def_prob_for_word)
                # Word is in vocabulary and this category
                else:
                    p += log(self.vocabulary[word])
            # Word is not in the vocabulary
            except KeyError:
                p += 0
        return p

    def get_category_words(self):
        return self.word_dict.keys()

    def get_test_set(self):
        return self.test_set

    def get_path(self):
        return self.category_dir
