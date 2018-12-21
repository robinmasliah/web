def etape8(patent_json):
    patent_json = pd.DataFrame(patent_json)
    patent_json = patent_json.T
    engine = create_engine('sqlite:///:memory:')
    patent_json.to_sql('table2', engine)
    pd.read_sql_table('table2', engine)
    df = pd.read_sql_query("select * from 'table2' where 'Author' like '%FR%'", con=engine)
    return df
