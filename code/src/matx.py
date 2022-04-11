from typing import Type
import pandas as pd
import numpy as np
import os
import sys
from slice import Slice
#   解决相对路径的问题
os.chdir(sys.path[0])

class Matx():
    __slices = []
    #   只接受此构造函数
    def __init__(self, index_:any, data_:dict) -> dict:
        
        for key,value in data_.items():
            if type(value) != list:
                if key != 'docstring':
                    raise TypeError('invalid input:all the specific data should be list(except docsting)')
            else:
                self.__slices.append(Slice(key, value))
        self.__keys = list(data_.keys())
        self.__values = list(data_.values())
        self.__index = index_
        self.__data = data_
        
    
    @property
    def index(self):
        return self.__index
    @property
    def data(self):
        return self.__data
    @property
    def keys(self):
        return self.__keys
    @property
    def values(self):
        return self.__values
    #   实际存储的时slice对象的地址
    @property
    def slices(self):
        return self.__slices
        #   以下代码将实际的slice对象中的数据添加到matx的slices中替换掉原本的slice对象的引用
        '''slices_ = []
        for i in self.__slices:#    避免死循环所以不适用self.slices
            slices_.append(i.DeReference)
        return slices_'''

    @staticmethod
    def CutStrListIntoNumList(str_:str, cut_flag_:str) -> Type[list]: 
        '''将以str形式呈现的列表切割并转换为float形式返回

        Args:
            str_ (str): 以字符串形式呈现的列表：'[1,2,3,4,5,6,7]'
            cut_flag_ (str): 列表内元素分割的标志

        Raises:
            TypeError: 有无法转换类型的元素

        Returns:
            _type_ (list): 以列表形式返回的列表，元素类型为float：[1.f,2.f...7.f] 
        '''
        str_ = str_.replace('[', '')
        str_ = str_.replace(' ', '')
        str_ = str_.replace(']', '')
        list_ = str_.split(',')
        try:list_ = list(map(float, list_))
        except:raise TypeError('invaild value in the str_')
        else:return list_
    
    @staticmethod
    def Func():
        print('func')
    
m = Matx('test', {
    1:[1,2,3,4],
    2:[1,1,1],
    3:[-1,-1,-1]
})



print(m.slices[0].describe)
