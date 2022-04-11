from ctypes import Union
import numpy as np

class a():
    a_ = 1
class b():
    a_ = 2
class c():
    a_ = 3
def func(cls:Union[a, b]):
    return cls.a_
a_ = a()
b_ = b()
c_ = c()
func(c)
print(func(a_))
print(func(b_))
