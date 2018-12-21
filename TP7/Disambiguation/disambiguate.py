'''Given as command line arguments
  (1) yagoLinks.tsv 
  (2) yagoLabels.tsv
  (3) wikipedia-ambiguous.txt
  (4) the output filename
  writes lines of the form
        title TAB entity
  where <title> is the title of the ambiguous
  Wikipedia article, and <entity> is the YAGO
  entity that this article belongs to. 
  It is OK to skip articles (do not output
  anything in that case). 
  (Public skeleton code)'''

import sys
import csv
from parser import Parser
from simpleKB import SimpleKB
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


yago = SimpleKB(sys.argv[1], sys.argv[2])
# yago is here an object containing 3 dictionaries:
## yago.links is a dictionary of type: entity -> set(entity).
##            It represents all the entities connected to a
##            given entity in the yago graph
## yago.labels is a dictionary of type: entity -> set(label).
##            It represents all the labels an entity can have.
## yago.rlabels is a dictionary of type: label -> set(entity).
##            It represents all the entities sharing a same label.

# Note that the class Page has a method Page.label(),
# which retrieves the human-readable label of an ambiguous
# Wikipedia page.


stemmer = SnowballStemmer("english")

with open(sys.argv[4], 'w', encoding="utf-8") as output:
    
    label_container = []
    link_container = []
    label_to_rlabel = {}
    stop_words = ["the", "of", "a", "to", "be", "from", "or", "on", "by", "is", "in", "was", "were"]
    
    for i, page in enumerate(Parser(sys.argv[3])):
    # Code goes here
        #if (i == 6):   break
        cont = page.content.split()
        for word in cont:
            if(word in stopwords.words('english')):
                cont.remove(word)

        content = []
        for x in cont:
            stemm = stemmer.stem(x)
            content.append(stemm)
        
        #
        titre = page.title
        label = page.label()
        rlabel_to_count = {}
        se = set()
        #print(content)
        
        try:
            #print('LABEL = ', label)
            rlabels = yago.rlabels.get(label)
            # Premier boucle rlabels
            score_rlabels = dict()
            for i, rl in enumerate(rlabels):
                
                tlab = []
                score_rlabels[rl] = 0
                elems = yago.labels.get(rl)
                elems = list(elems)
                for elem in elems:
                    elem = elem.split()
                    els = list()
                    for x in elem:
                        if(x not in stopwords.words('english')):
                            for x in elem:
                                els = stemmer.stem(x)
                for word in els:
                    if word in content:
                        score_rlabels[rl] += 1
            
                
                if(i == 2):
                    break
                links = yago.links.get(rl)
                for j, link in enumerate(links):
                  #  print('LINK = ', link)
                    lilabels = yago.labels.get(link)
                    #print(lilabels)
                    for lil in lilabels:
                        list_link_labels = lil.split()
                        new_list_link_labels = []
                        for elem in list_link_labels:
                            if elem not in stopwords.words('english'):
                                new_list_link_labels.append(elem)
                        #print(new_list_link_labels)
                        stemmed_list = []
                        for elem in new_list_link_labels:
                            stemmed_list.append(stemmer.stem(elem))
                        for stem in stemmed_list:
                            if(stem in content):
                                score_rlabels[rl] += 1
                                #print(score_rlabels)
                            
            lab = max(score_rlabels, key=score_rlabels.get)
            #print(lab)
            #print(page.title + "\t" + lab + '\n')
            output.write(page.title + "\t" + lab + '\n')


        except:
            pass
            