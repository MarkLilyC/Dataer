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

def dump_yml(path_:str, content_:dict) -> None:
    '''将数据写入yaml文件中

    Args:
        path_ (str): 写入的文件路径
        content_ (dict): _description_
    '''
    if os.path.exists(path=path_):
        log('File Already Exists, Recommand Not to Overwrite', 0)
    else:
        with open(path_, 'w', encoding='utf-8') as f:
            yaml.dump(content_, f)

def expand(length_:int, item_) -> list:
    '''将item元素扩写为一个指定长度的list 主要用于生成数据分析时需要的index数据列

    Args:
        length_ (int): 需要扩写到的长度
        item_ (_type_): 需要扩写的元素

    Returns:
        list: 扩写完成的list
    '''
    if length_ <= 0:
        log('Length Must be a Positive Integer', 0)
        return None
    else:
        res_ = []
        for i in range(length_):
            res_.append(item_)
        return res_

def judge_lr(positions_:list, casemode_ = 0) -> dict:
    '''输入一个坐标数组(x,y)判断其中每组坐标位于中轴线的左侧还是右侧

    Args:
        positions_ (list): 输入的坐标数据:[[x,y],[x,y]..[x,y]],每组坐标为(x,y)
        casemode_ (int, optional): 最终返回的dict中的keys. Defaults to 0.

    Returns:
        dict: 最终返回的坐标左右判断结果
    '''
    count_of_left_ = 0
    for i in positions_:
        if len(i) == 2:
            if i[0] < 0:
                count_of_left_ += 1
        else:
            log('Wrong Position Data:' + str(i), 0)
            return None
    if casemode_ == 1:
        return {'Unknown':count_of_left_, 'Known': len(positions_) - count_of_left_}
    elif casemode_ == 2:
        return {'Known':count_of_left_, 'Unknown': len(positions_) - count_of_left_}
    else:
        return {'Left':count_of_left_, 'Right': len(positions_) - count_of_left_}

def cut_str_list_2_num_list(str_:str, cut_flag_ = ',') -> list: 
        '''将以str形式呈现的列表切割并转换为float形式返回

        Args:
            str_ (str): 以字符串形式呈现的列表：'[1,2,3,4,5,6,7]'
            cut_flag_ (str): 列表内元素分割的标志

        Raises:
            TypeError: 有无法转换类型的元素

        Returns:
            list: 以列表形式返回的列表 元素类型为float [1.f,2.f...7.f]
            None, : 字符串切割后生成列表失败
        '''
        str_ = str_.replace('[', '')
        str_ = str_.replace(' ', '')
        str_ = str_.replace(']', '')
        list_ = str_.split(',')
        if len(list_) == 0: #   当除去列表边界元素后,split该str的结果为空列表
            log('Empty List',2)
            return []
        else:
            try:list_1 = list(map(float, list_))
            except:
                return None, list_
                '''
                print(list_)
                raise TypeError('invaild value in the str_')
                '''
            else:return list_1

def IQR_Outliers(list_:list, range_ = [0.25,0.75]) -> list:
    '''对传入的列表做IQR异常值处理

    Args:
        list_ (list): 传入的列表
        range_ (list, optional): 异常值上下threshold. Defaults to [0.25,0.75].

    Returns:
        list: 异常值处理后的数组
    '''
    df_ = pd.DataFrame(list_)
    Q1_ = df_.quantile(range_[0])
    Q3_ = df_.quantile(range_[1])
    IQR_ = Q3_ - Q1_
    return list(df_[~((df_ < (Q1_ - 1.5*IQR_))|(df_>(Q3_ + 1.5*IQR_))).any(axis=1)])

def get_first_nan(list_:list):
    '''在提供的list中找出第一个nan值的index
    * 适用于list中存在的nan列为整块 如[1,1,1,1,nan,nan,nan,nan,nan]
    * 主要用于获取给定时间序列中的最大疏散时间
        * 主要用于找出给定时间列表中的第一个nan值index 第一个nan值的前一个数据即为最后一个有效时间数据
    * 判断依据: nan != nan
    Args:
        list_ (list): 给定的数据list

    Returns:
        float: 给定数据list中的第一个nan值的index
        None: 给定数据中不存在nan值
    '''
    half_l_ = int(len(list_)/2)
    if list_[half_l_] != list_[half_l_]:
        list_ = list_[0:half_l_+1]
        for i in range(len(list_)):
            if list_[i] != list_[i]:
                return i
    else:
        list_ = list_[half_l_::]
        for i in range(len(list_)):
            if list_[i] != list_[i]:
                return i + half_l_
    return None

