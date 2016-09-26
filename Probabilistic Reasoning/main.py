import glob
from sets import Set
import math


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

def calc_word_prob(words, unique_words):
    p_word = []
    for word in unique_words:
        word_count = [word, float(words.count(word)/len(words))]
        p_word.append(word_count)

    return p_word

def assert_category(post, unique_words, p_words):
    post_words = parse_document(post)
    max_group = 0
    max_p = 1
    for i in range(len(unique_words)):
        p = 0
        for word in unique_words[i]:
            if word in post_words:
                p += p_word[i][unique_words[i].index(word)][1]
        if p > max_p or max_p == 1:
            max_p = p
            max_group = i

    return max_group

learning_set = 2.0/3.0

stop_words = []

for line in open("stop_words.txt", 'r'): stop_words += line.split()

categories = glob.glob("20_newsgroups\\*")

unique_words = []
p_word = []
for i in range(3):#len(categories)):
    words = parse_documents(categories[i], learning_set, stop_words)
    unique_words.append(list(Set(words)))
    p_word.append(calc_word_prob(words, unique_words[i]))
    print categories[i], "learned"

category = assert_category("20_newsgroups\\alt.atheism\\54485", unique_words, p_word)

for category in categories:
    files = glob.glob(dir + "\\*")
    start_file = int(len(files) * learning_set )
    for i in range (start_file, len(files)):
        probable_category = assert_category(files[i], unique_words, p_word)

print categories[category]




