import copy
from operator import index, indexOf
import os
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from scipy import stats
from typing import Type
import numpy as np
import pandas as pd
import yaml
import os, sys
LOGCOLOR = {
    0:'\033[0;30;41m',
    1:'\033[0;30;42m',
    2:'\033[0;30;43m'
}
#   解决相对路径的问题
os.chdir(sys.path[0])
#   log函数
def log(str_in_ = None, color = 1):
    '''自定义log函数
    * 输入字符串、数字、列表、字典等元素的字符长度不超过49
    '''
    if str_in_ is None:
        print(LOGCOLOR[color] + '~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~·~')
    else:
        len_in_ = len(str_in_)
        default_filler = '~·'
        left_filler = ''
        if len_in_ % 2 == 0:#    偶数
            left_len = (48 - len_in_)/2
            if left_len % 2 == 0:
                for i in range(int(left_len / 2)):
                    left_filler += default_filler
                out_ = left_filler + str_in_ + '·' + left_filler
                print(LOGCOLOR[color] + out_ + '\033[0m')
            else:
                for i in range(int((left_len- 1) /2)) :
                    left_filler += default_filler
                out_ = '·' + left_filler +  str_in_ + '·' + left_filler + '~'
                print(LOGCOLOR[color] + out_ + '\033[0m')
        else:
            left_len = (49 - len_in_)/2
            if left_len % 2 == 0:
                for i in range(int((left_len-1) / 2)):
                    left_filler += default_filler
                out_ = left_filler + default_filler + str_in_ + '·' + left_filler + '~'
                print(LOGCOLOR[color] + out_ + '\033[0m')
            else:
                for i in range(int((left_len- 1) /2)) :
                    left_filler += default_filler
                out_ = '·' + left_filler +  str_in_ + '·' + left_filler
                print(LOGCOLOR[color] + out_ + '\033[0m')

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

