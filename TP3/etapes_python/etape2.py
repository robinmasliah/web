def etape2(f):
    brevets_html = []
    for i in range(1, 61):
        lien = "http://www.freepatentsonline.com/result.html?" + str(i) + "'sort=relevance&srch=top&query_txt=video&submit=&patents=on"
        brevets_html.append(etape1(lien))
        time.sleep(5)
    return brevets_html
