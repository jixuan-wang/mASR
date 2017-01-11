import re

obofile = open('hp.obo', 'r')
namefile = open('hp.names', 'w')

words = []
p = re.compile('"[A-Za-z ]*"')
for line in obofile:
    line = line.strip()
    temp = line.split(' ')
    if temp[0] == 'name:':
        words.extend(w.lower() for w in temp[1:])
        namefile.write(' '.join(temp[1:]) + '\n')
    elif temp[0] == 'synonym:':
        if p.search(line):
            name = p.search(line).group()
            words.extend(w.lower() for w in name[1:-1].split(' '))
            namefile.write(name[1:-1] + '\n')
obofile.close()

wordsfile = open('hp.words', 'w')
for w in sorted(words):
    wordsfile.write(w+'\n')
wordsfile.close()
namefile.close()
obofile.close()
