import bs4 
import re
import requests

res = requests.get('https://www.merriam-webster.com/help/pronunciation-key')
soup = bs4.BeautifulSoup(res.text, "html.parser")
uls = soup.findAll("ul", { "class" : "pron_key_list" })
lis = []
pron_key_MW = []

lis = uls[0].findAll('li', recursive=False)
pron_key_MW.extend(li.text.split('\\')[1].strip() for li in lis)

lis = uls[1].findAll('li', recursive=False)
pron_key_MW.extend(li.text.split('\\')[1].strip() for li in lis)
pron_key_MW.append(u'\u022f')
pron_key_MW.append(u"\u022f i")
pron_key_MW.append(u'p')

lis = uls[2].findAll('li', recursive=False)
pron_key_MW.extend(li.text.split('\\')[1].strip() for li in lis)

import numpy as np
pron_key_MW = np.array(pron_key_MW)
for i in range(15):
    ind = [i, i+15, i+30]
    # print '\t'.join(repr(key.encode('raw_unicode_escape')) for key in pron_key_MW[ind])
    print '\t'.join(repr(key.encode('utf-8')) for key in pron_key_MW[ind])

# import pdb; pdb.set_trace()
