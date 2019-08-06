import pandas as pd
import datetime as dt
import fire
import tqdm



def calculate_STT_time(file_name, output_name):
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

    afsnt.loc[:, 'STT_TIME'] = 0
    REG_set = afsnt.groupby('REG').size().sort_values(ascending=False)

    new_afsnt = pd.DataFrame(columns=afsnt.columns)

    print(' >>> Calculating the time...')
    for REG in tqdm.tqdm(REG_set.keys(), mininterval=1):
        afsnt_apart = afsnt.loc[afsnt.REG==REG, :].sort_values(by=['REG', 'FLT', 'STT']).reset_index(drop=True)
        timedelta = [afsnt_apart.STT[i+1] - afsnt_apart.STT[i] for i in range(len(afsnt_apart.STT)-1)]

        afsnt_apart = _add_time(afsnt_apart, timedelta, 'STT_TIME')
        afsnt_apart = afsnt_apart.drop(['index'], axis=1)
        new_afsnt = pd.concat([new_afsnt, afsnt_apart])

    afsnt_apart = afsnt.loc[pd.isna(afsnt.REG), :]
    new_afsnt = pd.concat([new_afsnt, afsnt_apart])

    print(' >>> Writing the data')
    new_afsnt.to_csv(output_name, index = False)
    print(' >>> finished!')


def calculate_ATT_time(file_name, output_name):
    print(' >>> Load data')
    afsnt = pd.read_csv(file_name, encoding = 'utf-8')
    afsnt.ATT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.ATT]

    afsnt.loc[:, 'ATT_TIME'] = 0
    REG_set = afsnt.groupby('REG').size().sort_values(ascending=False)

    new_afsnt = pd.DataFrame(columns=afsnt.columns)

    print(' >>> Calculating the time...')
    for REG in tqdm.tqdm(REG_set.keys(), mininterval=1):

        afsnt_apart = afsnt.loc[afsnt.REG==REG, :].sort_values(by=['REG', 'FLT', 'ATT']).reset_index(drop=True)
        timedelta = [afsnt_apart.ATT[i+1] - afsnt_apart.ATT[i] for i in range(len(afsnt_apart.ATT)-1)]

        afsnt_apart = _add_time(afsnt_apart, timedelta, 'ATT_TIME')
        afsnt_apart = afsnt_apart.drop(['index'], axis=1)
        new_afsnt = pd.concat([new_afsnt, afsnt_apart])

    afsnt_apart = afsnt.loc[pd.isna(afsnt.REG), :]
    new_afsnt = pd.concat([new_afsnt, afsnt_apart])

    print(' >>> Writing the data')
    new_afsnt.to_csv(output_name, index = False)
    print(' >>> finished!')


def _add_time(afsnt_apart, timedelta, column):
    time = [int(t.days*24*60 + t.seconds/60) for t in timedelta]
    time.append(0)
    afsnt_apart.loc[:, column] = time

    afsnt_apart.loc[:, 'index'] = range(len(afsnt_apart))

    for i, FLT, TIME in afsnt_apart.loc[afsnt_apart.AOD=='D', ['index', 'FLT', column]].values:
        if i==len(afsnt_apart)-1:
            afsnt_apart.loc[i, column] = 0
        elif (afsnt_apart.loc[i+1, 'AOD']=='A') & (afsnt_apart.loc[i+1, 'FLT']==FLT):
            if (afsnt_apart.loc[i, 'DATE']==afsnt_apart.loc[i+1, 'DATE']):
                afsnt_apart.loc[i+1, column] = TIME
            else:
                afsnt_apart.loc[i, column] = 0
                afsnt_apart.loc[i+1, column] = 0
        else:
            afsnt_apart.loc[i, column] = 0

    for i, FLT in afsnt_apart.loc[afsnt_apart.AOD=='A', ['index', 'FLT']].values:
        if i==0:
            afsnt_apart.loc[i, column] = 0
        elif (afsnt_apart.loc[i-1, 'AOD']=='A') | (afsnt_apart.loc[i-1, 'FLT']!=FLT):
            afsnt_apart.loc[i, column] = 0
    return afsnt_apart


def count_num_flt(file_name, output_name):
    print(' >>> Load data')
    afsnt = pd.read_csv(file_name, encoding = 'cp949')

    afsnt.STT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.STT]

    print(' >>> Counting the number of flights...')
    for i in range(15, 0, -1):
        ARP = 'ARP'+str(i)
        print(' >>> Counting : '+ARP)
        afsnt_apart = afsnt.loc[afsnt.ARP==ARP, :].reset_index(drop=True)
        afsnt_apart.loc[:, 'NUM_FLT'] = 0
        STT = afsnt_apart.STT
        afsnt_apart.NUM_FLT = [sum((time - dt.timedelta(minutes=30) < STT) & (STT < time + dt.timedelta(minutes=30))) 
                               for time in tqdm.tqdm(afsnt_apart.STT, mininterval=1)]
        afsnt_apart.to_csv('./data/afsnt_'+ARP+'.csv', index = False)

    print(' >>> Concatenating data')
    afsnt_ARP = pd.read_csv('./data/afsnt_ARP1.csv', encoding = 'utf-8')
    for i in range(2, 16):
        afsnt_ARP_i = pd.read_csv('./data/afsnt_ARP'+str(i)+'.csv', encoding = 'utf-8')
        afsnt_ARP = pd.concat([afsnt_ARP, afsnt_ARP_i]).reset_index(drop=True)

    print(' >>> Writing the data')
    afsnt_ARP.to_csv(output_name, index = False)
    print(' >>> finished!')


if __name__ == '__main__':
    fire.Fire({'calculate_STT_time':calculate_STT_time, 
               'calculate_ATT_time':calculate_ATT_time, 
               'count_num_flt':count_num_flt})
