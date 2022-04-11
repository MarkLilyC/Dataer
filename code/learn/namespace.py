
class profile():
    __specie = 'human'
    __name = ''
    __age = 0
    def __init__(self, name = '', age = 0) -> None:
        self.__name = name
        self.__age = age
    @property
    def profile(self):
        return self.__name, self.__age
    @classmethod
    def profile_from_string(cls, profile_string:str):
        name, age = profile_string.split('-')
        instance = cls(name, age)
        return instance
p = profile.profile_from_string('marklily-24')
print(p.profile)


