import csv, math, tools, random


data = csv.reader(open("data/tweets.csv", "r"))
all_data = []
for d in data:
    all_data.append([d[1], d[2], d[4], d[10]])
    if "is_retweet" not in d[3]:
        if "True" not in d[3] and "False" not in d[3]:
            print d[3]
            assert False
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

def tweet_author(handle):
    if handle is "":
        return "OC"
    elif "trump" in handle.lower() or "donald" in handle.lower():
        return "Retweeted Trump user"
    elif "clinton" in handle.lower() or "hillary" in handle.lower():
        return "Retweeted Hillary user"
    else:
        return "Retweet"

def language(lang):
    if "en" == lang:
        return "English"
    else:
        return "Foreign"


def binary_choice(name):
    if "Trump" in name:
        return "0"
    else:
        return "1"

training_data = []
for data in all_data[(len(all_data) / 2):]:
    training_data.append([binary_choice(data[0]), contains_most_used_words(data[1]),
                          tweet_author(data[2]), language(data[3])])

verification_data = []
for data in all_data[:(len(all_data) / 2)]:
    verification_data.append([binary_choice(data[0]), contains_most_used_words(data[1]),
                              tweet_author(data[2]), language(data[3])])



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

def buildTree(oneclass, spaces="    ", depth=0):
    global actualClassifier
    if (isPure(oneclass) or isEmpty(oneclass) or depth is 2):
        #print(spaces, "then ", mostCommon(oneclass))
        #print(spaces, "#confidence", confidence(oneclass))
        actualClassifier += "\n" + spaces + "return " + mostCommon(oneclass)
        return
    highest = getHighestGain(oneclass)
    d = split(oneclass, highest)
    for key, value in d.items():
        #print(spaces, "if ", key)  # ,"(item", highest,")")
        actualClassifier += "\n" + spaces + "if(data[" + str(highest) + "]==\"" + str(key) + "\"):"
        buildTree(value, spaces + "   ", depth+1)

n_chunks = 10
chunk = len(training_data)/n_chunks
rest_of_set = training_data
answers = []
for i in range(n_chunks):
    actualClassifier = "def classify(data):"
    buildTree(rest_of_set[:chunk])
    rest_of_set = rest_of_set[chunk:]
    print(actualClassifier)
    exec actualClassifier
    for j in range(len(verification_data)):
        answer = classify(verification_data[j])
        try:
            answers[j].append(answer)
        except:
            answers.append([answer])

correct, wrong = 0.0, 0.0
for i in range(len(verification_data)):
    final_answer = "0"
    if answers[i].count(1) > len(answers[i])/2:
        final_answer = "1"
    if verification_data[i][0] is final_answer:
        correct += 1
    else:
        wrong += 1

print ("Correct classifications", correct)
print ("Wrong classifications", wrong)
print ("Accuracy", correct / (correct + wrong))
