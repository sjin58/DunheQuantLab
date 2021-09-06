




"""
该模块仅用于书写预处理模块，所有函数根据案例统一输入与输出
"""
import numpy as np
import pandas as pd
from get_data_from_wind import get_data



def MA(df,N):
    df[df.columns[0]] = df[df.columns[0]].rolling(N).mean()
    return df

def pre_Tongbi(df,N):
    df[df.columns[0]] = df[df.columns[0]].rolling(N).apply(lambda x: x[-1] / x[0])
    return df

def pre_Huanbi(df,N):
    df[df.columns[0]] = df[df.columns[0]].rolling(N).apply(lambda x: x[-1] / x[0])
    return df

def cumsum_Tongbi(df,N):
    pass

def current_val(df,N):
    df['差值'] = df[df.columns[0]].diff(1)
    def Month(x):
        if x['差值'] < 0 or np.isnan(x['差值']):
            return x[df.columns[0]]
        else:
            return x['差值']

    df['当月值'] = df.apply(lambda x: Month(x), axis=1)
    name = df.columns[0]
    df = df['当月值'].to_frame()
    df.columns=[name]
    return df

def data_fill(df,N):
    df.fillna(inplace=True,method='ffill')
    return df

def Tradingday_transfer(df,N):
    trading_day = get_data('S0105896','2010-01-01')

    def shift_holiday(df):
        columns = df.columns
        col_0 = columns[0]
        name = columns[1]

        def is_hoilday(x, name):
            if np.isnan(x[col_0]) and not np.isnan(x[name]):
                return 1
            else:
                return 0

        df_0 = df.copy()  # 保留交易日信息
        df = df.reset_index()
        df['is_holiday'] = df.apply(lambda x: is_hoilday(x, name), axis=1)

        date_index = df.columns[0]
        df[date_index] = df.apply(lambda x: np.nan if x['is_holiday'] == 1 else x[date_index], axis=1)
        df[date_index] = df[date_index].fillna(method='ffill')
        df.drop_duplicates(subset=[date_index], keep='last', inplace=True)

        df = df.set_index(date_index)
        res = pd.concat([df_0[col_0].to_frame(), df[name]], axis=1)
        res[name].fillna(inplace=True, method='ffill')
        res.dropna(inplace=True, subset=[col_0])

        return res

    df = pd.concat([trading_day,df],axis=1)
    df = shift_holiday(df)
    df = df.iloc[:,1]
    df = df.to_frame()
    return df


def delay(df,N):
    df[df.columns[0]] = df[df.columns[0]].shift(N)
    return df














