Bonjour,

Si vous avez python 3 et jupyter notebook je met en pièce jointe le .ipynb.

Sinon veuillez, s'il vous plait exécuter les lignes suivantes dans un interpréteur python :

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from sqlalchemy import create_engine
import pandas as pd
from tidylib import tidy_document
import re
import requests
import urllib
import time
import os
import json

url_link = 'http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on'

def etape1(url_link):
    f = urllib.request.urlopen(url_link).read()
    return f

def etape2(f):
    brevets_html = []
    for i in range(1, 61):
        lien = "http://www.freepatentsonline.com/result.html?" + str(i) + "'sort=relevance&srch=top&query_txt=video&submit=&patents=on"
        brevets_html.append(etape1(lien))
        time.sleep(5)
    return brevets_html

def etape3(f):
    brevets = []
    for j, i in enumerate(f):
        html = f[j]
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            brevets.append(a.get('href'))
        time.sleep(5)
    return brevets

def etape4(f):
    brevets_unique = set(f)
    list_brevets = list(brevets_unique)
    return list_brevets

def etape5(f):
    bon_lien = []
    
    for j, i in enumerate(f):
        string = f[j]
        result = re.search('(?<=/)\w+', string)
        if result is not None:
            bon_lien.append(string)
        else:
            pass
    return bon_lien

def etape6(f):
    liste_liens = pd.DataFrame(f)
    liste_liens.columns = ['a']
    engine = create_engine('sqlite:///:memory:')
    liste_liens.to_sql('table', engine)
    pd.read_sql_table('table', engine)
    df = pd.read_sql_query("select * from 'table' where a not like 'http%' and a not like '/se%' and a not like '/cont%' and a not like '/tools%' and a not like '/regist%' and a not like '/privac%' ", con=engine)
    liste_liens = list(df['a'])
    return liste_liens

def etape7(liste_liens):
    brevets = {}
    for j, i in enumerate(liste_liens):
        lien = "http://www.freepatentsonline.com" + str(liste_liens[j])
        html = etape1(lien)
        doc, error = tidy_document(html, options={'numeric-entities': 1})
        soup = BeautifulSoup(html, 'html.parser')
        brevets[lien] = {}
        for info in soup.find_all('form', {'name': 'biblio'})[0].find_all('input'):
            if info.get('name') == 'title':
                brevets[lien]['Title'] = info.get('value')
            elif info.get('name') == 'author':
                brevets[lien]['Author'] = info.get('value')
            elif info.get('name') == 'assignee':
                brevets[lien]['Assignee'] = info.get('value')
            elif info.get('name') == 'country':
                brevets[lien]['Country'] = info.get('value')
            elif info.get('name') == 'patent':
                brevets[lien]['Patent'] = info.get('value')
            elif info.get('name') == 'year':
                brevets[lien]['Year'] = info.get('value')
            elif info.get('name') == 'month':
                brevets[lien]['Month'] = info.get('value')
    time.sleep(5)
    with open('info_patents.json', 'w') as fp:
        json.dump(brevets, fp)
    return brevets

def etape8(patent_json):
    patent_json = pd.DataFrame(patent_json)
    patent_json = patent_json.T
    engine = create_engine('sqlite:///:memory:')
    patent_json.to_sql('table2', engine)
    pd.read_sql_table('table2', engine)
    df = pd.read_sql_query("select * from 'table2' where 'Author' like '%FR%'", con=engine)
    return df




brevets_html = etape2(url_link)
brevets = etape3(brevets_html)
print(brevets)
brevets_unique = etape4(brevets)
print(brevets_unique)
liste_liens = etape5(brevets_unique)
liste_liens = etape6(liste_liens)
print(liste_liens)
patent_json = etape7(liste_liens)
print(patent_json)
french_authors = etape8(patent_json)
french_authors.head()
