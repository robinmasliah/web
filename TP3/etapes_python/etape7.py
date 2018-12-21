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
