## 介绍与使用方法

### 01. 协程介绍

[介绍部分原文出处](https://ashooter.github.io/2018-11-19/深入理解Python的asyncio协程/)

#### 1.1 协程

协程（coroutines）是通过`async/await`定义函数或方法，是使用`asyncio`进行异步编程的首选途径。

实际上，`asyncio`提供了三种执行`协程`的机制：

- **使用`asyncio.run()`执行协程。一般用于执行最顶层的入口函数，如`main()`。**
- **`await`一个`协程`。一般用于在一个`协程`中调用`另一协程`。** 如下是一个示例：

~~~python
>>> import time
>>> async def say_after(delay,what):
        await asyncio.sleep(delay)
        print(what)

>>> async def main():
        print(f"started at {time.strftime('%X')}")
        await say_after(1,"hello")
        await say_after(2,"world")
        print(f"finished at {time.strftime('%X')}")

>>> asyncio.run(main())
started at 16:47:10
hello
world
finished at 16:47:13
~~~

- **用`asyncio.create_task()`方法将`Coroutine（协程）`封装为`Task（任务）`。一般用于实现异步并发操作。** 需要注意的是，只有在当前线程存在事件循环的时候才能创建任务（Task）。

我们修改以上的例程，**并发执行** 两个`say_after`协程。

~~~python
async def main():
    task1 = asyncio.create_task(say_after(1,"hello"))
    task2 = asyncio.create_task(say_after(2,"world"))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")
~~~

执行`asyncio.run(main())`,结果如下：

~~~python
started at 17:01:34
hello
world
finished at 17:01:36
~~~

#### 1.2 可等待对象

如果一个对象能够被用在`await`表达式中，那么我们称这个对象是`可等待对象（awaitable object）`。很多`asyncio API`都被设计成了`可等待的`。
主要有三类**可等待**对象：

- 协程`coroutine`

Python的`协程`是`可等待的（awaitable）`，因此能够被其他`协程`用在`await`表达式中。

~~~python
import asyncio

async def nested():
    print("something")

async def main():
    # 如果直接调用 "nested()"，什么都不会发生.
    # 直接调用的时候只是创建了一个 协程对象 ，但这个对象没有被 await,
    # 所以它并不会执行.
    nested()

    # 那么我们 await 这个协程，看看会是什么结果:
    await nested()  # 将会打印 "something".

asyncio.run(main())
~~~

- 任务`Task`

`Task`用来 **并发的** 调度协程。当一个`协程`通过类似 `asyncio.create_task()` 的函数被封装进一个 `Task`时，这个`协程` 会很快被自动调度执行：

~~~python
import asyncio

async def nested():
    return 42

async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
~~~

- 未来对象`Future`。

`Future` 是一种特殊的 **底层** 可等待对象，代表一个异步操作的**最终结果**。当一个`Future`对象被`await`的时候，表示当前的协程会持续等待，直到 `Future`对象所指向的异步操作执行完毕。在asyncio中，`Future`对象能使**基于回调**的代码被用于`asyn/await`表达式中。**一般情况下**，在应用层编程中，**没有必要** 创建`Future`对象。
有时候，有些`Future`对象会被一些库和`asyncio` API暴露出来，我们可以`await`它们：

~~~python
async def main():
    await function_that_returns_a_future_object()

    # this is also valid:
    await asyncio.gather(
        function_that_returns_a_future_object(),
        some_python_coroutine()
    )
~~~

#### １.3 创建task任务和执行`asyncio`程序

~~~
asyncio.create_task(coro)
~~~

将`coro`参数指定的`协程（coroutine）`封装到一个`Task`中，并调度执行。返回值是一个`Task`对象。任务在由[`get_running_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop)返回的事件循环（loop）中执行。如果当前线程中没有正在运行的事件循环，将会引发[`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError)异常:

~~~python
import asyncio
async def coro_1():
    print("do somthing")

task = asyncio.create_task(coro_1())

# 因为当前线程中没有正运行的事件循环，所以引发异常：
Traceback (most recent call last):
  File "C:\Program Files\Python37\lib\site-packages\IPython\core\interactiveshell.py", line 3265, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-4-456c15a4ed16>", line 1, in <module>
    task = asyncio.create_task(coro_1())
  File "C:\Program Files\Python37\lib\asyncio\tasks.py", line 324, in create_task
    loop = events.get_running_loop()
RuntimeError: no running event loop
~~~

对以上代码稍作修改，创建`main()`方法，在其中创建`Task`对象，然后在主程序中利用`asyncio.run()`创建`事件循环`：

~~~python
import asyncio
async def coro():
    print("something is running")

async def main():
    task = asyncio.create_task(coro())
    print(asyncio.get_running_loop())   

asyncio.run(main())

# 执行结果如下：
<_WindowsSelectorEventLoop running=True closed=False debug=False>
something is running
~~~

此函数已经被引入到Python 3.7。在Python早期版本中，可以使用底层函数`asyncio.ensure_future()`代替。

~~~python
asyncio.run(coro, * , debug=False)
~~~

这个函数运行`coro`参数指定的 `协程`，负责 **管理`asyncio`事件循环** ， **终止异步生成器**。在同一个线程中，当已经有`asyncio`事件循环在执行时，不能调用此函数。如果`debug=True`，事件循环将运行在 **调试模式**。此函数总是创建一个新的事件循环，并在最后关闭它。建议将它用作`asyncio`程序的主入口，并且只调用一次。
**重要**：这个函数是在Python 3.7被临时添加到`asyncio`中的。

#### 1.4 并发执行Tasks

~~~~python
awaitable asyncio.gather(* aws, loop=None, return_exceptions=False)
~~~~

并发执行`aws`参数指定的 `可等待（awaitable）对象`序列。如果 `aws` 序列中的某个 `awaitable 对象` 是一个 `协程`,则自动将这个 `协程` 封装为 `Task`对象进行处理。例如：

~~~~python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2)...
#     Task B: Compute factorial(2)...
#     Task C: Compute factorial(2)...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3)...
#     Task C: Compute factorial(3)...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4)...
#     Task C: factorial(4) = 24
~~~~

