'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

from parsy import Parsy
import sys
import re
import pandas as pd
import nltk as nltk

if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(-1)
    
def split_it(sentence):
    return re.findall('([^\s]+)', sentence)

def extractType(page):
    # Code goes here
    mot = page.content.split(' ')	
    mot = list(filter(('').__ne__, mot))
    tags = nltk.pos_tag(mot)
    #print(tags)
    print(page.title)
    #print(tags[-1])
    for i, tag in enumerate(tags):
        if (tag[0] == 'is a') | (tag[0] == 'was a') | (tag[0] == 'are ') | (tag[0] == 'were') | (tag[0] == 'means') | (tag[0] == 'is an') | (tag[0] == 'was an'):
            print('page = ', page.title)
            print('tag', tag)
            types = tags[-1][0].lower().replace('.', '')
            print(types)
        else:
            pass
            types = tags[-1][0].lower().replace('.', '')
            print(types)
    return None



with open(sys.argv[2], 'w', encoding="utf-8") as output:
    for page in Parsy(sys.argv[1]):
        typ = extractType(page)
        if typ:
            output.write(page.title + "\t" + typ + "\n")
    
