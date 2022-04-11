class profile():
    @property
    def func_property(self):
        print('call function being decorted by property')
    def func_nonproperty(self):
        print('call function not being decorted by property')
p = profile()
p.func_nonproperty()
p.func_property
