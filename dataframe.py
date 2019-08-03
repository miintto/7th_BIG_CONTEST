import pandas as pd
import datetime as dt
import fire



def count_num_flt(output_name):
    afsnt = pd.read_csv('./data/AFSNT.csv', encoding = 'cp949')

    for i in range(15, 0, -1):
        ARP = 'ARP'+str(i)
        afsnt_apart = afsnt.loc[afsnt.ARP==ARP, :].reset_index(drop=True)
        afsnt_apart.loc[:, 'NUM_FLT'] = 0
        STT = afsnt_apart.STT
        afsnt_apart.NUM_FLT = [sum((time - dt.timedelta(minutes=30) < STT) & (STT < time + dt.timedelta(minutes=30))) 
                               for time in afsnt_apart.STT]
        afsnt_apart.to_csv('./data/afsnt_'+ARP+'.csv', index = False)

    afsnt_ARP = pd.read_csv('./data/afsnt_ARP1.csv', encoding = 'utf-8')
    for i in range(2, 16):
        afsnt_ARP_i = pd.read_csv('./data/afsnt_ARP'+str(i)+'.csv', encoding = 'utf-8')
        afsnt_ARP = pd.concat([afsnt_ARP, afsnt_ARP_i]).reset_index(drop=True)
    afsnt_ARP.to_csv(output_name, index = False)


if __name__ == '__main__':
    fire.Fire({'count_num_flt':count_num_flt})