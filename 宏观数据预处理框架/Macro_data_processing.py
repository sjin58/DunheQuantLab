



"""
该脚本用于统一预处理宏观数据
"""
import sys
sys.path.append(r"Z:\宏观数据预处理框架")
from get_data_from_databao import get_data_from_bao
from pre_process import *
from post_process import *




class macro_data_processing:
    def __init__(self,setting_file_path):
        self.setting_file = pd.read_excel(setting_file_path)
        self.setting_list = []


    ## 根据来源和id直接从api获取数据
    def fetch_data(self,id,source):
        if source.upper()=='WIND':
            df = get_data(id,'2010-01-01')  #开始日期默认2010-01-01，可以自行调整

        elif source=='数据宝':
            df = get_data_from_bao(id,'2010-01-01')

        #如果不从api获取，请给出本地文件的地址，以excel形式存储
        else:
            df = pd.read_excel(id)

        return df



    def single_run(self,para):

        #根据来源获得对应的数据
        df = self.fetch_data(id=para['指标id'],source=para['指标来源'])

        #迭代模式，顺序按照书写的方式从左到右
        for key, val in para['预处理函数'].items():
            df = eval(key + f"(df,{val})")


        #根据参数中给定的处理方式与参数，生成与原数据合成的刻画指标
        origin_data = df.copy()
        for key,val in para['长期刻画'].items():
            df = pd.concat([df,eval( key+f"(origin_data,{val})")],axis=1)
        for key, val in para['中期刻画'].items():
            df = pd.concat([df, eval(key + f"(origin_data,{val})")], axis=1)
        for key, val in para['短期刻画'].items():
            df = pd.concat([df, eval(key + f"(origin_data,{val})")], axis=1)
        return df


    def run(self):
        for index, row in self.setting_file.iterrows():
            temp_dict = dict(zip(self.setting_file.columns, row.values))
            temp_dict['预处理函数'] = eval(temp_dict['预处理函数'])
            temp_dict['长期刻画'] = eval(temp_dict['长期刻画'])
            temp_dict['中期刻画'] = eval(temp_dict['中期刻画'])
            temp_dict['短期刻画'] = eval(temp_dict['短期刻画'])
            self.setting_list.append(temp_dict)

        #单线程
        for para in self.setting_list:
            res = self.single_run(para)
            self.to_file(res,para['指标名称'])
        #多线程

    def to_file(self,df,name):
        df.to_excel("Z:/宏观数据预处理框架/test_res/"+name+".xlsx")



if __name__ == '__main__':
    file_path = "Z:/宏观数据预处理框架/宏观预处理参数配置.xlsx"
    Data_pro = macro_data_processing(file_path)
    Data_pro.run()






