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
                        Requires python-aspell library. See
                        https://github.com/WojciechMula/aspell-python.
  -l LANG, --lang LANG  check words in that language (only if -a is set).
                        Needs aspell dictionary in that language installed.
                        Default: en
  -n, --nltk            use Natural Language Toolkit. Default: no
                        Requires nltk library.
                        See http://nltk.org/index.html. 
````
Example:
````
./getMailTopKeywords.py -a -c 10 -l es /home/esalgado/GmailBackup/2005-12
Reading from /home/esalgado/GmailBackup/2005-12 ... 
Analyzing 42 mails...
[==================================================] 100%
Building a list of the top keywords...
Top keywords:
  mas 21
  correo 20
  foto 18
  infantil 15
  seguridad 13
  enero 13
  parque 11
  servicios 11
  nuevos 11
````
Example using NLTK (extracts the roots of the words):
````
./getMailTopKeywords.py -a -c 10 -l es -n /home/esalgado/GmailBackup/2005-12
Reading from /home/esalgado/GmailBackup/2005-12 ... 
Analyzing 42 mails...
[==================================================] 100%
Building a list of the top keywords...
Processing using Natural Language Toolkit...
Top keywords:
  mas 21
  envi 20
  corre 20
  fot 20
  nuev 19
  infantil 15
  servici 14
  activ 14
  ener 13
  segur 13
  mes 12
  monitor 12
  parqu 11
````