如果所有的`awaitable`对象都执行完毕，则返回 **awaitable对象执行结果的聚合列表**。返回值的顺序于`aws`参数的顺序一致。简单修改以上代码：

~~~python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        #print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i

    #print(f"Task {name}: factorial({number}) = {f}")
    return number

async def main():
    # Schedule three calls *concurrently*:
    print(await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    ))

asyncio.run(main())

# Expected output:
#
#[2, 3, 4]#await asyncio.gather()的返回值是一个列表，
#分别对应factorial("A", 2),factorial("B", 3),factorial("C", 4)的执行结果。
~~~

如果`return_execptions`参数为`False`（默认值即为`False`），引发的第一个异常会立即传播给等待`gather()`的任务，即调用`await asyncio.gather()`对象。序列中其他`awaitable`对象的执行不会受影响。例如：

~~~python
import asyncio

async def division(divisor, dividend):
    if divisor == 0:
        raise ZeroDivisionError
    else:
        print(f"{dividend}/{divisor}={dividend/divisor}")
        return dividend/divisor

async def main():
    # Schedule three calls *concurrently*:
    print(await asyncio.gather(
        division(0, 2),
        division(1, 2),
        division(2, 2),
    ))

asyncio.run(main())
~~~

执行结果：

~~~python
2/1=2.0
2/2=1.0
Traceback (most recent call last):
  File "test.py", line 19, in <module>
    asyncio.run(main())
  File "c:\Program Files\Python37\lib\asyncio\runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "c:\Program Files\Python37\lib\asyncio\base_events.py", line 573, in run_until_complete
    return future.result()
  File "test.py", line 16, in main
    division(2, 2),
  File "test.py", line 6, in division
    raise ZeroDivisionError
ZeroDivisionError
~~~

如果`return_exceptions`参数为`True`，异常会和正常结果一样，被聚合到结果列表中返回。对以上代码稍作修改，将`return_exceptions`设为`True`：

~~~python
import asyncio


async def division(divisor, dividend):
    if divisor == 0:
        raise ZeroDivisionError
    else:
        print(f"{dividend}/{divisor}={dividend/divisor}")
        return dividend/divisor

async def main():
    # Schedule three calls *concurrently*:
    print(await asyncio.gather(
        division(0, 2),
        division(1, 2),
        division(2, 2),
        return_exceptions=True
    ))

asyncio.run(main())
~~~

执行结果：

~~~python
2/1=2.0
2/2=1.0
[ZeroDivisionError(), 2.0, 1.0]#错误不会向上传播，而是作为结果返回
~~~

如果`gather()`被取消，则提交的所有`awaitable`对象（尚未执行完成的）都会被取消。例如：

~~~python
import asyncio

async def division(divisor, dividend):
    if divisor == 0:
        raise ZeroDivisionError
    else:
        await asyncio.sleep(divisor)
        print(f"{dividend}/{divisor}={dividend/divisor}")
        return dividend/divisor

async def main():
    # Schedule three calls *concurrently*:
    t = asyncio.gather(
        division(0, 2),
        division(1, 5),
        division(3, 6),
        return_exceptions=True
    )
    await asyncio.sleep(2)
    t.cancel()
    await t