def get_starttime(list_:list, item_ = 0):
    '''获取给定list中的元素开始变化的index
    * 适用于list中开头元素为长段的定值 如[0,0,0,1,2,3,4]
    * 主要用于获取给定坐标㤡中坐标开始变化的行
        * 该行主要用于获取对应时间序列中同一位置的时间值
        * 即获取开始运动的时间
    Args:
        list_ (list): 输入待检索的数据list

    Returns:
        index(float): 给定元素第一次出现的index
    '''

    if len(list_) == 0:
        log('Input List is Empty', 0)
        return None
    else:
        for i in range(len(list_)):
            if list_[i] != item_:
                return i

def FixData(origin_data:pd.DataFrame, correct_columns: int, *axis):
    '''fix the given data in case this data has empty columns or descirpion information at the header

    Args:
        origin_data (pd.DataFrame): the origin data readed from the xlsx
        correct_columns (int): the correctly number of columns

    Returns:
        fix_info (dict): a dict contains the fix information, and this would be used as origin the yml input
    '''
    fix_info = {}
    rows, columns = origin_data.shape
    print(origin_data.index)
    reindex = 1
    # row correct
    if origin_data.iloc[0][0] != 0.1: # 如果第一行一个元素不是数字0.1，则进行校正
            origin_data = origin_data.drop([0]) # 删除第一行
            fix_info['Row Correct'] = 'True' # 将是否校正第一行添加到valu
            reindex = 0
    if columns == correct_columns:
        pass
    else:
        origin_data = origin_data.dropna(axis=1, how='all')
        fix_info['Column Correct'] = 'True' # 将是否校正第一行添加到valu
    print(origin_data.index)
    return origin_data, fix_info, reindex


class SliceDoc():
    '''SliceDoc类
    * 是基本数据类型
    * 用于存储说明性质的数据
    * 不具有计算功能
    '''
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
    '''SliceCal类
    * 是基本类型
    * 用于存储具体的数值型数据
    * 提供计算方法
    '''
    def __init__(self, key_:any, value_:list, describe_ = '', correct_ = False) -> None:
        '''SliceCal类构造函数

        Args:
            key_ (any): 当前slicecal对象所描述的数据名称,最好为str
            value_ (list): 当前slicecal对象所存储的具体的数据
            describe_ (str, optional): 使用者对当前数据的描述. Defaults to ''.
            correct_ (bool, optional): 是否对数据进行IQR异常值处理,当数据值较少时不建议使用. Defaults to False.
        '''
        self.__key = key_
        if correct_:    self.__value = IQR_Outliers(value_)
        else:           self.__value = value_
        value_ = np.array(value_)
        self.__describe = {
            'min':value_.min(),
            'max':value_.max(),
            'mean':value_.mean(),
            'std':value_.std(),
            'var':value_.var()
        }
        del value_
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
        del value_
    #   describe管理，不提供方法修改describe
    @property
    def describe(self):
        return self.__describe
    #   用于将matx对象中存储的slice对象地址dereference为具体的slice值，默认以dict形式返回
    @property
    def de_reference(self, mode = dict):
        '''用于将matx对象中存储的slice对象引用(地址)dereference为具体的slice值,默认以dict形式返回

        Args:
            mode (typr, optional): 返回值的类型:dict or list. Defaults to dict.

        Returns:
            _type_: 返回当前slice对象中的key value describe值
        '''
        if mode == dict:
            return {
                'key':self.key, 
                'value':self.value, 
                'describe':self.describe
            }
        return [self.key, self.value, self.describe]