def cut_str_list_2_num_list(str_:str, cut_flag_ = ',') -> Type[list]: 
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
        try:list_1 = list(map(float, list_))
        except:
            return None
            '''print(list_)
            raise TypeError('invaild value in the str_')
'''
        else:return list_1

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
    __slices = {}
    __type_of_key = None
    #   只接受此构造函数
    def __init__(self, index_:any, data_:dict) -> dict:
        for key,value in data_.items():
            #   如果value为单纯数字，则代表此slice为最简单的描述性数字，直接基于此添加一个slice对象即可
            if type(value) == int or type(value) == float:
                self.__slices[key] = copy.deepcopy(SliceDoc(key, value))
            #   如果value为str，则代表此slice可能为描述性说明数据，更大可能是以str存储的list
            elif type(value) == str:
                if key == 'docstring':# 如果这个key是docstring，便不执行cutstr2list，直接创建一个slicedoc对象
                    self.__slices[key] = SliceDoc(key, value)
                else:
                    value_ = cut_str_list_2_num_list(value)
                    if value_ is None:
                        self.__slices[key] = SliceDoc(key, value_)
                    else:
                        self.__slices[key] = SliceDoc(key, value_)
            #   如果value为dict，则代表此slice其实是matx对象，直接添加一个matx对象到slice中即可
            elif type(value) == dict:
                self.__slices[key] = copy.deepcopy(Matx(key, value))
        self.__key = list(data_.keys())
        self.__type_of_key = type(self.__key[0])
        self.__value = list(data_.values())
        self.__index = index_
        self.__data = data_
    @property
    def index(self):
        return self.__index
    @property
    def data(self):
        return self.__data
    @property
    def key(self):
        return self.__key
    @property
    def value(self):
        return self.__value
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
    __keys = []
    __values = []
    __docstring = ''
    __type_of_key = None
    __matxes = {}
    #   原始初始化函数，传入字典
    def __init__(self, data_:dict, docstring_ = 'original data from given Dict data') -> Type[dict]:
        self.__keys = list(data_.keys())
        self.__type_of_key = type(self.__keys[0])
        self.__values = list(data_.values())
        self.__docstring = docstring_
        for key, value in data_.items():
            if type(value) is not dict:
                if key != 'docstring':
                    raise TypeError('Wrong data')
            else:
                t = Matx(key, value)
                self.__matxes[key] = t #   深拷贝
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
    @property
    def keys(self):
        return self.__keys
    
    def drop_key_value(self, key_:any):
        flag_, key_ = self.find_key(key_)
        if flag_:#    如果目标key存在
            del self.data[key_]
            return True
        else:
            log('Key: ' + str(key_) + 'Doesnt Exist', color=0)
    #   虽然可以将此方法写为一个三个类共用的方法，但为了代码可读性 仍然将其保留在各自
    def find_key(self, key_):
        if type(key_) != self.__type_of_key:#    如果传入key类型与当前keys类型不一致
            try:#   尝试将传入key类型转换为当前keys type
                key_convert_ = self.type_of_key(key_)
            except:#    转换失败
                raise ValueError('Wrong Input Key Type: ' + type(key_) + ', the Correct Type is ' + str(self.type_of_key))
            else:  #    转换成功
                log(str('Should Use Right Key Type: ' + str(self.type_of_key)), color=2)
                try:    self.keys.index(key_convert_)#   尝试定位
                except: return False, None#   并未找到，返回false,none
                else:   return True, key_convert_#  找到，返回true,keys中准确的key
        else:
            try: self.keys.index(key_)#   尝试定位
            except: return False, None#   并未找到，返回false
            else: return True, key_#  找到，返回true

    def check_keys(self, keys_:list):
        #   如果输入的list为空，则警告，返回None
        if len(keys_) == 0:
            log('Should Not Input Empty', 0)
            return None, []
        else:
            overall_flag_ = True    #   总的check结果，全部存在则为true，其余情况为false
            wrong_keys_ = []    #   错误的keylist
            cor_keys = []   #   findkey修正的keylist'
            for i in keys_:
                flag_, key_ = self.find_key(i)  #   查找输入 keylist中的key
                cor_keys.append(key_)
                if flag_ :pass
                else:
                    overall_flag_ == False
                    wrong_keys_.append([i, key_])
            if overall_flag_:return overall_flag_, cor_keys
            else:return overall_flag_, wrong_keys_
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

    def get_specific_slices(self, index_of_matxs = None, *items):
        log('Get Specific Slices')
        if len(items) == 0:
            log('Should Input Specific Items to Load', 0)
            return None
        else:
            #   如果不指定具体的indexofmatx，则代表将遍历所有matx
            if index_of_matxs is None:
                index_of_matxs = self.keys
                log('Iterate All Matxs in the Data',  2)
            #   1 检查indexofmatxs内的index类型是否匹配
            flag_, cor_keys = self.check_keys((index_of_matxs))
            #   如果查找结果为True，则代表输入的key全部存在
            if flag_:   log('Input Keys all exist', 1)
            else:       log('Keys:' + str(cor_keys) + 'dont exist', 0)
            #   2 递归找出item中指向的slice
            res_ = {}   #   以字典的形式存储所找到的slice，其key为matx_key-items
            for i in cor_keys:
                res_key_ = str(i) + '-'  #   将index str化
                tmp_res_ = self.matxes[i]   #   获取到每一个matx
                for j in items[0:-1]:   #   对item（即具体需要获取的数据的keys）遍历  
                    tmp_res_ = tmp_res_.slices[j]   #   仅拿出silice
                    res_key_ += str(j) + '-'       
                print(tmp_res_.__class__, tmp_res_.value)
                res_[res_key_ + items[-1]] = tmp_res_.slices[items[-1]].value #   具体的值在最后拿出
            return res_


def slice_t_test(slcie1_:SliceCal, slice2_:SliceCal):
    log('T Test', color=1)
    value1_ = slcie1_.value
    value2_ = slice2_.value
    args_ = [value1_, value2_]
    w, p = stats.levene(*args_)
    log('Slice-' + str(slcie1_.key) + ': mean-' + str(np.array(value1_).mean()) + ',std-' + str(np.array(value1_).std()), color = 1)
    log('Slice-' + str(slice2_.key) + ': mean-' + str(np.array(value2_).mean()) + ',std-' + str(np.array(value2_).std()), color = 1)
    if p >= 0.05:
        log('方差相等')
        print(stats.ttest_ind(value1_,value2_,equal_var=True))
    else:
        log('方差不等')
        print(stats.ttest_ind(value1_,value2_,equal_var=False))



if __name__ == '__main__':
    data = Dataer.load_yml('./results.yml')
    a = data.get_specific_slices(None, 'stdmaxtime', 'left')
    print(a)


#   列表传输，lista = listb 