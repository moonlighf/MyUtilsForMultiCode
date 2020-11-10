## 介绍与使用方法

### [01. Scrapy异步写入MySQL](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/pipelines.py)

Scrapy通过`twisted`模块实现异步写入数据库（MySQL）。其中`do_insert`实现了插入操作，`sql_failed`主要是插入出错的回调函数，呈现错误原因

### [02. Scrapy-Redis起始网址带参数](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/TmallSourceComment.py)

通过`from scrapy_redis.spiders import RedisSpider`分析可知，`RedisSpider`继承于`RedisMixin`和`Spider`类，执行逻辑是`RedisMixin`的`next_requests`函数接收到了redis中data后，通过`make_request_from_data`函数来解码data生成`url`,`make_request_from_data`继续调用Spider类中的`make_requests_from_url`函数生成Request,因此重写Spider中的`make_requests_from_url`函数即可。同时，为了传入使用传入redis的其他信息，可以直接在`make_requests_from_url`进行解析。

~~~python
    def start_requests(self):
        for param in self.start_urls:
            yield self.make_requests_from_url(param)

    def make_requests_from_url(self, param):
        headers = self.get_headers()
        # 初始传入的参数在此解析
        # params = {"item_id": item_id, "shop_name": shop_name}
        params = json.loads(param)
        return scrapy.Request(url, dont_filter=True, callback=self.parse,meta={})
~~~

### [03. Scrapy-Redis抓取完后仍然阻塞等待](https://github.com/moonlighf/MyUtilsForMultiCode/blob/master/Python/Scrapy/extensions.py)

**首先解决爬虫等待，不被关闭的问题：**

- scrapy内部的信号系统会在爬虫耗尽内部队列中的request时，就会触发spider_idle信号。
- 爬虫的信号管理器收到spider_idle信号后，将调用注册spider_idle信号的**处理器**进行处理。
- 当该信号的所有处理器(handler)被调用后，如果spider仍然保持空闲状态， 引擎将会关闭该spider。

scrapy-redis 中的解决方案 在信号管理器上注册一个对应在spider_idle信号下的spider_idle()方法，当spider_idle触发是，信号管理器就会调用这个爬虫中的spider_idle()， Scrapy_redis 源码如下：

```python
def spider_idle(self):
    """Schedules a request if available, otherwise waits."""
    # XXX: Handle a sentinel to close the spider.
    # 这里调用schedule_next_requests() 来从redis中生成新的请求
    self.schedule_next_requests()    
    # 抛出不要关闭爬虫的DontCloseSpider异常，保证爬虫活着
    raise DontCloseSpider              
```

**解决思路：**

- 通过前面的了解，我们知道 爬虫关闭的关键是 spider_idle 信号。
- spider_idle信号只有在爬虫队列为空时才会被触发， 触发间隔为5s。
- 那么我也可以使用同样的方式，在信号管理器上注册一个对应在spider_idle信号下的spider_idle()方法。
- 在 spider_idle() 方法中，编写结束条件来结束爬虫，这里以 判断redis 中关键key 是否为空，为条件

使用时，在`settings.py`中添加以下配置， 将`TmallCrawlerSrapyByRedis`替换为你的项目目录名。此方法只使用于5秒内跑不完一组链接的情况，如果一组链接5秒就能跑完，需要在此基础上做一些判断

~~~python
# 开启扩展，当redis中的任务结束的时候自动停止爬虫
REDISEXT_ENABLED = True
# 配置空闲持续时间单位为 360 个 ，一个时间单位为5s
IDLE_NUMBER = 12*5
EXTENSIONS = {
    'TmallCrawlerSrapyByRedis.extensions.RedisSpiderSmartIdleClosedExtensions': 500,
}
~~~

