import glob
from copy import deepcopy
from math import log

class Category:
    def __init__(self, path, vocabulary, stop_words, learning_fraction, category_prob):
        self.path = path
        files = glob.glob(path + "\\*")
        files_to_learn = learning_fraction*len(files)
        self.learning_set = []
        self.test_set = []
        for file in range(len(files)):
            if file < files_to_learn:
                self.learning_set.append(files[file])
            else:
                self.test_set.append(files[file])

        self.words = []
        for path in self.learning_set:
            file = open(path, 'r')
            start_parse = False

            for line in file:
                if not start_parse and "Lines:" in line:
                    start_parse = True
                elif start_parse:
                    words_in_line = line.split()
                    for w in words_in_line:
                        word = filter(lambda x: x.isalpha(), w).lower()
                        if word not in stop_words and len(word) > 0:
                            self.words.append(word)

        relevant_words = set(self.words)

        self.category_prob = category_prob
        self.vocabulary = deepcopy(vocabulary)
        self.def_prob_for_word = 1.0/(len(self.words) + len(vocabulary))
        for word in relevant_words:
            word_count = self.words.count(word)
            p = (word_count + 1.0) / (len(self.words) + len(vocabulary))
            self.vocabulary[word] = p

    def check_if_docment_fits(self, words_in_document):
        p = self.category_prob
        for word in words_in_document:
            try:
                if self.vocabulary[word] == 0:
                    p += log(self.def_prob_for_word)
                else:
                    p += log(self.vocabulary[word])
            except KeyError:
                p += 0
        return p

    def get_test_set(self):
        return self.test_set

    def get_path(self):
        return self.path

    def get_vocabulary(self):
        return self.vocabulary