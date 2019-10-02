import nltk
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk import ConditionalFreqDist
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict
import pytesseract
import re
from collections import Counter
from nltk import tokenize
from difflib import SequenceMatcher
from nltk.corpus import words

sentenceList = []
unigramDict = {}
unigramWordCount = 0
bigramDict = {}
bigramWordCount = 0

file = open("new4.txt", "r", encoding="utf8")
for f in file.readlines():
    st = f.split('.')
    for sentence in st:
        s = re.sub(r'[^\w\s]', '', sentence.strip('\n'))
        s = re.sub(r'[0-9]+', '', s)
        if (len(s) > 0):
            st = s.strip()
            # print(st)
            tokens = nltk.word_tokenize(st)
            for tok in tokens:
                if tok not in unigramDict:
                    unigramWordCount = unigramWordCount + 1
                    unigramDict[tok] = 1
                else:
                    unigramWordCount = unigramWordCount + 1
                    unigramDict[tok] = unigramDict.get(tok) + 1
            bigrm = nltk.bigrams(tokens)
            for big in bigrm:
                if big not in bigramDict:
                    bigramWordCount = bigramWordCount + 1
                    bigramDict[big] = 1
                else:
                    bigramDict[big] = bigramDict.get(big) + 1

print(bigramDict)
print(unigramDict)

import enchant

d = enchant.Dict("en_US")

predictedString='This  fist  volume  in  the series extends  from  che  basics  of setting up  a  molecular  biology laboratory and  growing'
correctString='This  first  volume  in  the series extends  from  the  basics  of setting up  a  molecular  biology laboratory and  growing'


predictedStringTokens = nltk.word_tokenize(predictedString)
correctStringTokens=nltk.word_tokenize(correctString)

wronglyPredicedWord=[]

for i in range(0,len(predictedStringTokens)):
    if(predictedStringTokens[i].__eq__(correctStringTokens[i])):
        print('yes')
    else:
        wronglyPredicedWord.append(predictedStringTokens[i])

import math

def getMaximumProbableWord(sentenceList):
    probabilityList={}
    for k,v in sentenceList.items():
        tokens = nltk.word_tokenize(v.strip())
        bigrm = nltk.bigrams(tokens)
        probabilityValue=1
        for b in bigrm:
            if b in bigramDict and b[0] in unigramDict:
                probabilityValue = probabilityValue * (bigramDict.get(b) / unigramDict.get(b[0]))
            else:
                probabilityValue = probabilityValue * 0.01
        probabilityList[k] = abs(math.log(probabilityValue))
    maximumValue =max(zip(probabilityList.values(), probabilityList.keys()))
    return maximumValue[1]

for i in wronglyPredicedWord:
    sentenceList = {}
    #print("wronglyPredicedWord :"+str(i))
    similarWordList = d.suggest('fist')
    #similarWordList=['fist']
    for w in similarWordList:
        #print("similarWordList :"+str(w))
        tokens= nltk.word_tokenize(predictedString)
        sentence=' '
        for tok in tokens:
            #print("tok  :"+str(tok))
            if(tok.__eq__(i)):
                sentence=sentence+' '+w
            else:
                sentence = sentence + ' ' + tok
        sentenceList[w]=sentence.strip()
    wrd=getMaximumProbableWord(sentenceList)
    predictedString =predictedString.replace(i,wrd)

print(predictedString)

count=0

predictedStringTokens = nltk.word_tokenize(predictedString)

for i in range(0,len(predictedStringTokens)):
    if(predictedStringTokens[i].__eq__(correctStringTokens[i])):
        count=count+1


print("Accuracy  :"+str((count/len(predictedStringTokens))*100))
