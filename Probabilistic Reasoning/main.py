import glob
from sys import float_info
from category import Category
import plotly as py
from plotly import graph_objs as go


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

# Fraction of documents reserved for learning
learning_fraction = 2.0 / 3.0

# Listing words to avoid when caluclating probablity
stop_words = []
for line in open("stop_words.txt", 'r'):
    stop_words += line.split()

# Acquiring paths for the documents in each category
category_paths = glob.glob("20_newsgroups\\*")


# Get words from learning sets and establishing vocabulary
categories = []
total_words = []
category_probs = []
print "Getting words from learning sets and establishing vocabulary..."
for i in range(len(category_paths)):
    words = parse_documents(category_paths[i], learning_fraction, stop_words)
    total_words += set(words)
    category_probs.append(calc_category_prob(i))

vocabulary = dict(zip(set(total_words), [0]*len(set(total_words))))

test_documents = []
print "Making category objects and calculating word prob given category"
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
        p = category.check_if_document_fits(words_in_document)
        if p>max_p:
            max_p = p
            max_group = category.get_path()
    if max_group in document:
        correctly_asserted.append([max_group, document])
        print "Correct! Guessed", max_group, "for", document
    else:
        incorrectly_asserted.append([max_group, document])
        print "Wrong! Guessed", max_group, "for", document

print len(correctly_asserted), "right"
print len(incorrectly_asserted), "wrong"

accuracy = float(len(correctly_asserted))/(len(correctly_asserted)+len(incorrectly_asserted))
print accuracy*100, "percent accurate"

# Sorting results
actual_category_vs_guessed_category = []
for path in category_paths:
    category_guessed = []
    for guess in correctly_asserted:
        if path in guess[1]:
            category_guessed.append(guess[0])
    for guess in incorrectly_asserted:
        if path in guess[1]:
            category_guessed.append(guess[0])
    actual_category_vs_guessed_category.append([path, category_guessed])

# Creating pie charts using plotly
data = []
for category in actual_category_vs_guessed_category:
    d1 = []
    d2 = []
    for guess in set(category[1]):
        d1.append(guess)
        d2.append(category[1].count(guess))
    data.append([category[0], d1, d2])

for category in data:
    fig = {
        'data': [{'labels': category[1],
                  'values': category[2],
                  'type': 'pie'}],
        'layout': {'title': category[0]}
    }
    py.offline.plot(fig, filename=category[0]+'.html')