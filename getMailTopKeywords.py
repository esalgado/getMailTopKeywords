#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import locale
import stripHTML
from HTMLParser import HTMLParser

try:
    import pyzmail
except ImportError:
    if os.path.isdir('../pyzmail'):
        sys.path.append(os.path.abspath('..'))
    elif os.path.isdir('pyzmail'):
        sys.path.append(os.path.abspath('.'))
    import pyzmail

def main(argv):
    if len(sys.argv) < 0:
        sys.exit('Usage: %s Directory containing mails (including subfolders)' % sys.argv[0])

    print "Reading from: " + argv[1]
    
    extractMailFromPath(argv[1])

def extractMailFromPath(path):
    listing = os.listdir(path)
    text = ""
    for root, subFolders, files in os.walk(path):
    #for directory in listing:
        for filename in files:
            filePath = os.path.join(root, filename)
        #for infile in directory:    
            #print filePath
            text = text + extractMailFromFile(filePath)
        
    getTopKeywords(text)

def extractMailFromFile(filename):
    msg=pyzmail.PyzMessage.factory(open(filename, 'rb'))
    #print len(msg.mailparts)
    #print msg.mailparts
    str_list = []
    for mailpart in msg.mailparts:
        if mailpart.is_body=='text/plain':
        #if mailpart.is_body=='text/html':
            payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None) 
            for line in payload.split('\n'):
                if line:
                    str_list.append(`line`)
                    #print line
                    #print stripHTML.strip_tags(line)"""
    return ''.join(str_list)

#http://programming-review.com/top-keywords-in-python/
def getTopKeywords(text):
    #https://es.wiktionary.org/wiki/Ap%C3%A9ndice:Palabras_m%C3%A1s_frecuentes_del_espa%C3%B1ol
    stopwords = 'de que no a la el es y en lo un por me qué una te los se con para mi está si pero las su yo tu del al como le eso sí esta ya más muy hay bien estoy todo nos tengo ha este cuando sólo vamos cómo estás o soy puedo esto quiero aquí tiene tú ahora algo fue son ser he era eres así sé tiene ese bueno creo todos sus puede voy tan esa porque dónde hacer quién nunca nada él estaba están quieres va sabes vez hace ella dos tenemos puedes sin hasta sr'
    stoplist = stopwords.split()
    print "Top keywords"
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
        if len(word2.lower()) > 1 and word2.lower() not in stoplist:
            wordList2.append(word2.lower())
        
    # create word frequency dictionary  = hashtable
    Dict = {}
    for word2 in wordList2:
        Dict[word2] = Dict.get(word2, 0) + 1
    
    # create a list of keys and sort the list
    keys = Dict.keys()
    keys.sort()
    
    #function inside a function
    def byvalues(d):
        return d[1] 
    
    items = sorted(Dict.items(), key=byvalues, reverse=True)
    # Print the first 40
    #for item in items[:10]:
    for item in items[:40]:
        print item[0].encode('utf-8'), item[1]
    
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
    
if __name__ == "__main__":
    main(sys.argv)