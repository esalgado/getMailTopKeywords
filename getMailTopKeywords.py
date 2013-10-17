#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import math
from HTMLParser import HTMLParser
from progress_bar import ProgressBar

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
    #First we get 
    numberOfFiles = 0
    for root, subFolders, files in os.walk(path):
        for filename in files[1:]:
            numberOfFiles += 1

    counter = 0
    text = ""
    for root, subFolders, files in os.walk(path):
        for filename in files[1:]:
            counter += 1
            progress(50, counter*100/numberOfFiles)
            filePath = os.path.join(root, filename)
            text = text + extractMailFromFile(filePath)

    getTopKeywords(text)

def extractMailFromFile(filename):
    #print filename
    msg=pyzmail.PyzMessage.factory(open(filename, 'rb'))
    #print len(msg.mailparts)
    #print msg.mailparts
    text = ""
    for mailpart in msg.mailparts:
        if mailpart.is_body=='text/plain':
        #if mailpart.is_body=='text/html':
            #print mailpart.charset
            payload, used_charset=pyzmail.decode_text(mailpart.get_payload(), mailpart.charset, None) 
            for line in payload.replace('\r',' ').split('\n'):
                # omit lines starting with >, which is normally a quote for previous mail
                if not line.startswith('>'):
                    text = text + line
    return text

def getTopKeywords(text):
    print "Building a list of the top keywords..."
    #http://programming-review.com/top-keywords-in-python/
    #https://es.wiktionary.org/wiki/Ap%C3%A9ndice:Palabras_m%C3%A1s_frecuentes_del_espa%C3%B1ol
    stoplist = decode('from: to: re: cc: de: para: subject: asunto: date: fecha: escribió: de que no a la el es y en lo un por me qué una te los se con para mi está si pero las su yo tu del al como le eso sí esta ya más muy hay bien estoy todo nos tengo ha este cuando sólo vamos cómo estás o soy puedo esto quiero aquí tiene tú ahora algo fue son ser he era eres así sé tiene ese bueno creo todos sus puede voy tan esa porque dónde hacer quién nunca nada él estaba están quieres va sabes vez hace ella dos tenemos puedes sin hasta sr és per dels jo amb com ho has').split()
    omitcharacterlist = '@ ( / -'.split()
    print "Top keywords:"
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
            if not any(character in word2.lower() for character in omitcharacterlist):
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
    for item in items:
        if item[1] > 50:
            print item[0], item[1]
    
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
    main(sys.argv)