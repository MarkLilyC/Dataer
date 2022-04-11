from operator import index
import os
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats
from typing import Type
import numpy as np
import pandas as pd
import yaml
import os, sys

#   解决相对路径的问题
os.chdir(sys.path[0])
#   log函数
def log(*in_:any):
    '''自定义log函数
    * 输入字符串、数字、列表、字典等元素的字符长度不超过49
    '''
    if len(in_) == 0:
        print('\033[0;31;42m~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~\033[0m')
    else:
        in_ = str(in_[0])
        len_in_ = len(in_)
        default_filler = '~·'
        left_filler = ''
        if len_in_ % 2 == 0:#    偶数
            left_len = (48 - len_in_)/2
            if left_len % 2 == 0:
                for i in range(int(left_len / 2)):
                    left_filler += default_filler
                out_ = left_filler + in_ + '·' + left_filler
                print('\033[0;31;42m' + out_ + '\033[0m')
            else:
                for i in range(int((left_len- 1) /2)) :
                    left_filler += default_filler
                out_ = '·' + left_filler +  in_ + '·' + left_filler + '~'
                print('\033[0;31;42m' + out_ + '\033[0m')
        else:
            left_len = (49 - len_in_)/2
            if left_len % 2 == 0:
                for i in range(int((left_len-1) / 2)):
                    left_filler += default_filler
                out_ = left_filler + default_filler + in_ + '·' + left_filler + '~'
                print('\033[0;31;42m' + out_ + '\033[0m')
            else:
                for i in range(int((left_len- 1) /2)) :
                    left_filler += default_filler
                out_ = '·' + left_filler +  in_ + '·' + left_filler
                print('\033[0;31;42m' + out_ + '\033[0m')

def dump_yml(path_:str, content_:dict):
    with open(path_, 'w', encoding='utf-8') as f:
        yaml.dump(content_, f)

def expand(length_:int, item_):
    res_ = []
    for i in range(length_):
        res_.append(item_)
    return res_

def judge_lr(positions_:list, casemode_ = None):
    count_of_left = 0
    for i in positions_:
        if i[0] < 0:
            count_of_left += 1
    if casemode_ == 1:
        return {'Unknown':count_of_left, 'Known': len(positions_) - count_of_left}
    elif casemode_ == 2:
        return {'Known':count_of_left, 'Unknown': len(positions_) - count_of_left}
    else:
        return {'Left':count_of_left, 'Right': len(positions_) - count_of_left}

def cut_str_list_2_num_list(str_:str, cut_flag_:str) -> Type[list]: 
        '''将以str形式呈现的列表切割并转换为float形式返回

        Args:
            str_ (str): 以字符串形式呈现的列表：'[1,2,3,4,5,6,7]'
            cut_flag_ (str): 列表内元素分割的标志

        Raises:
            TypeError: 有无法转换类型的元素

        Returns:
            _type_ (list): 以列表形式返回的列表 元素类型为float [1.f,2.f...7.f] 
        '''
        str_ = str_.replace('[', '')
        str_ = str_.replace(' ', '')
        str_ = str_.replace(']', '')
        list_ = str_.split(',')
        try:list_ = list(map(float, list_))
        except:raise TypeError('invaild value in the str_')
        else:return list_

def IQR_Outliers(list_:list, range_ = [0.25,0.75]):
        df_ = pd.DataFrame(list_)
        Q1_ = df_.quantile(range_[0])
        Q3_ = df_.quantile(range_[1])
        IQR_ = Q3_ - Q1_
        return list(df_[~((df_ < (Q1_ - 1.5*IQR_))|(df_>(Q3_ + 1.5*IQR_))).any(axis=1)])

class SliceDoc():
    def __init__(self, key_:any, value_:any) -> None:
        self.__key = key_
        self.__value = value_
    @property
    def key(self):
        return self.__key
    @key.setter
    def set_key(self, key_):
        self.__key = key_
    @property
    def value(self):
        return self.__value
    @value.setter
    def set_value(self, value_):
        self.__value = value_

class SliceCal():
    def __init__(self, key_:any, value_:list, describe_ = '', correct_ = False) -> None:
        self.__key = key_
        if correct_: self.__value = IQR_Outliers(value_)
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
    def set_key(self, key_):
        self.__key = key_
    #   value管理，暂时只需要返回value与修改value
    @property
    def value(self):
        return self.__value
    @value.setter
    def set_value(self, value_):
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
    def de_reference(self, mode = dict):
        if mode == dict:
            return {
                'key':self.key, 
                'value':self.value, 
                'describe':self.describe
            }
        return [self.key, self.value, self.describe]


