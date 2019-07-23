import pandas as pd
import pymysql
from sqlalchemy import create_engine
import fire

pymysql.install_as_MySQLdb()
import MySQLdb

def insert_into(table1='afsnt', table2='afsnt_dly', table3='sfsnt'):
    user_id = str(input('id : '))
    pwd = str(input('password : '))
    db_name = str(input('database name : '))
    
    afsnt = pd.read_csv('./data/AFSNT.csv', encoding = 'cp949')
    afsnt_dly = pd.read_csv('./data/AFSNT_DLY.csv', encoding = 'cp949')
    sfsnt = pd.read_csv('./data/SFSNT.csv', encoding = 'utf-8')
    
    table1, table2, table3 = map(str, [table1, table2, table3])

    engine = create_engine('mysql+pymysql://'+user_id+':'+pwd+'@localhost/'+db_name, encoding='utf-8')
    con = engine.connect()
    afsnt.to_sql(name=table1, con=engine, if_exists='append', index=False)
    afsnt_dly.to_sql(name=table2, con=engine, if_exists='append', index=False)
    sfsnt.to_sql(name=table3, con=engine, if_exists='append', index=False)
    con.close()
    
def pprint(n='123'):
    print(n)
    
    
if __name__ == '__main__':
    fire.Fire({'insert_into':insert_into})