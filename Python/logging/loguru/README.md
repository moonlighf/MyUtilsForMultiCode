## 介绍与使用方法

这个日志方法主要是在普通脚本中使用的日志封装类，需要安装`loguru`模块才可使用。可以如下方法引用。

~~~python
from utils.Logging import GetLogging

LOG_FILE = os.path.join(abspath, "logs/Judge_IsOffline_{time:YYYY-MM-DD}_INFO.log")
ERROR_LOG_FILE = os.path.join(abspath, "logs/Judge_IsOffline_{time:YYYY-MM-DD}_ERROR.log")
_logClient = GetLogging(ERROR_LOG_FILE, LOG_FILE)
lg = _logClient.get()
~~~

**特别注意**：如果是在scrapy和scrapyd相结合的项目中，为了保证一个项目中多个spider的日志都能在scrapyd中查看，也能输出到不同日志文件，需要使用本日志方法，而不是使用`common`的日志方法，具体使用如下：

~~~python
# spider1
class ScrapyQuestion1Spider(RedisSpider):
    name = 'ScrapyQuestion1'
    def __init__(self, *args, **kwargs):
        super(ScrapyQuestion1Spider, self).__init__(*args, **kwargs)
        _client = GetLogging(error_log_file_path="./a.log",
                             info_log_file_path="./b.log")
        self.lsg = _client.get()
    
    def parse(self, response):
        time.sleep(0.1)
        test_item = response.meta["test_item"]
        test_item["test1"] = "这是1"
        self.lsg.info("这里是11111111111111111")
        yield test_item
~~~

~~~~python
# spider2
class ScrapyQuestion2Spider(RedisSpider):
    name = 'ScrapyQuestion2'
    def __init__(self, *args, **kwargs):
        super(ScrapyQuestion1Spider, self).__init__(*args, **kwargs)
        _client = GetLogging(error_log_file_path="./c.log",
                             info_log_file_path="./d.log")
        self.lag = _client.get()
    
    def parse(self, response):
        time.sleep(0.1)
        test_item = response.meta["test_item"]
        test_item["test2"] = "这是2"
        self.lag.info("这里是2222222222222222")
        yield test_item
~~~~

