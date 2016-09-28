def get_words_from_document(path, stop_words):
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
                if len(word) > 1 and word not in stop_words:
                    words.append(word)
    return words


def make_dict_from_documents(paths, stop_words):
    word_dict = {}
    number_of_words = 0
    for path in paths:
        file = open(path, 'r')
        start_parse = False
        for line in file:
            if not start_parse and "Lines:" in line:
                start_parse = True
            elif start_parse:
                words_in_line = line.split()
                for w in words_in_line:
                    word = filter(lambda x: x.isalpha(), w).lower()
                    if len(word) > 1 and word not in stop_words:
                        number_of_words += 1
                        if word not in word_dict:
                            word_dict[word] = 1
                        else:
                            word_dict[word] += 1

    return number_of_words, word_dict