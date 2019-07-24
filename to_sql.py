import pandas as pd
import datetime as dt
import pymysql
from sqlalchemy import create_engine
import fire

pymysql.install_as_MySQLdb()
import MySQLdb


def insert_into(table1='afsnt', table2='sfsnt', table3='afsnt_dly'):
    afsnt = pd.read_csv('./data/AFSNT.csv', encoding = 'cp949')
    sfsnt = pd.read_csv('./data/SFSNT.csv', encoding = 'utf-8')
    afsnt_dly = pd.read_csv('./data/AFSNT_DLY.csv', encoding = 'cp949')
    
    afsnt.loc[:, 'DATE'] = [dt.date(int(line[0]), int(line[1]), int(line[2])) for line in afsnt.values]
    afsnt = afsnt.drop(['SDT_YY', 'SDT_MM', 'SDT_DD', 'SDT_DY'], axis=1)
    afsnt_dly.loc[:, 'DATE'] = [dt.date(int(line[0]), int(line[1]), int(line[2])) for line in afsnt_dly.values]
    afsnt_dly = afsnt_dly.drop(['SDT_YY', 'SDT_MM', 'SDT_DD', 'SDT_DY'], axis=1)
    
    user_id = str(input('id : '))
    pwd = str(input('password : '))
    db_name = str(input('database name : '))
    
    table1, table2, table3 = map(str, [table1, table2, table3])
    
    engine = create_engine('mysql+pymysql://'+user_id+':'+pwd+'@localhost/'+db_name, encoding='utf-8')
    con = engine.connect()
    afsnt.to_sql(name=table1, con=engine, if_exists='append', index=False)
    sfsnt.to_sql(name=table2, con=engine, if_exists='append', index=False)
    afsnt_dly.to_sql(name=table3, con=engine, if_exists='append', index=False)
    con.close()



if __name__ == '__main__':
    fire.Fire({'insert_into':insert_into})