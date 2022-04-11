from typing import Type
import pandas as pd
import numpy as np
import os
import sys
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats

#   解决相对路径的问题
os.chdir(sys.path[0])

class Slice():
    
    @staticmethod
    def IQRDelOutliers(list_:list, range_ = [0.25,0.75]):
        df_ = pd.DataFrame(list_)
        Q1_ = df_.quantile(range_[0])
        Q3_ = df_.quantile(range_[1])
        IQR_ = Q3_ - Q1_
        return list(df_[~((df_ < (Q1_ - 1.5*IQR_))|(df_>(Q3_ + 1.5*IQR_))).any(axis=1)])

    def __init__(self, key_:any, value_:list, describe_ = '', correct_ = False) -> None:
        self.__key = key_
        if correct_: self.__value = Slice.IQRDelOutliers(value_)
        else: self.__value = value_
        value_ = np.array(value_)
        self.__describe = {
            'min':value_.min(),
            'max':value_.max(),
            'mean':value_.mean(),
            'std':value_.std(),
            'var':value_.var()
        }
    #   key管理方法，暂时不需要删除key
    @property
    def key(self):
        return self.__key
    @key.setter
    def SetKey(self, key_):
        self.__key = key_
    #   value管理，暂时只需要返回value与修改value
    @property
    def value(self):
        return self.__value
    @value.setter
    def SetValue(self, value_):
        self.__value = value_
        #   每次修改完value后都应该修改describe
        value_ = np.array(value_)
        self.__describe = {
            'min':value_.min(),
            'max':value_.max(),
            'mean':value_.mean(),
            'std':value_.std(),
            'var':value_.var()
        }
    #   describe管理，不提供方法修改describe
    @property
    def describe(self):
        return self.__describe
    #   用于将matx对象中存储的slice对象地址dereference为具体的slice值，默认以dict形式返回
    @property
    def DeReference(self, mode = dict):
        if mode == dict:
            return {
                'key':self.key, 
                'value':self.value, 
                'describe':self.describe
            }
        return [self.key, self.value, self.describe]
    

def SliceTTest(slcie1_:Slice, slice2_:Slice):
    log('T Test')
    value1_ = slcie1_.value
    value2_ = slice2_.value
    w, p = stats.levene(args=[value1_, value2_])
    log('Slice-' + str(slcie1_.key) + ': mean-' + str(np.array(value1_).mean()) + ',std-' + str(np.array(value1_).std()))
    log('Slice-' + str(slice2_.key) + ': mean-' + str(np.array(value2_).mean()) + ',std-' + str(np.array(value2_).std()))

    
if __name__ == '__main__':
    s1 = Slice('starttime', [1,2,3,4,13,1,1,1,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,], correct_=True)
    s2 = Slice('starttime', [1,2,3,4,13,1,1,1,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,], correct_=True)
    SliceTTest(slcie1_=s1, slice2_=s2)
    