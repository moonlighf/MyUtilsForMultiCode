## 介绍与使用方法

这个日志方法主要是在`scrapy`爬虫中使用的日志封装类，可以直接在`spider`中如下方法引用。

**切记：为了在同一个工程里面不同spider中引用此类，必须把`lg`的初始化写在`def __init__`里面，不能写在外面，否则会多个spider的日志会被重定向到同一个文件里面！！**

~~~python
from ..utils.better_logging import Logger
from scrapy.utils.project import get_project_settings
import time

today = time.strftime("%Y-%m-%d", time.localtime())
lg = Logger(logger_module="Common",
            log_conf_path=settings.get("LOG_CONF_PATH"),
            log_file=settings.get("LOG_FILE_PATH") + 'Tmall_Flagship_' + today + '.log',
            log_error_file=settings.get("LOG_FILE_PATH") + 'Tmall_Flagship_Error_' + today + '.log',)
~~~

