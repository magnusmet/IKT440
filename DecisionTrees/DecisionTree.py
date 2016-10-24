import csv, math, tools, random

data = csv.reader(open("data/tweets.csv", "r"))
all_data = []
for d in data:
    all_data.append([d[1], d[2]])
all_data = all_data[1:]
random.shuffle(all_data)
training_tweets = all_data[(len(all_data) / 2):]
trump_words, hillary_words = tools.get_top_words(training_tweets)


def contains_most_used_words(tweet):
    global trump_words
    global hillary_words
    for word in tweet.split():
        w = filter(lambda x: x.isalpha() or "#" in x or "@" in x, word).lower()
        if w in trump_words:
            return "Contains Trump word"
        elif w in hillary_words:
            return "Contains Hillary word"

    return "Contains no Trump or Hillary words"


def binary_choice(name):
    if "Trump" in name:
        return "0"
    else:
        return "1"

training_data = []
for data in all_data[(len(all_data) / 2):]:
    training_data.append([binary_choice(data[0]), contains_most_used_words(data[1])])

verification_data = []
for data in all_data[:(len(all_data) / 2)]:
    verification_data.append([binary_choice(data[0]), contains_most_used_words(data[1])])



def split(data, attribute, remove=False):
    retvals = {}
    allattributes = set([i[attribute] for i in data])
    for d in data:
        c = d[attribute]
        aList = retvals.get(c, [])
        if (remove):
            d.pop(attribute)
        aList.append(d)
        retvals[c] = aList
    return retvals


def entropy(oneclass):
    pos = len([i for i in oneclass if i[0] == "0"])
    neg = len([i for i in oneclass if i[0] == "1"])
    total = float(pos + neg)
    if (min((pos, neg)) == 0):
        return 0
    entropy = - (pos / total) * math.log(pos / total, 2) - (neg / total) * math.log(neg / total, 2)
    return entropy


def gain(oneclass, attribute):
    d = [(entropy(i), len(i)) for i in split(oneclass, attribute, False).values()]
    nAll = sum([i[1] for i in d])
    gain = sum([(i[0] * i[1]) / nAll for i in d])
    return gain


def getHighestGain(oneclass):
    before = entropy(oneclass)
    classes = [i for i in range(1, len(oneclass[0]))]
    entropies = [gain(oneclass, c) for c in classes]
    return entropies.index(min(entropies)) + 1


def isPure(oneclass):
    classes = [i for i in range(1, len(oneclass[0]))]

    for c in classes:
        if (len(set([i[c] for i in oneclass])) > 1):
            return False
    return True


def isEmpty(oneclass):
    return len(oneclass[0]) <= 1


def mostCommon(oneclass):
    lst = [i[0] for i in oneclass]
    return max(set(lst), key=lst.count)


def confidence(oneclass):
    mostcommon = mostCommon(oneclass)
    return len([i[0] for i in oneclass if i[0] == mostcommon]) / len(oneclass)


actualClassifier = "def classify(data):"


def buildTree(oneclass, spaces="    "):
    global actualClassifier
    if (isEmpty(oneclass) or isPure(oneclass)):
        print(spaces, "then ", mostCommon(oneclass))
        print(spaces, "#confidence", confidence(oneclass))
        actualClassifier += "\n" + spaces + "return (" + mostCommon(oneclass) + ")"
        return
    highest = getHighestGain(oneclass)
    d = split(oneclass, highest)
    for key, value in d.items():
        print(spaces, "if ", key)  # ,"(item", highest,")")
        actualClassifier += "\n" + spaces + "if(data[" + str(highest) + "]==\"" + str(key) + "\"):"
        buildTree(value, spaces + "   ")


buildTree(training_data)
print(actualClassifier)
exec (actualClassifier)
correct, wrong = 0.0, 0.0
for data in verification_data:
    if (int(data[0]) == int(classify(data))):
        correct += 1
    else:
        wrong += 1
print ("Correct classifications", correct)
print ("Wrong classifications", wrong)
print ("Accuracy", correct / (correct + wrong))
