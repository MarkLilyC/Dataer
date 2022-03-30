from re import L


class animal:
    def __init__(self, name:str) -> None:
        print('i am ' + name + ' and i am an animal')

class dog(animal):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        print('i am ' + name + ' and i am an dog')
    
an = animal('an')
dog1 = dog('dog1')