def etape3(f):
    brevets = []
    for j, i in enumerate(f):
        html = f[j]
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.find_all('a', href=True):
            brevets.append(a.get('href'))
        time.sleep(5)
    return brevets
