import pandas as pd
import datetime as dt
import fire
import tqdm

# python dataframe.py calculate_time ./data/AFSNT.csv ./data/AFSNT_addtime.csv

def calculate_time(file_name, output_name):
    print(' >>> Load data')
    afsnt = pd.read_csv(file_name, encoding = 'cp949')

    afsnt.loc[:, 'DATE'] = [dt.date(int(line[0]), int(line[1]), int(line[2])) for line in afsnt.values]
    afsnt = afsnt.drop(['SDT_YY', 'SDT_MM', 'SDT_DD', 'SDT_DY'], axis=1)

    STT = [i.split(':') for i in afsnt.STT]
    afsnt.STT = [dt.time(int(h), int(m)) for h, m in STT]
    ATT = [i.split(':') for i in afsnt.ATT]
    afsnt.ATT = [dt.time(int(h), int(m)) for h, m in ATT]

    afsnt['STT'] = [dt.datetime.combine(i, j) for i, j in zip(afsnt['DATE'], afsnt['STT'])]
    afsnt['ATT'] = [dt.datetime.combine(i, j) for i, j in zip(afsnt['DATE'], afsnt['ATT'])]

    afsnt.loc[:, 'TIME'] = 0
    REG_set = afsnt.groupby('REG').size().sort_values(ascending=False)

    new_afsnt = pd.DataFrame(columns=afsnt.columns)

    print(' >>> Calculating the time...')
    for REG in tqdm.tqdm(REG_set.keys(), mininterval=1):
        afsnt_apart = afsnt.loc[afsnt.REG==REG, :].sort_values(by=['REG', 'FLT', 'STT']).reset_index(drop=True)

        time = [(afsnt_apart.ATT[i+1] - afsnt_apart.ATT[i]).seconds for i in range(len(afsnt_apart.STT)-1)]
        time.append(0)
        afsnt_apart.loc[:, 'TIME'] = time
        afsnt_apart.loc[:, 'TIME'] = (afsnt_apart.loc[:, 'TIME']/60).astype(int)

        afsnt_apart.loc[:, 'index'] = range(len(afsnt_apart))

        for i, FLT, TIME in afsnt_apart.loc[afsnt_apart.AOD=='D', ['index', 'FLT', 'TIME']].values:
            if i==len(afsnt_apart)-1:
                afsnt_apart.loc[i, 'TIME'] = 0
            elif (afsnt_apart.loc[i+1, 'AOD']=='A') & (afsnt_apart.loc[i+1, 'FLT']==FLT):
                afsnt_apart.loc[i+1, 'TIME'] = TIME
            else:
                afsnt_apart.loc[i, 'TIME'] = 0

        for i, FLT, TIME in afsnt_apart.loc[afsnt_apart.AOD=='A', ['index', 'FLT', 'TIME']].values:
            if i==0:
                afsnt_apart.loc[i, 'TIME'] = 0
            elif (afsnt_apart.loc[i-1, 'AOD']=='A') | (afsnt_apart.loc[i-1, 'FLT']!=FLT):
                afsnt_apart.loc[i, 'TIME'] = 0

        afsnt_apart = afsnt_apart.drop(['index'], axis=1)
        new_afsnt = pd.concat([new_afsnt, afsnt_apart])

    new_afsnt.to_csv(output_name, index = False)
    print(' >>> finished!')


def count_num_flt(file_name, output_name):
    print(' >>> Load data')
    afsnt = pd.read_csv(file_name, encoding = 'cp949')

    afsnt.STT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.STT]
    afsnt.ATT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.ATT]

    print(' >>> Counting the number of flights...')
    for i in tqdm.tqdm(range(15, 0, -1), mininterval=1):
        ARP = 'ARP'+str(i)
        afsnt_apart = afsnt.loc[afsnt.ARP==ARP, :].reset_index(drop=True)
        afsnt_apart.loc[:, 'NUM_FLT'] = 0
        STT = afsnt_apart.STT
        afsnt_apart.NUM_FLT = [sum((time - dt.timedelta(minutes=30) < STT) & (STT < time + dt.timedelta(minutes=30))) 
                               for time in afsnt_apart.STT]
        afsnt_apart.to_csv('./data/afsnt_'+ARP+'.csv', index = False)

    print(' >>> Concatenate data')
    afsnt_ARP = pd.read_csv('./data/afsnt_ARP1.csv', encoding = 'utf-8')
    for i in range(2, 16):
        afsnt_ARP_i = pd.read_csv('./data/afsnt_ARP'+str(i)+'.csv', encoding = 'utf-8')
        afsnt_ARP = pd.concat([afsnt_ARP, afsnt_ARP_i]).reset_index(drop=True)
    afsnt_ARP.to_csv(output_name, index = False)
    print(' >>> finished!')


if __name__ == '__main__':
    fire.Fire({'calculate_time':calculate_time, 
               'count_num_flt':count_num_flt})