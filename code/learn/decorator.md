# `decorator`

## `python`函数也是对象

假设有以下代码：

```python
from types import FunctionType

def decor(func):
    print('get in the decorator')
    print('return the pass in function:' + func.__name__)
    return func
    
def func():
    print('test_called_function is being called')

out_func = decor(func) 
out_func()
```

```bash
get in the decorator
return the pass in function:func
test_called_function is being called
```

先定义了一个`decor`装饰函数

* 该装饰函数接受另外一个函数对象（`FunctionType`）`func`
* 在该装饰函数内部有一些该函数自己需要执行的代码（如此时的一系列`print`）
* 最终该装饰函数将其接收的函数对象`func`返回

接下来定义了一个`func`函数

* 其内部有一些`func`函数自己需要执行的代码，如此时的`print`

紧接着，将`func`函数作为参数传入`decor`函数

* 将返回值赋值为`out_func`，表示这是由`decor`函数处理后得到的函数

根据对`decor`函数的分析，知道其返回值就是传入的`func`函数

* 因此可以知道`out_func`函数其内在就是传入的`func`函数本身

通过添加以下代码，可以更加明确看出`func`与`out_func`二者为同一对象：

```python
print(out_func.__name__)
print(func)
print(out_func)
```

```bash
func
<function func at 0x000002145ED98048>
<function func at 0x000002145ED98048>
```

* `print(out_func.__name__)`打印的`out_func`这个对象的实际`__name__`就是`func`这个函数对象

* 打印`func`与`out_func`两个对象，可见他们都是`function`对象，名为`func`，内存地址也一致

**这个例子充分表明，函数在`python`中也是以对象的形式存在着**

* 函数可以当作参数和返回值被传递、赋值

以上代码做出以下修改：

```python
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
```

```bash
func at <function func at 0x0000025783448048>
get in the decorator
return the pass in function:func
test_called_function is being called
func at <function func at 0x0000025783448048>
```

通过代码`func = decor(func)`，将`decor`的返回值继续命名（赋值给）`func`

这样看起来我们覆盖了原`func`对象的值，但基于以上分析可以知道`func`依然是原来的`func`

* 只不过在其外部通过`decor`函数新加了一些代码
* 并且前后两个`func`的地址也是一致的

这样，通过将`func`作为参数传入、作为参数被赋值，完成了对一个函数的初级’改造’



