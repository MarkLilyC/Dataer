import numpy as np
from numpy import nan
def get_first_nan(list_:list):
    '''在提供的list中找出第一个nan值的index
    * 主要用于找出
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

l = [1,1,1,nan,nan,nan]
a = get_first_nan(l)
print(a, l[a])