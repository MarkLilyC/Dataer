import copy

class inner():
    def __init__(self, key:int, value:int) -> None:
        self.__key = key
        self.__value = value
    @property
    def value(self):
        return self.__value

class outter():
    __inners = {}
    def __init__(self, inner_list:dict) -> None:
        for key, value in inner_list.items():
            self.__inners[key] = inner(key, value)
    @property
    def inners(self):
        return self.__inners
    
inner1 = {
    1:12,
    2:13,
    3:14,
}
inner2 = {
    4:22,
    5:24,
    6:25
}
out = [inner1, inner2]
outters = []
for i in out:
    outters.append(outter(i))

print(outters[0].value)
print(outters[1].value)




