import glob
import math
from sys import float_info
from category import Category


def parse_documents(dir, learning_set, stop_words):
    files = glob.glob(dir + "\\*")
    files_to_read = int(len(files)*learning_set)
    words = []
    for file in files:
        if files_to_read == 0:
            break
        files_to_read -= 1
        words += parse_document(file, stop_words)
    return words


def parse_document(path, stop_words):
    file = open(path, 'r')
    start_parse = False
    words = []
    for line in file:
        if not start_parse and "Lines:" in line:
            start_parse = True
        elif start_parse:
            words_in_line = line.split()
            for w in words_in_line:
                word = filter(lambda x: x.isalpha(), w).lower()
                if word not in stop_words and len(word) > 0:
                    words.append(word)
    return words


def calc_category_prob(category):
    categories = glob.glob("20_newsgroups\\*")
    total_files = 0.0
    category_files = 0.0
    for c in categories:
        files = glob.glob(c + "\\*")
        total_files += len(files)
        if c == categories[category]:
            category_files += len(files)
    return category_files/total_files

#Fraction of documents used for learning
learning_fraction = 0.8#2.0 / 3.0

#Listing words to avoid when caluclating probablity
stop_words = []
for line in open("stop_words.txt", 'r'):
    stop_words += line.split()

#Acquiring paths for the documents in each category
category_paths = glob.glob("20_newsgroups\\*")


#Get words from learning sets and establishing vocabulary
categories = []
total_words = []
category_probs = []
for i in range(len(category_paths)):
    words = parse_documents(category_paths[i], learning_fraction, stop_words)
    total_words += set(words)
    category_probs.append(calc_category_prob(i))
    print category_paths[i], "parsed"

vocabulary = dict(zip(set(total_words), [0]*len(set(total_words))))

test_documents = []
for i in range(len(category_paths)):
    print "Learning", category_paths[i]
    category = Category(category_paths[i], vocabulary, stop_words, learning_fraction, category_probs[i])
    categories.append(category)
    test_documents += category.get_test_set()

print "Start testing"
correctly_asserted = []
incorrectly_asserted = []
for document in test_documents:
    words_in_document = parse_document(document, stop_words)
    max_group = ''
    max_p = -float_info.max
    for category in categories:
        p = category.check_if_docment_fits(words_in_document)
        if p>max_p:
            max_p = p
            max_group = category.get_path()
    print max_p
    if max_group in document:
        correctly_asserted.append(document)
        print "Correct! Guessed", max_group, "for", document
    else:
        incorrectly_asserted.append(document)
        print "Wrong! Guessed", max_group, "for", document

print len(correctly_asserted), "right"
print len(incorrectly_asserted), "wrong"

accuracy = float(len(correctly_asserted))/(len(correctly_asserted)+len(incorrectly_asserted))
print accuracy*100, "percent accurate"
