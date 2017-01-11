import requests
import bs4 
import re
import time

# wordsfile = open('cmu.words', 'r')
# pronsfile = open('cmu.words.pron', 'r')
logfile = open('cmu.words.log', 'r')

# output file, look for the pronunciations of word not included in the dict
mypronfile = open('my.words.pron.oxford', 'w')
notfoundfile = open('my.words.notfound.oxford', 'w')

def pronounce(word, session):
    if word and session:
        # word = 'APLASTIC'
        # u = 'https://en.oxforddictionaries.com/definition/'+word.lower()
        # url = 'https://en.oxforddictionaries.com/definition/abetalipoproteinaemia'
        u = 'https://en.oxforddictionaries.com/search?filter=dictionary&query='+word
        #response = session.get(u, headers={"Accept" : "application/json, text/javascript, */*; q=0.01",
        response = session.get(u, headers={"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                             "X-Requested-With": "XMLHttpRequest",
                                             "Referer": "https://en.oxforddictionaries.com/",
                                             "Host": "en.oxforddictionaries.com"},
                                             allow_redirects=True)
        # print response.url
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        pron = soup.find_all("span", class_='phoneticspelling')
        #if word == 'ABETALIPOPROTEINEMIA':
            #import pdb; pdb.set_trace()
        if "Retry" in response.text[0:30]:
            return 'retry'
        if len(pron) > 0:
            # unicode 
            return '\t'.join(p.text for p in pron)
    return None


p = re.compile('Morpheme|By LtoS rules')
with requests.Session() as session:
    # session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"}
    session.get("https://en.oxforddictionaries.com/")
    for line in logfile:
        line = line.strip()
        if p.search(line):
            word = line.split(' - ')[0]
            print word
            pron = pronounce(word, session)
            while pron == 'retry':
                print 'wait for retrying'
                time.sleep(15)
                pron = pronounce(word, session)
            if not pron:
                notfoundfile.write(line + '\n')
            else:
                mypronfile.write((word + '\t' + pron + '\n').encode("utf-8"))
                print pron

logfile.close()
mypronfile.close()
notfoundfile.close()

