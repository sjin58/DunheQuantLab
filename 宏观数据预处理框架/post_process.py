

"""
该函数用于将处理后的函数进行刻画的模块，根据案例统一输入与输出
"""


from ZigZag import peak_valley_pivots
import numpy as np

def ShuiWei(df,N):
    """
    :param df:初始数据，时间序列，只有一列
    :param N: 算法窗口长度
    :return: dataframe，为计算后的数据，也保持一列，columns需要指出算法与算法参数
    """
    temp = df.copy() ##防止浅拷贝，每个函数第一列需要有这个
    def water(x):
        x = x.to_frame()
        x = x.rank()
        return (x.iloc[-1][0] - x.min()[0]) / (x.max() - x.min())[0]

    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x:water(x))
    temp.columns = [str(N)+'水位']  #指出算法参数与算法名称
    return temp

def Tongbi(df,N):

    temp = df.copy()
    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x: x[-1]/x[0])
    temp.columns = [str(N) + '同比']  # 指出算法参数与算法名称
    return temp


def BIAS(df,N):
    """
    :param df: 初始数据，时间序列，只有一列
    :param N: 算法窗口长度
    :return: dataframe，为计算后的数据，也保持一列，columns需要指出算法与算法参数
    """
    temp = df.copy()
    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x: (x[-1]-x.mean())/x.mean())
    temp.columns = [str(N)+'偏离度']
    return temp


def HuanBi(df,N):
    temp = df.copy()
    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x: x[-1]/x[0])
    temp.columns = [str(N)+'环比']
    return temp


def Zscore(df,N):
    temp = df.copy()
    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x: (x[-1]-x.mean())/x.std())
    temp.columns = [str(N) + 'zscore']
    return temp

def Pivot_momentum(df,N):
    temp = df.copy()
    temp.dropna(inplace=True)
    temp['pivot'] = peak_valley_pivots(temp[temp.columns[0]], 0, 0)
    temp['pivot_val'] = temp.apply(lambda x: x[temp.columns[0]] if x['pivot'] != 0 else np.nan, axis=1)
    temp['pivot_val'] = temp['pivot_val'].fillna(method='ffill')
    temp['pivot_val'] = temp['pivot_val'].shift(1)
    temp['短期动量'] = temp[temp.columns[0]] - temp['pivot_val']

    # 以过去一段时间振幅的变化幅度来衡量，不是很路径依赖
    temp['极差'] = temp[temp.columns[0]].rolling(N).apply(lambda x: x.max() - x.min())
    temp['变化占比'] = temp['短期动量'] / temp['极差'] * 100

    temp = temp['变化占比'].to_frame()
    temp = temp.columns[str(N)+'拐点动量']
    return temp

def HuanBi_way(df,N):
    temp = df.copy()
    temp[temp.columns[0]] = temp[temp.columns[0]].rolling(N).apply(lambda x:np.sign(x[-1]-x[0]))
    temp.columns = [str(N)+'环比方向']
    return temp

def cut_val(df,N):
    temp = df.copy()
    pass


def max_min_standardilzation(df):
    pass

