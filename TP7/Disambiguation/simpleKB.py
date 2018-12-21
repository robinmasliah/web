'''A simplified knowledge base with just
links between entities and labels'''

__author__ = "Jonathan Lajus"

def load(fileName, container, reverseContainer = None):
    with open(fileName, encoding="ISO-8859-1") as file:
        print("Loading",fileName,end="...",flush=True)
        for line in file:
            splitLine = line.split('\t')
            if len(splitLine) is not 2:
                raise RuntimeError('The file is not a valid KB file')
            subject=splitLine[0]
            obj=splitLine[1].strip('"\n')
            container.setdefault(subject,set()).add(obj)
            if reverseContainer!=None:
                reverseContainer.setdefault(obj,set()).add(subject)
        print("done",flush=True) 

class SimpleKB:
    def __init__(self, yagoLinksFile, yagoLabelsFile):
        self.links = {}
        self.labels = {}
        self.rlabels = {}
        load(yagoLinksFile, self.links, self.links)
        load(yagoLabelsFile, self.labels, self.rlabels)
