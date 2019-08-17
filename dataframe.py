import os
import pandas as pd
import numpy as np
import datetime as dt
import requests
import cgi
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
        afsnt_apart.to_csv('./data/tmp/afsnt_'+ARP+'.csv', index = False)

    print(' >>> Concatenating data')
    afsnt_ARP = pd.DataFrame(columns=afsnt_apart.columns)
    for i in range(15):
        afsnt_ARP_i = pd.read_csv('./data/tmp/afsnt_ARP'+str(i+1)+'.csv', encoding = 'utf-8')
        afsnt_ARP = pd.concat([afsnt_ARP, afsnt_ARP_i]).reset_index(drop=True)

    print(' >>> Writing the data')
    afsnt_ARP.to_csv(output_name, index = False)
    print(' >>> finished!')



def load_weather_data(output_name):
    ICAO_code = ['RKSS', 'RKPK', 'RKPC', 'RKTN', 'RKJJ', 'RKJB', 'RKTU', 'RKNY', 
                 'RKJY', 'RKPU', 'RKPS', 'RKTH', 'RKJK', 'RKNW', 'RKSI']

    yyyymm_list = []
    for y in ['2017', '2018', '2019']:
        for i in range(12):
            yyyymm_list.append(y+str(i+1).zfill(2))


    weather = pd.DataFrame(columns=['TYPE', 'TM', 'WD', 'WSPD', 'WS_GST', 'VIS', 'RVR1', 'RVR2', 'RVR3', 'RVR4','WC', 'TMP', 
                                    'TD', 'PS', 'PA', 'RN', 'HM', 'CA_TOT', 'CLA_1LYR', 'BASE_1LYR', 'CLF_1LYR', 
                                    'CLA_2LYR', 'BASE_2LYR', 'CLF_2LYR', 'CLA_3LYR', 'BASE_3LYR', 'CLF_3LYR', 'CLA_4LYR', 
                                    'BASE_4LYR', 'CLF_4LYR'])
    for idx, ICAO in enumerate(ICAO_code):
        print(' >>> Load data : {} ({}/15)'.format(ICAO, idx+1))
        for yyyymm in tqdm.tqdm(yyyymm_list[:-6], mininterval=1):
            url = 'http://amoapi.kma.go.kr/amoApi/air_stcs?icao='+ICAO+'&yyyymm='+yyyymm
            res = requests.get(url, stream = True)
            if 'Content-Disposition' in res.headers:
                content_disposition = res.headers.get('Content-Disposition')
                filename = requests.utils.unquote(cgi.parse_header(content_disposition)[1]['filename'])
                with open('./data/weather/'+filename, 'wb') as f:
                    for chunk in res.iter_content(chunk_size=1024):
                        f.write(chunk)
                weather_i = pd.read_csv('./data/weather/'+filename)
                weather_i.loc[:, 'TYPE'] = ICAO
                weather = pd.concat([weather, weather_i], sort=False).reset_index(drop=True)

    print(' >>> Writing the data')
    weather.to_csv(output_name, index = False)
    print(' >>> Finished!')



def merge_weather_data(weather_input, afsnt_input, output_name):
    print(' >>> Load data')
    weather = pd.read_csv(weather_input, encoding = 'utf-8')
    afsnt = pd.read_csv(afsnt_input, encoding = 'utf-8')

    datetime = [dt.datetime.strptime(str(i)[:-2], "%Y%m%d") for i in weather.TM]
    hours = [dt.timedelta(hours = i%100) for i in weather.TM]
    weather.TM = [d+h for d, h in zip(datetime, hours)]
    weather_dev = weather.drop(['WD', 'WS_GST', 'RVR1', 'RVR2', 'RVR3', 'RVR4', 'TD', 'PS', 'RN', 'HM',
                                'CA_TOT', 'CLA_1LYR', 'BASE_1LYR', 'CLF_1LYR', 'CLA_2LYR', 'BASE_2LYR', 'CLF_2LYR', 
                                'CLA_3LYR', 'BASE_3LYR', 'CLF_3LYR', 'CLA_4LYR', 'BASE_4LYR', 'CLF_4LYR'], 
                                axis = 1)
    print(' >>> Data processing')
    afsnt.STT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.STT]
    afsnt.loc[:, 'TM'] = [i - dt.timedelta(minutes = i.minute) for i in afsnt.STT]

    ICAO = weather_dev.groupby('TYPE').size().keys()

    print(' >>> Merge the data')
    arp_dict2 = {'RKSS':'ARP1', 'RKPK':'ARP2', 'RKPC':'ARP3', 'RKTN':'ARP4', 'RKJJ':'ARP5', 'RKJB':'ARP6', 'RKTU':'ARP7', 'RKNY':'ARP8',
                 'RKJY':'ARP9', 'RKPU':'ARP10', 'RKPS':'ARP11', 'RKTH':'ARP12', 'RKJK':'ARP13', 'RKNW':'ARP14', 'RKSI':'ARP15'}

    afsnt_dev = pd.DataFrame(columns=['ARP', 'ODP', 'FLO', 'FLT', 'REG', 'AOD', 'IRR', 'STT', 'ATT', 'DLY',
                                      'DRR', 'CNL', 'CNR', 'DATE', 'STT_TIME', 'ATT_TIME', 'NUM_FLT', 'TM',
                                      'TYPE', 'WSPD', 'VIS', 'WC', 'TMP', 'PA'])
    for icao in ICAO:
        _afsnt = pd.merge(afsnt.loc[afsnt.ARP==arp_dict2[icao], :], weather_dev.loc[weather_dev.TYPE==icao, :])
        afsnt_dev = pd.concat([afsnt_dev, _afsnt])

    for idx in set(afsnt.ARP) - set([arp_dict2[i] for i in ICAO]):
        afsnt_dev = pd.concat([afsnt_dev, afsnt.loc[afsnt.ARP==idx, :]], sort = False)

    afsnt_dev = afsnt_dev.drop(['TM', 'TYPE', 'WC'], axis = 1)
    print(' >>> Writing the data')
    afsnt_dev.to_csv(output_name, index = False)



