import glob
from sys import float_info
from category import Category
import document_parsing as dp
import time


def calc_category_prob(category):
    categories = glob.glob("20_newsgroups\\*")
    total_files = 0.0
    category_files = 0.0
    for c in categories:
        files = glob.glob(c + "\\*")
        total_files += len(files)
        if c == category:
            category_files += len(files)
    return category_files/total_files

t0 = time.time()

# Fraction of documents reserved for learning
learning_fraction = 2.0 / 3.0

# Listing words to avoid when caluclating probablity
stop_words = []
for line in open("stop_words.txt", 'r'):
    stop_words += line.split()

# Acquiring paths for the documents in each category
category_paths = glob.glob("20_newsgroups\\*")

categories = []
total_words = []
test_documents = []
print "Parsing documents and establishing vocabulary"
for i in range(len(category_paths)):
    category = Category(category_paths[i], stop_words, learning_fraction)
    categories.append(category)
    total_words += category.get_category_words()
    test_documents += category.get_test_set()

vocabulary = dict(zip(set(total_words), [0]*len(set(total_words))))

t1 = time.time()

print "Calculating word probs for given category"
for category in categories:
    category_prob = calc_category_prob(category.get_path())
    category.calc_word_prob(vocabulary, category_prob)

t2 = time.time()

print "Start testing"
correctly_asserted = []
incorrectly_asserted = []
for document in test_documents:
    words_in_document = dp.get_words_from_document(document, stop_words)
    max_group = ''
    max_p = -float_info.max
    for category in categories:
        p = category.check_if_document_fits(words_in_document)
        if p > max_p:
            max_p = p
            max_group = category.get_path()
    if max_group in document:
        correctly_asserted.append([max_group, document])
    else:
        incorrectly_asserted.append([max_group, document])

print len(correctly_asserted), "right"
print len(incorrectly_asserted), "wrong"

accuracy = float(len(correctly_asserted))/(len(correctly_asserted)+len(incorrectly_asserted))
print accuracy*100, "percent accurate"

t3 = time.time()

print t1-t0, "seconds to parse documents and establish vocabulary"
print t2-t1, "seconds to calculate word probs for categories"
print t3-t2, "seconds to test and calculate accuracy"
print t3-t0, "seconds elapsed in total"
