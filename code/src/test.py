import copy
from traceback import print_tb
import numpy as np


class slice():
    def __init__(self, var:list) -> None:
        var_ = np.array(var)
        self.__var = np.mean(var_)
        del var_
    @property
    def var(self):
        return self.__var

a = slice([1,2,3,4,5,6,7])
print(a.var)
b = None
if b:
    print(1)
else:
    print