def data_processing(input_name, output_dir):
    '''
    # ARP 는 카테고리화 : [ARP1, ARP2, ARP3, ARP15, 나머지]
    # FLO도 카테고리화 : [A, B, F, H, I, J, L, 나머지]
    # AOD -> binary [A:1, D:0]
    # IRR -> binary [Y:1, N:0]
    # STT 카티고리화 : [0~4, 5, 6~12, 13~18, 19~23]
    # ODP, FLT, REG, STT_TIME, ATT_TIME, DATE 제거
    # 결항데이터 제거
      - CNL=='N'인 데이터만
      - CNL, CNR 제거
    '''
    print(' >>> Load data')
    afsnt = pd.read_csv(input_name, encoding = 'utf-8')

    afsnt.STT = [dt.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in afsnt.STT]


    ARP_cat = np.array([int(ARP.replace('ARP', '')) for ARP in afsnt.ARP])
    ARP_cat[(ARP_cat<15)&(ARP_cat>3)] = 5
    ARP_cat[ARP_cat==15] = 4
    ARP_onehot = np.eye(6)[ARP_cat].astype(int)
    afsnt.loc[:, 'ARP1'] = ARP_onehot[:, 1]
    afsnt.loc[:, 'ARP2'] = ARP_onehot[:, 2]
    afsnt.loc[:, 'ARP3'] = ARP_onehot[:, 3]
    afsnt.loc[:, 'ARP15'] = ARP_onehot[:, 4]
    afsnt.loc[:, 'ARP_'] = ARP_onehot[:, 5]

    FLO = np.array([ord(i) for i in afsnt.FLO])
    FLO[FLO==65] = 1
    FLO[FLO==66] = 2
    FLO[FLO==70] = 3
    FLO[FLO==72] = 4
    FLO[FLO==73] = 5
    FLO[FLO==74] = 6
    FLO[FLO==76] = 7
    FLO[FLO > 65] = 8
    FLT_onehot = np.eye(9)[FLO].astype(int)
    afsnt.loc[:, 'FLT_A'] = FLT_onehot[:, 1]
    afsnt.loc[:, 'FLT_B'] = FLT_onehot[:, 2]
    afsnt.loc[:, 'FLT_F'] = FLT_onehot[:, 3]
    afsnt.loc[:, 'FLT_H'] = FLT_onehot[:, 4]
    afsnt.loc[:, 'FLT_I'] = FLT_onehot[:, 5]
    afsnt.loc[:, 'FLT_J'] = FLT_onehot[:, 6]
    afsnt.loc[:, 'FLT_L'] = FLT_onehot[:, 7]
    afsnt.loc[:, 'FLT_'] = FLT_onehot[:, 8]

    afsnt.loc[:, 'AOD'] = (afsnt.AOD=='A').astype(int)
    afsnt.loc[:, 'IRR'] = (afsnt.IRR=='Y').astype(int)

    afsnt.loc[:, 'STT_hour'] = np.array([i.hour for i in afsnt.STT])
    # STT[STT<5] = 0
    # STT[STT==5] = 1
    # STT[(5<STT)&(STT<=12)] = 2
    # STT[(12<STT)&(STT<=18)] = 3
    # STT[18<STT] = 4
    # HOUR_onehot = np.eye(5)[STT].astype(int)
    # afsnt.loc[:, 'HOUR0'] = HOUR_onehot[:, 0]
    # afsnt.loc[:, 'HOUR1'] = HOUR_onehot[:, 1]
    # afsnt.loc[:, 'HOUR2'] = HOUR_onehot[:, 2]
    # afsnt.loc[:, 'HOUR3'] = HOUR_onehot[:, 3]
    # afsnt.loc[:, 'HOUR4'] = HOUR_onehot[:, 4]

    afsnt_train = afsnt.loc[afsnt.CNL=='N', :]
    afsnt_train = afsnt_train.drop(['ARP', 'ODP', 'FLO', 'FLT', 'REG', 'STT', 'ATT', 'DRR', 'CNL', 'CNR', 'DATE', 'STT_TIME', 'ATT_TIME'], axis=1)
    train = afsnt_train.loc[afsnt.STT < dt.datetime(2019, 6, 15), :].reset_index(drop=True)
    validation = afsnt_train.loc[afsnt.STT > dt.datetime(2019, 6, 15), :].reset_index(drop=True)

    print(' >>> Writing the train data')
    train.to_csv(output_dir+'train.csv', index=False)
    print(' >>> Writing the validation data')
    validation.to_csv(output_dir+'validation.csv', index=False)



def standardization(data):
    mean = np.mean(data)
    sd = np.std(data)
    return (data - mean)/sd



def to_numpy(data):
    # data.loc[:, 'NUM_FLT'] = standardization(data.NUM_FLT)
    
    Y = data.loc[:, 'DLY']
    Y = Y.values.reshape(-1, 1)
    Y = (Y=='Y').astype(int)
    X = data.drop('DLY', axis=1).values
    
    return X, Y



if __name__ == '__main__':
    fire.Fire({'calculate_STT_time':calculate_STT_time, 
               'calculate_ATT_time':calculate_ATT_time, 
               'count_num_flt':count_num_flt, 
               'load_weather_data':load_weather_data, 
               'merge_weather_data':merge_weather_data, 
               'data_processing':data_processing})
