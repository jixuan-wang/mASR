import requests
import bs4 
import re

# wordsfile = open('cmu.words', 'r')
# pronsfile = open('cmu.words.pron', 'r')
logfile = open('my.words.notfound.oxford', 'r')

# output file, look for the pronunciations of word not included in the dict
mypronfile = open('my.words.pron.oxford.mw', 'w')
notfoundfile = open('my.words.notfound.oxford.mw', 'w')

def pronounce(word):
    response = requests.get('http://c.merriam-webster.com/medlineplus/'+word)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    ele = soup.findAll("div", { "class" : "pag-count-one" })
    if len(ele) == 1 and ele[0].text == 'One entry found.':
        pr = soup.findAll("span", { "class" : "pr" })
        if len(pr) == 1:
            # unicode 
            pron = pr[0].text
            return pron
    return None


p = re.compile('Morpheme|By LtoS rules')
for line in logfile:
    line = line.strip()
    if p.search(line):
        word = line.split(' - ')[0]
        print word
        pron = pronounce(word)
        if pron:
            mypronfile.write((word + '\t' + pron + '\n').encode("utf-8"))
        else:
            notfoundfile.write(line + '\n')

logfile.close()
mypronfile.close()
notfoundfile.close()

