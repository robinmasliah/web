def etape6(f):
    liste_liens = pd.DataFrame(f)
    liste_liens.columns = ['a']
    engine = create_engine('sqlite:///:memory:')
    liste_liens.to_sql('table', engine)
    pd.read_sql_table('table', engine)
    df = pd.read_sql_query("select * from 'table' where a not like 'http%' and a not like '/se%' and a not like '/cont%' and a not like '/tools%' and a not like '/regist%' and a not like '/privac%' ", con=engine)
    liste_liens = list(df['a'])
    return liste_liens