class Matx():
    __slices = []
    __type_of_key = None
    #   只接受此构造函数
    def __init__(self, index_:any, data_:dict) -> dict:
        for key,value in data_.items():
            if type(value) == int or float:
                self.__slices.append(SliceDoc(key, value))
            elif type(value) == str:
                pass
            elif type(value) == dict:
                self.slices.append(Matx(key, value))
        self.__keys = list(data_.keys())
        self.__type_of_key = type(self.__keys[0])
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
    @property
    def type_of_key(self):
        return self.__type_of_key
    #   实际存储的时slice对象的地址
    @property
    def slices(self):
        return self.__slices
        #   以下代码将实际的slice对象中的数据添加到matx的slices中替换掉原本的slice对象的引用
        '''slices_ = []
        for i in self.__slices:#    避免死循环所以不适用self.slices
            slices_.append(i.DeReference)
        return slices_'''



class Dataer:
    __data = {}
    __keys = []
    __values = []
    __docstring = ''
    __type_of_key = None
    __matxes = []
    #   原始初始化函数，传入字典
    def __init__(self, data_:dict, docstring_ = 'original data from given Dict data') -> Type[dict]:
        self.__data = data_#    del
        self.__keys = list(self.__data.keys())
        self.__type_of_key = type(self.__keys[0])
        self.__values = list(self.__data.values())
        self.__docstring = docstring_
        for key, value in data_.items():
            if type(value) is not dict:
                if key != 'docstring':
                    raise TypeError('Wrong data')
            else:
                self.__matxes.append(Matx(key, value))
    #   重构构造函数，通过传入yml数据文件的地址来读取数据
    @classmethod
    def load_yml(cls, filepath:str, docstring_ = 'original data from given YML file'):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data_ = yaml.load(f.read(),Loader=yaml.Loader)
                data = cls(data_, docstring_)
                return data
        else:
            raise FileNotFoundError("File Doesn't exist")
    #   将data property化
    @property
    def data(self):
        return self.__data
    #   将keys property化
    @property
    def keys(self):
        return self.__keys
    
    def drop_key_value(self, key_:any):
        flag_, key_ = self.find_key(key_)
        if flag_:#    如果目标key存在
            del self.data[key_]
            return True
        else:
            log('Key: ' + str(key_) + 'Doesnt Exist')
    #   虽然可以将此方法写为一个三个类共用的方法，但为了代码可读性 仍然将其保留在各自
    def find_key(self, key_):
        if type(key_) != self.__type_of_key:#    如果传入key类型与当前keys类型不一致
            try:#   尝试将传入key类型转换为当前keys type
                key_convert_ = self.type_of_key(key_)
            except:#    转换失败
                raise ValueError('Wrong Input Key Type: ' + type(key_) + ', the Correct Type is ' + str(self.type_of_key))
            else:  #    转换成功
                log('Should Use Right Key Type: ' + str(self.type_of_key))
                try: self.keys.index(key_convert_)#   尝试定位
                except: return False, None#   并未找到，返回false,none
                else: return True, key_convert_#  找到，返回true,keys中准确的key
        else:
            try: self.keys.index(key_)#   尝试定位
            except: return False, None#   并未找到，返回false
            else: return True, key_#  找到，返回true
    def check_keys(self, keys_:list):
        overall_flag_ = None
        wrong_keys_ = []
        for i in keys_:
            flag_, key_ = self.find_key(i)
            if flag_ is False:
                overall_flag_ == False
                wrong_keys_.append([i, key_])
            else:pass
        return overall_flag_, wrong_keys_
    #   将values property化
    @property
    def values(self):
        return self.__values
    @property
    def docstring(self):
        return self.__docstring
    @property
    def type_of_key(self):
        return self.__type_of_key
    @property
    def Drop(self, drop_keys_list:list):
        keyErrorFlag = False
        notFoundKeyList = []
        for key in drop_keys_list:
            if key not in self.__keys:
                notFoundKeyList.append(key)
        if keyErrorFlag:
            raise KeyError('Error Key Found:' + notFoundKeyList+', Not Found in The Dataer Keys')
        else:
            for key in drop_keys_list:
                del self.__data[key]
    @property
    def matxes(self):
        return self.__matxes


def slice_t_test(slcie1_:SliceCal, slice2_:SliceCal):
    log('T Test')
    value1_ = slcie1_.value
    value2_ = slice2_.value
    args_ = [value1_, value2_]
    w, p = stats.levene(*args_)
    log('Slice-' + str(slcie1_.key) + ': mean-' + str(np.array(value1_).mean()) + ',std-' + str(np.array(value1_).std()))
    log('Slice-' + str(slice2_.key) + ': mean-' + str(np.array(value2_).mean()) + ',std-' + str(np.array(value2_).std()))
    if p >= 0.05:
        log('方差相等')
        print(stats.ttest_ind(value1_,value2_,equal_var=True))
    else:
        log('方差不等')
        print(stats.ttest_ind(value1_,value2_,equal_var=False))

def get_data(data_:Dataer, index_:list, *items_):
    f_, k_ = data_.check_keys(index_)
    if f_:
        log('Wrong index in the index list:')
        log(k_)
    else:
        log_content_ = ''
        log_res_ = {}
        for i in index_:
            log_content_  = data_.values[i]
            for j in items_:
                log_content_ = log_content_[j]


if __name__ == '__main__':
    data = Dataer.load_yml('./res.yml')
    print(data.matxes[0].slices[0].value)
