

import sys
sys.path.append(r"C:\Wind\Wind.NET.Client\WindNET\x64")
import pandas as pd
from WindPy import w


w.start()

def get_data(id,start_date='2010-01-01'):
    receive = w.edb(id, start_date)
    df = {}
    for i in range(len(receive.Data)):
        df[id] = receive.Data[i]
    df = pd.DataFrame(df, index=receive.Times)
    df = df.reset_index()
    df.columns = ['日期', id]
    df.index = pd.to_datetime(df['日期'])
    del df['日期']

    return df

def get_stock_data(number_list,field,start_date):
    receive = w.wsd(number_list,field, start_date)
    df = {}
    for i in range(len(receive.Data)):
        df[number_list[i]] = receive.Data[i]
    df = pd.DataFrame(df, index=receive.Times)
    df = df.sum(axis=1).to_frame()
    df = df.reset_index()
    df.columns = ['日期', number_list[-1]]
    df.index = pd.to_datetime(df['日期'])
    del df['日期']

    return df


if __name__ == '__main__':


    get_data('M0017142','2010-01-01')



