def count_num_flt(output_name):
    for i in range(15, 0, -1):
        ARP = 'ARP'+str(i)
        afsnt_apart = afsnt.loc[afsnt.ARP==ARP, :].reset_index(drop=True)
        afsnt_apart.loc[:, 'NUM_FLT'] = 0
        STT = afsnt_apart.STT
        print(afsnt_apart.shape[0])
        afsnt_apart.NUM_FLT = [sum((time - dt.timedelta(minutes=30) < STT) & (STT < time + dt.timedelta(minutes=30))) 
                               for time in afsnt_apart.STT]
        afsnt_apart.to_csv('./data/'+ARP+'.csv', index = False)

    ARP = pd.read_csv('./data/ARP1.csv', encoding = 'utf-8')
    for i in range(2, 16):
        ARP_i = pd.read_csv('./data/ARP'+str(i)+'.csv', encoding = 'utf-8')
        ARP = pd.concat([ARP, ARP_i]).reset_index(drop=True)
    ARP.to_csv(output_name, index = False)