import re

wordfile = open('hp.words', 'r')

words = wordfile.readlines()
words = sorted(list(set(sorted(words))))

cleanfile = open('hp.words.clean', 'w')
p = re.compile("^[a-z-]+$")
for word in words:
    word = word.strip()
    if p.match(word):
        cleanfile.write(word+'\n')
cleanfile.close()
