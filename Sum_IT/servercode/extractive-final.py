from nltk.stem import PorterStemmer
import nltk.classify.util
#from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#from collections import OrderedDict
import collections
import math
import heapq
#import bs4 as bs  
#import urllib.request
from nltk import ngrams
import os
import glob
import itertools
import operator
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import sys
import re

sentenceList = []
sentenceListEn = []
wordListDoc = []
wordListVocab = collections.defaultdict(list)
vocabidf = {}
sentence_score = {}
summary = ""
summaryNew = []
articlegram = []
summarygram = []
wordGraph = {}

rogue = []
senListComplete = []
sumListComplete = []
Vocabulary = {}
filteredWords = {}
scoreGraph = {}

path = 'stories/*'
files = glob.glob(path)

"""
Allowed POS Tagging
"""
allowedPOS=['J','V','R','N']


"""
    Porter Stemmer
"""
def word_stemming(word):
     return ps.stem(word)


"""
    Function for Punctuation Removal
"""
def punctuation_remove(word):
    punctuations = '''!()-[]{};:'"\,<>./?@#+=$%^&*_~'''
    # remove punctuation from the string
    no_punct = ""
    for char in word:
        if char not in punctuations and not char.isdigit():
            no_punct = no_punct + char
    return no_punct


"""
    Preprocessing omn Input Sentence 
"""

def sentenceCreation(inputSentenceList, outSentenceList):
    
    for inptemp in inputSentenceList:
        inp = []
        inp = inptemp.split()
        itemListNew = []
        item = []
        itemList = ''
        """POS Tagging"""
        posTagged= nltk.pos_tag(inp)
        for word in posTagged:
            if word[1][0] in allowedPOS:
                item.append(word[0].lower())
        for word in item:
            ## Call to punctuation removal ##
            word = punctuation_remove(word)
            if word != '' and word.lower() not in stops:
                wordNew  = word_stemming(word)                
                itemListNew.append(wordNew.lower())
        itemList = ' '.join(itemListNew)
        outSentenceList.append(itemList)


"""
Tokenizing sentence 

"""
def tokenize(sentenceList):
    for item in sentenceList:
        wordListDoc.append(item.split())
    """Creating vocabList with tf-idf value"""
    tfidf(wordListDoc)
        
    
"""
Calculating tf-idf
"""
def tfidf(wordList):
    i = 0
    for item in wordList:
        itemDict = {}
        for word in item:
            if word in itemDict:
                itemDict[word] += 1
            else:
                itemDict[word] = 1
        for word in itemDict:
            itemapnd = {}
            itemapnd[i] = itemDict[word]/len(itemDict)
            if word in wordListVocab:
                listTemp = []
                listTemp = wordListVocab[word]
                listTemp.append(itemapnd)
                wordListVocab[word] = listTemp
            else:
                listTemp = []
                listTemp.append(itemapnd)
                wordListVocab[word] = listTemp
        i += 1
    for item in wordListVocab:
        listTemp = []
        listTemp = wordListVocab[item]
        matchdoc = len(listTemp)
        totaldoc = len(wordList)
        idf = math.log10(totaldoc/matchdoc)
        vocabidf[item] = idf
        for listItem in listTemp:
            for key, value in listItem.items():
                val = listItem[key]
                listItem[key] = val * idf
        
        

"""
Ranking Sentences
"""
def rankSentence(wordListDoc):
    i = 0
    for item in wordListDoc:
        for word in item:
            listTemp = []
            listTemp = wordListVocab[word]
            for listItem in listTemp:
                for key, value in listItem.items():
                    if(key == i):
                        if i not in sentence_score:
                            sentence_score[i] = listItem[key]
                        else:
                            sentence_score[i] += listItem[key]
        i = i +1
            
    

"""
Showing Summary
"""
def showSummary(n, sentence_score):
    sumSize = int(n * 0.15)
    sort = []
    if sumSize == 0:
        sumSize = 1
    
    summary_sentences = heapq.nlargest(sumSize, sentence_score, key=sentence_score.get)
    sort = sorted(summary_sentences, key=int)
    for i in sort:
        summaryNew.append(sentenceList[i])
    summary = '\n\n '.join(summaryNew)
    print(summary)
    file = open("./servercode/sample.txt","w")
    file.write(summary)
    file.close()
    
