import glob
from sets import Set
import math
import sys
from xml.etree.ElementInclude import include


def parse_documents(dir, learning_set, stop_words):
    files = glob.glob(dir + "\\*")
    files_to_read = int(len(files)*learning_set)
    words = []
    for file in files:
        if files_to_read == 0: break

        files_to_read -= 1
        f = open(file, 'r')
        start_parse = False

        for line in f:
            if not start_parse and "Lines:" in line: start_parse = True
            elif start_parse:
                l = line.split()
                for w in l:
                    word = filter(lambda x: x.isalpha(), w).lower()
                    if word not in stop_words and len(word)>0:
                        words.append(word)
    return words


def parse_document(path):
    file = open(path, 'r')
    start_parse = False

    for line in file:
        if not start_parse and "Lines:" in line:
            start_parse = True
        elif start_parse:
            l = line.split()
            for w in l:
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


def calc_word_prob(words, vocabulary):
    p_words = []
    relevant_words = list(Set(words))
    def_val = 1.0/(len(words)+len(vocabulary))
    for word in vocabulary:
        if word in relevant_words:
            word_count = words.count(word)
            p = (word_count+1.0)/(len(words)+len(vocabulary))
            p_words.append([word, p])
        else:
            p_words.append([word, def_val])

    return p_words


def assert_category(document, vocabulary, p_words):
    print "Parsing document..."
    words_in_document = parse_document(document)
    max_group = 0
    max_p = -sys.float_info.max
    for i in range(len(vocabulary)):
        p = math.log(calc_category_prob(i))
        for word in words_in_document:
            if word in vocabulary[i]:
                word_index = vocabulary[i].index(word)
                p += math.log(p_words[i][word_index][1])
        print "max_p", max_p
        print "i: ", i, "p: ", p, "base_p:", calc_category_prob(i)
        if p>max_p:
            max_p = p
            max_group = i
            print "***new max*** --->", i

    return max_group

learning_set = 2.0/3.0

stop_words = []

for line in open("stop_words.txt", 'r'):
    stop_words += line.split()

categories = glob.glob("20_newsgroups\\*")

category_words = []
vocabulary = []
for i in range(len(categories)):
    words = parse_documents(categories[i], learning_set, stop_words)
    category_words.append(words)
    vocabulary += list(Set(words))
    print categories[i], "parsed"


p_words = []
for category in category_words:
    print "Learning new category"
    words = calc_word_prob(category, vocabulary)
    p_words.append(words)
    print categories[len(p_words)-1], "learned"


correctly_asserted = []
incorrectly_asserted = []

for category in categories:
    print "Testing documents from", category
    files = glob.glob(categories[1] + "\\*")
    start_file = int(len(files) * learning_set)
    for i in range(start_file, len(files)):
        probable_category = assert_category(files[i], vocabulary, p_words)
        if categories[probable_category] == categories[1]:
            correctly_asserted.append(files[i])
            print "correct", files[i]
        else:
            incorrectly_asserted.append(files[i])
            print "wrong", files[i], "guessed", categories[probable_category]

print len(correctly_asserted), "right"
print len(incorrectly_asserted), "wrong"

accuracy = len(correctly_asserted)/(len(correctly_asserted)+len(incorrectly_asserted))
print accuracy, "accuracy"