asyncio.run(main())
~~~

执行结果：

```python
5/1=5.0 #除已执行的之外，其他的任务全部被取消
Traceback (most recent call last):
  File "test.py", line 23, in <module>
    asyncio.run(main())
  File "c:\Program Files\Python37\lib\asyncio\runners.py", line 43, in run
    return loop.run_until_complete(main)
  File "c:\Program Files\Python37\lib\asyncio\base_events.py", line 573, in run_until_complete
    return future.result()
concurrent.futures._base.CancelledError
#在return_exceptions=True的情况下，异常依然向上传播。
```

如果`aws`中某些`Task`或`Future`被取消，`gather()`调用不会被取消，被取消的`Task`或`Future`会以引发`CancelledError`的方式被处理。这样可以避免个别`awaitable`对象的取消操作影响其他`awaitable`对象的执行。例如：

```python
import asyncio

async def division(divisor, dividend):
    if divisor == 0:
        raise ZeroDivisionError
    else:
        await asyncio.sleep(divisor)
        print(f"{dividend}/{divisor}={dividend/divisor}")
        return dividend/divisor

async def main():
    # Schedule three calls *concurrently*:
    task1 = asyncio.create_task(division(0, 2))
    task2 = asyncio.create_task(division(1, 5))
    task3 = asyncio.create_task(division(3, 6))
    t = asyncio.gather(
        task1,
        task2,
        task3,
        return_exceptions=True
    )
    task1.cancel()

    print(await t)

asyncio.run(main())
```

预期执行结果如下：

```
5/1=5.0
6/3=2.0
[CancelledError(), 5.0, 2.0] # 仅task1被取消，其他任务不受影响。
```

#### 1.5 避免取消

~~~python
awaitable asyncio.shield(aw, * , loop=None)
~~~

防止`awaitable`对象被[取消(cancelled)](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task.cancel)执行。如果`aw`参数是一个`协程(coroutines)`,该对象会被自动封装为`Task`对象进行处理。通常，代码：

```
#code 1
res = await shield(something())
```

同代码：

```
#code 2
res = await something()
```

是等价的。
特殊情况是，如果包含以上代码的`协程`被 **取消**，`code 1`与`code 2`的执行效果就完全不同了：

- `code 1`中，运行于`something()`中的任务 **不会被取消**。
- `code 2`中，运行于`something()`中的任务 **会被取消**。

在`code 1`中，从`something()`的视角看，取消操作并没有发生。然而，事实上它的调用者确实被取消了，所以`await shield(something())`仍然会引发一个`CancelledError`异常。

```python
import asyncio
import time

async def division(divisor, dividend):
    if divisor == 0:
        raise ZeroDivisionError
    else:
        await asyncio.sleep(divisor)
        print(f"{time.strftime('%X')}:{dividend}/{divisor}={dividend/divisor}")
        return dividend/divisor

async def main():
    # Schedule three calls *concurrently*:
    print(f"Start time:{time.strftime('%X')}")
    task1 = asyncio.shield(division(1, 2))
    task2 = asyncio.create_task(division(1, 5))
    task3 = asyncio.create_task(division(3, 6))

    res = asyncio.gather(task1, task2, task3, return_exceptions=True)

    task1.cancel()
    task2.cancel()
    print(await res)

asyncio.run(main())
```



执行结果：

```python
Start time:10:38:48
10:38:49:2/1=2.0
10:38:51:6/3=2.0
[CancelledError(), CancelledError(), 2.0]
#task1虽然被取消，但是division(1,2)这个函数r依然正常执行了。
#task2被取消后，division(1,5)没有执行
#虽然task1内的协程被执行，但返回值依然为CancelledError
```



如果`something()`以其他的方式被取消，比如从自身内部取消，那么`shield()`也会被取消。
如果希望完全忽略`取消操作`（不推荐这么做），则可以将`shield()`与`try/except`结合起来使用：

```python
try:
    res = await shield(something())
except CancelledError:
    res = None
```

### 02. 协程应用

这里主要是关于Python中的协程的使用，其中：

- python: 3.7.7
- aiohttp: 3.62

关于`asyncio_demo.py`的作用

1. 创建一个任务队列 fetching（asyncio.Queue()）

2. 所有任务put进任务队列（self.fetching.put(url)）
3. 建立两个处理任务的worker（all_the_coros）
4. 两个work分别执行任务，哪个worker先执行完自己的任务就继续从任务队列（fetching）里面拿任务

如果将`asyncio_demo.py`应用于爬虫项目，那么则有了`aiohttp_demo.py`，通过`aiohttp`模块的异步http请求可以做到异步抓取



