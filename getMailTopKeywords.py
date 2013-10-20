#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from HTMLParser import HTMLParser
import math
import os
import pyzmail #http://www.magiksys.net/pyzmail/#
import sys
import time
import unicodedata

def main(argv):
    args = optionParser(argv)
    print('Reading from %s ... ' % args.folder)
    text = extractMailFromPath(args.folder)
    
    omitwords = decode('from to re de para subject asunto date fecha escribió de que no a la el es y en lo un por me qué una te los se con para mi está si pero las su yo tu del al como le eso sí esta ya más muy hay bien estoy todo nos tengo ha este cuando sólo vamos cómo estás o soy puedo esto quiero aquí tiene tú ahora algo fue son ser he era eres así sé tiene ese bueno creo todos sus puede voy tan esa porque dónde hacer quién nunca nada él estaba están quieres va sabes vez hace ella dos tenemos puedes sin hasta sr és per dels jo amb com ho has').split()
     #https://es.wiktionary.org/wiki/Ap%C3%A9ndice:Palabras_m%C3%A1s_frecuentes_del_espa%C3%B1ol

    language = 'en'    
    if args.lang:
        language = args.lang
    
    count = 10        
    if args.count:
        count = args.count
    
    print "Building a list of the top keywords..."
    if args.aspell:
        wordsInDict, wordsNotInDict = getWordsFromDictionary(language, text, omitwords)
    else:
        wordsInDict = getWords(text, omitwords)

    words = wordsInDict
    if args.nltk:
        words = stemWords(words, language)
    
    returnRepetitions(words, count)
    
def stemWords(list, lang):
    #http://nltk.org/index.html
    from nltk.stem import SnowballStemmer
    nltk = True
    if lang == "es":
        lang = "spanish"
    elif lang == "en":
        lang = "english"
    else:
        print "Language %s not supported in NLTK, not processing." % lang
        nltk = False
        lang = "english"

    if nltk:
        print "Processing using Natural Language Toolkit in %s..." % lang
        st = SnowballStemmer(lang)
        stemedList = []
        for word in list:
            stemedList.append(st.stem(word))
    else:
        stemedList = list
    
    return stemedList

def optionParser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="the folder to process",
                        type=str)
    parser.add_argument("-c", "--count", help="show words with count greater or equal than this number. Default: 10",
                        type=int)
    parser.add_argument("-a", "--aspell", help="whether to check the words using Aspell. Requires python-aspell library. See https://github.com/WojciechMula/aspell-python. Default: no",
                        action="store_true")

    parser.add_argument("-l", "--lang", help="check words in that language (only if -a is set).\nNeeds aspell dictionary in that language installed.\nDefault: en",
                        type=str)

    parser.add_argument("-n", "--nltk", help="use Natural Language Toolkit. Requires nltk library. See http://nltk.org/index.html. Default: no",
                        action="store_true")                        
                        
    args = parser.parse_args()
    
    if os.path.exists(args.folder):
        return args
    else:
        sys.exit('Sorry: directory %s does not exist!' % args.folder)

def getWordsFromDictionary(language, text, omitwords):
    import aspell
    #http://mx.answers.yahoo.com/question/index?qid=20090923123859AA0EO5m
    s = aspell.Speller('lang', language)
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    wordList1 = []
    wordList1 = text.lower().split(None)
    wordListInDictionary = []
    wordListNotInDictionary = []
    for word1 in wordList1:
        lastchar = word1[-1:]
        if lastchar in [",", ".", "!", "?", ";", ":"]:
            word2 = word1.rstrip(lastchar)
        else:
            word2 = word1
        if len(word2) > 1 and s.check(word2) and word2 not in omitwords:
            wordListInDictionary.append(word2)
        else:
            if word2 not in omitwords:
                wordListNotInDictionary.append(word2)
    
    return wordListInDictionary, wordListNotInDictionary
    
def getWords(text, omitwords):
    #http://programming-review.com/top-keywords-in-python/
    omitcharacterlist = '@ ( / -'.split()
    wordList1 = []
    wordList1 = text.lower().split(None)
    wordList2 = []
    for word1 in wordList1:
        lastchar = word1[-1:]
        if lastchar in [",", ".", "!", "?", ";"]:
            word2 = word1.rstrip(lastchar)
        else:
            word2 = word1
        # build a wordList2 of lower case modified words
        if len(word2.lower()) > 1 and word2.lower() not in omitwords:
            if not any(character in word2.lower() for character in omitcharacterlist):
                wordList2.append(word2.lower())
    
    return wordList2
    
def returnRepetitions(wordlist, repetitions):
    print "Top keywords:"
    # create word frequency dictionary  = hashtable
    Dict = {}
    for word in wordlist:
        Dict[word] = Dict.get(word, 0) + 1
    
    # create a list of keys and sort the list
    keys = Dict.keys()
    keys.sort()
    
    #function inside a function
    def byvalues(d):
        return d[1] 
    
    items = sorted(Dict.items(), key=byvalues, reverse=True)
    for item in items:
        if item[1] > repetitions:
            print " ", item[0], item[1]

def extractMailFromPath(path):
    numberOfFiles = 0
    for root, subFolders, files in os.walk(path):
        for filename in files[1:]:
            numberOfFiles += 1
    print "Analyzing %s mails..." % numberOfFiles
    counter = 0
    text = ""
    for root, subFolders, files in os.walk(path):
        for filename in files[1:]:
            counter += 1
            progress(50, counter*100/numberOfFiles)
            filePath = os.path.join(root, filename)
            text = text + extractMailFromFile(filePath)
    return text

def extractMailFromFile(filename):
    msg=pyzmail.PyzMessage.factory(open(filename, 'rb'))
    text = ""
    '''if len(msg.mailparts) > 1:
        for mailpart in msg.mailparts:
            if mailpart.is_body=='text/html':
                #print mailpart.charset
                payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None) 
                for line in payload.replace('\r',' ').split('\n'):
                    # omit lines starting with >, which is normally a quote for previous mail
                    if not line.startswith('>'):
                        text = text + line
        text = strip_tags(text)
    else:'''
    for mailpart in msg.mailparts:
        if mailpart.is_body=='text/plain':
            payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None) 
            for line in payload.replace('\r',' ').split('\n'):
                # omit lines starting with >, which is normally a quote for previous mail
                if not line.startswith('>'):
                    text = text + line

    return text

# http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def decode(s, encodings=('ascii', 'utf8', 'ISO-8859-1')):
    for encoding in encodings:
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            pass
    return s.decode('ascii', 'ignore')

# http://snipplr.com/view/25735/python-cli-command-line-progress-bar/
# width defines bar width
# percent defines current percentage
def progress(width, percent):
    marks = math.floor(width * (percent / 100.0))
    spaces = math.floor(width - marks)
    
    loader = '[' + ('=' * int(marks)) + (' ' * int(spaces)) + ']'
    
    sys.stdout.write("%s %d%%\r" % (loader, percent))
    if percent >= 100:
        sys.stdout.write("\n")
    sys.stdout.flush()
    
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print "\nCtrl+C detected, exiting."