class Matx():
    #   只接受此构造函数
    def __init__(self, index_:any, data_:dict):
        '''Matx的构造函数

        Args:
            index_ (any): 本matx对象的index,一般为该组数据的工况号,如'第x组试验'或'x'(x:int)
            data_ (dict): 本matx对象的具体数据,其内部的键值对用于生成matx内部存储的__slices
        '''
        self.__slices = {}  #   用于存储slices对象
        self.__type_of_key = None   #   存储slices对象key的类型
        for key,value in data_.items(): #   迭代传入的dict
            #   如果value为单纯数字，则代表此slice为最简单的描述性数字，直接基于此添加一个slicedoc对象即可
            if type(value) == int or type(value) == float:
                self.__slices[key] = SliceDoc(key, value)
            #   如果value为str，则代表此slice可能是描述性语句(docstring), 也可能是str形式存储的list
            elif type(value) == str:
                if key == 'docstring':  #   此value的key为docstring,则直接创建一个slicedoc对象
                    self.__slices[key] = SliceDoc(key, value)
                else:   #   此value为正常数字型数据
                    value_ = cut_str_list_2_num_list(value)
                    if value_:  #   当字符串切割并生成列表失败,则直接退出程序
                        self.__slices[key] = SliceDoc(key, value_)
                    else:   #   字符串切割并生成列表成功
                        log('Failed to Cut Str:' + str(index_) + str(key), 0)
            #   如果value为dict，则代表此slice其实是matx对象，直接添加一个matx对象到slice中即可
            elif type(value) == dict:
                self.__slices[key] = Matx(key, value)
        self.__key = list(data_.keys())
        self.__type_of_key = type(self.__key[0])
        self.__value = list(data_.values())
        self.__index = index_
    @property
    def index(self):
        return self.__index
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
    #   原始初始化函数，传入字典
    def __init__(self, data_:dict, docstring_ = 'original data from given Dict data') -> Type[dict]:
        self.__index = list(data_.keys())
        self.__matxes = {}
        self.__type_of_key = type(self.__index[0])
        self.__values = list(data_.values())
        self.__docstring = docstring_
        for key, value in data_.items():
            if type(value) is not dict:
                if key != 'docstring':
                    raise TypeError('Wrong data')
            else:
                self.__matxes[key] = Matx(key, value)
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
    def index(self):
        return self.__index
    
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
                try:    self.__index.index(key_convert_)#   尝试定位
                except: return False, key_#   并未找到，返回false,错误的输入key
                else:   return True, key_convert_#  找到，返回true,keys中准确的key
        else:
            try:    self.__index.index(key_)#   尝试定位
            except: return False, key_#   并未找到，返回false
            else:   return True, key_#  找到，返回true

    def check_keys(self, keys_:list):
        '''传入一个matx的index列表 检查其中的index是否存在

        Args:
            keys_ (list): 待查询的index列表

        Returns:
            true, cor_index: 所有index都存在时 返回true以及矫正后的index列表
            false, wrong_index: 有一个index不存在便会false 以及所有不存在的index列表 
        '''
        #   如果输入的list为空，则警告，返回None
        if len(keys_) == 0:
            log('Should Not Input Empty', 0)
            return None, []
        else:
            overall_flag_ = True    #   总的check结果，全部存在则为true，其余情况为false
            wrong_keys_ = []    #   错误的keylist
            cor_keys_ = []   #   findkey修正的keylist'
            for i in keys_:
                flag_, key_ = self.find_key(i)  #   查找输入 keylist中的key
                if flag_ :  #   key存在
                    cor_keys_.append(key_)   #   cor_keys_
                else:   #   key不存在
                    overall_flag_ = False  #   标记存在一个不存在的key
                    wrong_keys_.append(i)
            if overall_flag_:   return True, cor_keys_
            else:               return False, wrong_keys_
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
            if key not in self.__index:
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
                index_of_matxs = self.__index
                log('Iterate All Matxs in the Data',  2)
            #   1 检查indexofmatxs内的index类型是否匹配
            flag_, cor_keys = self.check_keys((index_of_matxs))
            #   如果查找结果为True，则代表输入的key全部存在
            if flag_:  
                log('Input Matx Indexes all exist', 1)
            else:       
                log('Indexes::' + str(cor_keys) + 'dont exist', 0)
                quit()
            #   2 递归找出item中指向的slice
            res_ = {}   #   以字典的形式存储所找到的slice，其key为matx_key-items
            print('cor_key_: ' + str(cor_keys))
            res_keys_ = ''
            for i in items[0:-1]:
                res_keys_ += i + '-'
            res_keys_ += items[-1]
            for i in cor_keys:
                tmp_res_ = self.matxes[i]   #   获取到每一个matx
                for j in items[0:-1]:   #   对item（即具体需要获取的数据的keys）遍历  
                    tmp_res_ = tmp_res_.slices[j]   #   仅拿出silice       
                res_[i] = tmp_res_.slices[items[-1]].value #   具体的值在最后拿出
            res_['docstring'] = res_keys_
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
    '''data = Dataer.load_yml('./results.yml')
    a = data.get_specific_slices([1,10], 'endpos')
    print(data.matxes)'''
    print(get_first_nan([1,2,3,3,4,5,6,7]))
