def etape1(url_link):
    f = urllib.request.urlopen(url_link).read()
    return f