"""
"""
def createWordGraph(article):
    #for listItem in article:
    wordList = article.split()
    filteredList_temp = []
    allList_temp = []
    wordGraphNode = {}
    prevWord = ""
    dictTemp = {}
    unigram = []
    bigram = []
    trigram = []
    ngram = []
    i = 0
    k = 0
    prevword = ""
    prevprevword = ""
    for word in wordList:
        wordNew = word.split("_")
        if wordNew[0].lower() not in stops:
            
            #word = ps.stem(wordNew[0]).lower()
            word = wordNew[0].lower()
            """
            Creating Vocabulary and Count
            """
            if word not in Vocabulary:
                Vocabulary[word] = 1
            else:
                Vocabulary[word] += 1
            if k == 0:
                unigram.append((word,))
                prevword = word
            elif k == 1:
                unigram.append((word,))
                bigram.append((prevword, word))
                prevprevword = prevword
                prevword = word               
                
            elif k == 2:
                unigram.append((word,))
                bigram.append((prevword, word))
                trigram.append((prevprevword, prevword, word))
                prevprevword = prevword
                prevword = word            
            else:
                unigram.append((word,))
                bigram.append((prevword, word))
                trigram.append((prevprevword, prevword, word))
                prevprevword = prevword
                prevword = word
            k += 1
                
        else:
            k = 0
            prevprevword = ""
            prevword = ""
             
        
        try:
            if wordNew[0].lower() not in stops:
                #word = ps.stem(wordNew[0])
                word = wordNew[0].lower()
                if word not in filteredList_temp:
                    filteredList_temp.append(word.lower())
                    allList_temp.append(word.lower())
                else:
                    allList_temp.append(word.lower())
                dictTemp[i] = 1
                if (i-1) in dictTemp.keys():
                    if(dictTemp[i-1] == 1):
                        if prevWord in wordGraphNode.keys():
                            makeList = []
                            makeList = wordGraphNode[prevWord]
                            makeList.append(word.lower())
                            wordGraphNode[prevWord] = makeList
                        else:
                            makeList = []
                            makeList.append(word.lower())
                            wordGraphNode[prevWord] = makeList
                        if word.lower() in wordGraphNode.keys():
                            makeList = []
                            makeList = wordGraphNode[word.lower()]
                            makeList.append(prevWord)
                            wordGraphNode[word.lower()] = makeList
                        else:
                            makeList = []
                            makeList.append(prevWord)
                            wordGraphNode[word.lower()] = makeList
                prevWord = word.lower()
            else:
                #if word not in allList_temp:
                    #allList_temp.append(word.lower())
                pass
                dictTemp[i] = 2
        except IndexError:
            pass
        i += 1
    #ngram = list(itertools.chain(unigram, bigram, trigram))
    #ngramGraph[key] = ngram
    wordGraph[str("1")] = wordGraphNode    
    filteredWords[str("1")] = filteredList_temp
    createSCore(filteredWords)
    makescoreGraph(filteredWords)
    #allWords[key] = allList_temp

"""
"""

def createSCore(filteredWords):
    for key, val in  filteredWords.items():
        scoreNode = {}
        for i in range(len(filteredWords[key])):
            scoreNode[i] = 1/len(filteredWords[key])
        scoreGraph[key] = scoreNode
    
def makescoreGraph(filteredWords):   
    for key, val in  filteredWords.items():    
        for k in range(10):
            #scoreNode = {}
            nodesum = 0
            for i in range(len(filteredWords[key])):
                #listNeighbours = []
                wij = 0
                wjk = 0
                nodesum = 0
                if filteredWords[key][i] in  wordGraph[key].keys():
                    listNeighbours = wordGraph[key][filteredWords[key][i]]
                    for item in listNeighbours:
                        wij = listNeighbours.count(item)
                        indexofj = listNeighbours.index(item)
                        nbrsNeighbours = wordGraph[key][item]
                        for subsequentitems in nbrsNeighbours:
                            wjk += nbrsNeighbours.count(subsequentitems)
                        nodesum += ((wij*scoreGraph[key][indexofj])/(wjk)) + ((0.15)*(1/len(filteredWords[key])))
                else:
                    wij = 0
                    wjk = 1
                    nodesum += ((wij*scoreGraph[key][indexofj])/(wjk)) + ((0.15)*(1/len(filteredWords[key])))
                scoreGraph[key][i] = (0.85)*nodesum
  

def wordCloud():
    
    for key, val in scoreGraph.items():
        n = len(scoreGraph[key])
        num = int(0.1*n)
        sortedlist = sorted(scoreGraph[key].items(), key=operator.itemgetter(1), reverse = True)
        for i in range(num):
            #print(sortedlist[i][0])
            print(filteredWords[str("1")][sortedlist[i][0]])

def findmetrics(sentence_score, inpSummary, k):
   
    sumSize = len(inpSummary)
    summary_sentences = heapq.nlargest(sumSize, sentence_score, key=sentence_score.get)
    for i in summary_sentences:
        kgram = ngrams(sentenceListEn[i].split(), k)
        for grams in kgram:
            articlegram.append(grams)
    for item in inpSummary:
        kgram = ngrams(item.split(), k)
        for grams in kgram:
            summarygram.append(grams)
        
def calculateRogue(articlegram, summarygram):
    count = 0
    for item in articlegram:
        if item in summarygram:
            count += 1
    qval = len(summarygram)
    rogue.append(count/qval)
    
"""
Reading StopWords 
"""

with open('./servercode/stopwords.txt', 'r') as stopFile:
    stops = stopFile.read().split('\n')
        
ps = PorterStemmer() 


"""
    Converting Input in Sentence Vector
"""

sentenceList = []
sentenceListOrig = []
summaryList = []
summaryListEn = []

"""
with open('withHeadlines.txt', 'r', encoding="utf8") as inpFile:
    FIleInp = inpFile.read().split('\n')
    for item in FIleInp:
        if item != "":
            sentenceListOrig.append(item.strip())
i = 0
for item in sentenceListOrig:
    if i == 1:
        summaryList.append(item)
        i = 0
    if item == "@highlight":
        i = 1        
    if i == 0:
        sentenceList.append(item)
        i = 0

"""

"""
Pass your string to this variable
"""
inputString = sys.argv[1]


sentenceList = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', inputString)            
sentenceCreation(sentenceList, sentenceListEn)
#sentenceCreation(summaryList, summaryListEn)
tokenize(sentenceListEn)
rankSentence(wordListDoc)
n = len(wordListDoc)
showSummary(n, sentence_score)
createWordGraph(inputString)
#print("Word Cloud")
wordcloud = WordCloud().generate(inputString)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

wordcloud.to_file("./servercode/first_review.png")