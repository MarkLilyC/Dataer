


from types import FunctionType

def decor(func:FunctionType):
    print('get in the decorator')
    print('return the pass in function:' + func.__name__)
    return func
    
def func():
    print('test_called_function is being called')
print('func at '+ str(func))
func = decor(func) 
func()
print('func at ' + str(func))
