import nltk
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk import ConditionalFreqDist
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


from PIL import Image

from PIL import Image
from collections import defaultdict
import pytesseract
import re
from collections import Counter
from nltk import tokenize
from difflib import SequenceMatcher
from nltk.corpus import words

st1='that  some  background knowledge of  microbiology  and biochemistry will  help  in  understanding and fllewing  the protools  presented '
st2='  The final chapter  is  a  lengthy  discussion of cloning veciors '
st3='USA and Conde  rest  of  word  pages ISBN  The  definitive  source  of established name  for drug sin  the  USA cover jom proppietary'
st4='codes and official  names  of  substances  in the United  States Pharmacopeis and the  National  Formulary'


st11='that  some  background knowledge of  microbiology  and biochemistry will  help  in  understanding and flowinng  the protocols  presented '
st12='  The final chapter  is  a  lengthy  discussion of cloning vectors '
st13='USA and Canada  rest  of  word  pages ISBN  The  definitive  source  of established name  for drugs in  the  USA cover jom proppietary'
st14='codes and official  names  of  substances  in the United  States Pharmacopeias and the  National  Formulary'

correctList=[]
correctList.append(st11)
correctList.append(st12)
correctList.append(st13)
correctList.append(st14)

sentenceTest=[]
sentenceTest.append(st1)
sentenceTest.append(st2)
sentenceTest.append(st3)
sentenceTest.append(st4)

import enchant
import difflib


import re

unigramDict={}
unigramWordCount=0
bigramDict={}
bigramWordCount=0

file=open("new4.txt", "r",encoding="utf8")
for f in file.readlines():
    st=f.split('.')
    for sentence in st:
        s = re.sub(r'[^\w\s]', '', sentence.strip('\n'))
        if(len(s)>0):
            st=s.strip()
            #print(st)
            tokens = nltk.word_tokenize(st)
            for tok in tokens:
                if tok not in unigramDict:
                    unigramWordCount=unigramWordCount+1
                    unigramDict[tok] = 1
                else:
                    unigramDict[tok] = unigramDict.get(tok) + 1
            bigrm = nltk.bigrams(tokens)
            for big in bigrm:
                if big not in bigramDict:
                    bigramWordCount=bigramWordCount+1
                    bigramDict[big] = 1
                else:
                    bigramDict[big] = bigramDict.get(big) + 1

print(bigramDict)
print(unigramDict)


uniqueWordCount = {}
total = 0
wordList=[]
file=open("C:/Users/karna/PycharmProjects/untitled/venv/Lib/Dictionary.txt", "r",encoding="utf8")
for f in file.readlines():
    s = re.sub(r'[^\w\s]', '',f)
    tokens = nltk.word_tokenize(s)
    for i in tokens:
        wordList.append(i)

list_set = set(wordList)
unique_list = (list(list_set))

d = enchant.Dict("en_US")
incorrectSpellingList=[]
for i in sentenceTest:
    tokens = nltk.word_tokenize(i)
    for tok in tokens:
        if tok not in unique_list:
            incorrectSpellingList.append(tok)

print(incorrectSpellingList)

def getTheMostProbableWord(predSentence):
    probabilityList = {}
    sent = ''
    predictedSentence=predSentence
    #print("predictedSentence  :"+str(predictedSentence))
    tks = nltk.word_tokenize(predictedSentence)
    #print(predictedSentence)
    for tk in tks:
        if tk in incorrectSpellingList:
            finalWordList = []
            probabilityList = {}
            #print("misSpeltWord  :"+str(tk))
            similarWordList = d.suggest(tk)
            #print("similarWordList  :"+str(similarWordList))
            for word in similarWordList:
                words = re.findall('[a-z]+', word.lower())
                if (len(words) > 1):
                    print('c')
                else:
                    finalWordList.append(word)
            print("finalWordList  :"+str(similarWordList))
            for wrd in finalWordList:
                print("wrd  :"+str(wrd))
                sent= predictedSentence[:predictedSentence.find(tk)]
                print('sent  :'+str(sent))
                extractString = predictedSentence[:predictedSentence.find(tk)]+" "+wrd
                print(extractString)
                tokens = nltk.word_tokenize(extractString)
                bigrm = nltk.bigrams(tokens)
                probabilityValue = 1
                for b in bigrm:
                    if b in bigramDict and b[0] in unigramDict:
                        probabilityValue = probabilityValue * (bigramDict.get(b) / unigramDict.get(b[0]))
                    else:
                        probabilityValue = probabilityValue * 0.01
                probabilityList[wrd] = probabilityValue
            max_v = max(zip(probabilityList.values(), probabilityList.keys()))
            predictedSentence=predictedSentence.replace(tk,max_v[1])
       # print("final sentence :"+str(predictedSentence))
    return predictedSentence

finalResult=[]
for i in sentenceTest:
    st=getTheMostProbableWord(i)
    print("stt.."+st)
    finalResult.append(st)


for i in range(0,len(sentenceTest)):
    totalAccuracy = 0
    predictedStringTokens = nltk.word_tokenize(finalResult[i])
    correctStringTokens = nltk.word_tokenize(correctList[i])
    for i in range(0, len(predictedStringTokens)):
        if (predictedStringTokens[i].__eq__(correctStringTokens[i])):
            totalAccuracy = totalAccuracy + 1
    totalAccuracy=((totalAccuracy / len(predictedStringTokens)) * 100)+totalAccuracy

print("Final Accuracy  :"+str(totalAccuracy/len(sentenceTest)))


