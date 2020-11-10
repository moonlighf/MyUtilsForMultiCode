# MyUtilsForPython
主要是Python代码开发中自用一些**工具类**和一些能够复用的**代码模板**

### [01. 如何在Python中使用日志](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/logging)

- [common](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/logging/common)：基于传统的`logging`模块的日志类的封装
- [loguru](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/logging/loguru)：基于`loguru`模块的日志类的封装

### [02. Scrapy/Scrapy-Redis](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/Scrapy)

- [pipelines.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/pipelines.py)：Scrapy异步写入MySQL
- [extensions.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/extensions.py)：解决Scrapy-Redis抓取完后仍然阻塞等待的拓展‘
- [TmallSourceComment.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/TmallSourceComment.py)：解决Scrapy-Redis起始网址带参数以及如何从Redis中传入json格式参数而不是单独的网址

### [03. 如何在Python中发送邮件](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/Email)

- [SendEmail.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Email/SendEmail.py)：利用`smtp`模块发送邮件（gmail)

### [04. 如何在Python中使用协程](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/Coroutines)

协程相关介绍和一些协程应用的demo。

- [asyncio_demo.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Coroutines/asyncio_demo.py)：协程的简单应用，主要实现多个worker异步执行同一个队列（先进先出）
- [aiohttp_demo.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Coroutines/aiohttp_demo.py)：协程+aiohttp构成异步http请求进行网站抓取

### [05. 如何在Python中实现tail监控文件功能](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/Monitor)

- [follow_file.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Monitor/follow_file.py)：利用yield实现的简单的`tila -f`功能，实时监控日志文件然后按行读取
- [MonitorFile.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Monitor/MonitorFile.py)：利用`watchdog`模块实现的实时监控日志然后输出最后一行功能

### [06. 如何在Python中实现本地操作远程文件和文件夹](https://github.com/moonlighf/MyUtilsForMultiCode/tree/master/Python/SSHConnect)

- [SSHConnection.py](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/SSHConnect/SSHConnection.py)：利用`paramiko`模块封装的简单类，用以实现本地对远程文件的操作
