file=open("org-op.txt", "r",encoding="utf8")

correctSentence=[]
predictedSentence=[]

import nltk

sent=''
totalAccuracy=0
totalLines=0

for f in file.readlines():
    if(f.startswith('ORG:')):
        sent=f.replace('ORG:','')
        totalLines=totalLines+1
        print(sent)
        correctSentence.append(sent.strip())
    if (f.startswith('O/P:')):
        totalCount=0
        Accuracy=0
        sent2=f.replace('O/P:','')
        lineCount=0
        predictedStringTokens = nltk.word_tokenize(sent2)
        correctStringTokens=nltk.word_tokenize(sent)
        for i in range(0, len(predictedStringTokens)):
            if(i<len(predictedStringTokens) and i<len(correctStringTokens)):
                lineCount=lineCount+1
                if (predictedStringTokens[i].__eq__(correctStringTokens[i])):
                    totalCount = totalCount + 1
        Accuracy=((totalCount/lineCount)*100)
        totalAccuracy=totalAccuracy+Accuracy

print("total Accuracy  :"+str(totalAccuracy/totalLines))
