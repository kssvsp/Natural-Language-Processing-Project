from PIL import Image
from collections import defaultdict
import pytesseract
import re
from collections import Counter
from nltk import tokenize
from difflib import SequenceMatcher
import nltk
nltk.download('words')
from nltk.corpus import words
nltk.download('wordnet')
from nltk.corpus import wordnet


def callViterbi(text):
    scoreList, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k = 0
        k = 0
        for j in range(max(0, i - maximumlength), i):
            maximumProbability = scoreList[j] * (dictionary[text[j:i]] / total)
            if (maximumProbability > prob_k):
                prob_k = maximumProbability
                k = j
        scoreList.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words


uniqueWordCount = {}
total = 0
wordList=[]
file=open("C:/Users/karna/PycharmProjects/untitled/venv/Lib/Dictionary.txt", "r",encoding="utf8")
for f in file.readlines():
    s = re.sub(r'[^\w\s]', '',f)
    tokens = nltk.word_tokenize(s)
    for i in tokens:
        wordList.append(i)
        total = total + 1

list_set = set(wordList)
unique_list = (list(list_set))

dictionary = Counter(unique_list)
maximumlength = max(map(len, dictionary))

uniqueWordProbability={}

for word in wordList:
    uniqueWordProbability[word] = dictionary[word] / total

im = Image.open("main.png")
text =pytesseract.image_to_string(im,lang= 'eng')

tokenized_sentence=tokenize.sent_tokenize(text)

sentenceList=[]

for tok in tokenized_sentence:
    tok1=tok.replace('\n', '')
    word = re.sub(r'[^\w\s]', '', tok1)
    word = re.sub(r'[0-9]+', '', word)
    sentence = ''
    tokens = nltk.word_tokenize(word)
    for tk in tokens:
        sentence = sentence+ " "+tk
    sentenceList.append(sentence.strip())

print(sentenceList)

for sentence in sentenceList:
    sentence1=' '
    tokens=sentence.split(' ')
    for tok in tokens:
        if (wordnet.synsets(tok)):
            sentence1 = sentence1 + " " + tok + " "
        else:
            if tok not in wordList:
                z = callViterbi(tok)
                #print(z)
                for i in z:
                    sentence1=sentence1+i+" "
            else:
                sentence1 = sentence1 + " " + tok + " "
    print(sentence1)

