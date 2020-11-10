## 介绍与使用方法

### [01.实时监控日志文件新写入的行](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Monitor/follow_file.py)

利用python的`yield`来实现一个生成器函数，然后调用这个生成器函数，这样当日志文件有变化时就打印新的行。其中`seek()`函数的用法如下，这个函数接收2个参数：`file.seek(off, whence=0)`，从文件中移动`off`个操作标记（文件指针），正数往结束方向移动，负数往开始方向移动。如果设定了`whence`参数，就以`whence`设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。

```
# 从头开始
os.SEEK_SET = 0
# 当前位置
os.SEEK_CUR = 1
# 文件末尾
os.SEEK_END = 2
```

#### [1.1 监控日志文件重启某个脚本](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Monitor/MonitorAndRestart.py)

监控指定文件，如果指定时间内没有新的写入，则结束进程然后重启指定脚本

```python
_monitor_log_file = ""    	# 待监控的文件
_restart_py_path = ""		# 重启的脚本的路径
_monitor_process_word = ""	# 用于搜索进程的关键词
_log_file_path = ""			# 新重启脚本的日志输出
```

### [02. 实时监控日志文件新写入的行（Watchdog模块使用）](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Monitor/MonitorFile.py)

利用`watchdog`模块实现的文件监控。自定义了`MonitorHandler`类并继承`PatternMatchingEventHandler`类，重写`PatternMatchingEventHandler`类的`on_modified`等方法，用于监控文件是否被修改、删除、创建、移动等，可以在重写的方法中定义自己需要的操作，比如输出最后一行。

```python
# 模块可以指定需要监控的文件类型，文件名等参数

# watch_patterns:      监控文件的模式，输入为列表形式     ["*.py", "*.txt", "*.log"]
# ignore_patterns:     忽略的文件模式，输入为列表形式     [] / ["*.tmp"]
# ignore_directories:  是否忽略文件夹变化               True/False
# case_sensitive:      是否对大小写敏感                 True/False
# watch_path:          监控文件夹目录
# go_recursively:      是否监控子文件夹                 True/False
# file_name:           是否监控指定文件，如果是则直接指定文件名，否则赋值为空字符串
```

