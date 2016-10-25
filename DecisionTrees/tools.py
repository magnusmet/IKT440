import operator


def get_top_words(tweets):
    stop_words = []
    for line in open("data/stop_words.txt", 'r'):
        stop_words += line.split()
    trump_dict = {}
    hillary_dict = {}

    for tweet in tweets:
        if "Trump" in tweet[0]:
            for word in tweet[1].split():
                w = filter(lambda x: x.isalpha() or "#" in x or "@" in x, word).lower()
                if w not in stop_words and len(w) > 2:
                    if w in trump_dict:
                        trump_dict[w] += 1
                    else:
                        trump_dict[w] = 1
        elif "Hillary" in tweet[0]:
            for word in tweet[1].split():
                w = filter(lambda x: x.isalpha() or "#" in x or "@" in x, word).lower()
                if w not in stop_words and len(w) > 2:
                    if w in hillary_dict:
                        hillary_dict[w] += 1
                    else:
                        hillary_dict[w] = 1

    trump_words = sorted(trump_dict.items(), key=operator.itemgetter(1))
    trump_words.reverse()
    hillary_words = sorted(hillary_dict.items(), key=operator.itemgetter(1))
    hillary_words.reverse()

    top_trump = []
    for word in trump_words:
        if word[0] not in hillary_dict:
            top_trump.append(word)
        elif word[1]/3 > hillary_dict[word[0]]:
            top_trump.append(word)
    top_trump = dict(top_trump)

    top_hillary = []
    for word in hillary_words:
        if word[0] not in trump_dict:
            top_hillary.append(word)
        elif word[1]/2 > trump_dict[word[0]]:
            top_hillary.append(word)
    top_hillary = dict(top_hillary)


    return top_trump, top_hillary
