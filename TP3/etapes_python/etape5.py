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
