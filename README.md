getMailTopKeywords
==================

Scans mail folders and returns a count of repeated words. I'm using it with a backup 
of Gmail I got using "Backup Gmail"
https://code.launchpad.net/~cfraire/backup-gmail/devel

Requires pyzmail library: 
http://www.magiksys.net/pyzmail/
````
usage: getMailTopKeywords.py [-h] [-c COUNT] [-a] [-l LANG] [-n] folder

positional arguments:
  folder                the folder to process

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        show words with count greater or equal than this
                        number. Default: 10
  -a, --aspell          whether to check the words using Aspell. Default: no
                        Requires python-aspell library. 
                        See https://github.com/WojciechMula/aspell-python.
  -l LANG, --lang LANG  check words in that language (only if -d is set).
                        Default: es
  -n, --nltk            use Natural Language Toolkit. Default: no
                        Requires nltk library.
                        See http://nltk.org/index.html. 
````
