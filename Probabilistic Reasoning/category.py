import glob
from copy import deepcopy
from math import log


class Category:
    def __init__(self, path, vocabulary, stop_words, learning_fraction, category_prob):
        # Keeping path for easy access
        self.path = path

        # Getting files for learning set and test set
        files = glob.glob(path + "\\*")
        files_to_learn = learning_fraction*len(files)
        learning_set = []
        self.test_set = []
        for file in range(len(files)):
            if file < files_to_learn:
                learning_set.append(files[file])
            else:
                self.test_set.append(files[file])

        # Could get copy from outside of class, but easy and quick to repeat
        words = []
        for path in learning_set:
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
                            words.append(word)

        # Removing duplicates
        relevant_words = set(words)

        # Keep in object for use in check_if_document_fits
        self.category_prob = category_prob

        # Deepcopy to avoid getting reference
        self.vocabulary = deepcopy(vocabulary)

        # Default probability for words in the vocabulary but not in the category learning set
        self.def_prob_for_word = 1.0/(len(words) + len(vocabulary))

        # Calculating probability of a word given the category.
        # Only iterating over words found in the category as all other words will have known values
        for word in relevant_words:
            word_count = words.count(word)
            p = (word_count + 1.0) / (len(words) + len(vocabulary))
            self.vocabulary[word] = p

    # Calculating value p. High p means document likely fits the category
    def check_if_document_fits(self, words_in_document):
        p = self.category_prob
        for word in words_in_document:
            try:
                # Word is in vocabulary, but not in this category
                if self.vocabulary[word] == 0:
                    p += log(self.def_prob_for_word)
                #Word is in vocabulary and this category
                else:
                    p += log(self.vocabulary[word])
            # Word is not in the vocabulary
            except KeyError:
                p += 0
        return p

    def get_test_set(self):
        return self.test_set

    def get_path(self):
        return self.path