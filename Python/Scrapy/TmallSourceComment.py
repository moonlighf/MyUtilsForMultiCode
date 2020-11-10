# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  TmallSourceCommentSpider
# Description  :  天猫旗舰店评论抓取，通过Redis获取任务列表
# Author       :  skymoon9406@gmail.com
# Date         :  2020/7/06
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import os
import sys
abspath = os.path.split(os.path.realpath(__file__))[0]
father_path = os.path.dirname(abspath)
sys.path.append(abspath)
sys.path.append(father_path)
# --------------------------------导入模块和包------------------------------------#
import re
import time
import json
import scrapy
import random
from ..utils.better_logging import Logger
from scrapy_redis.spiders import RedisSpider
from scrapy.utils.project import get_project_settings


class TmallSourceCommentSpider(RedisSpider):
    name = 'TmallSourceComment'

    custom_settings = {
        "DOWNLOAD_DELAY": 1.3,
        "CONCURRENT_REQUESTS": 32,
        "COOKIES_ENABLED": False,
        "ITEM_PIPELINES": {
            "scrapy_redis.pipelines.RedisPipeline": 300,
            "TmallCrawlerSrapyByRedis.pipelines.TmallSourceCommentPipelineByTwi": 350,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'TmallCrawlerSrapyByRedis.middlewares.RandomUserAgentMiddleware': 443,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550
        },
    }

    # 制定redis中待抓取任务的key
    today = time.strftime("%Y-%m-%d", time.localtime())
    redis_key = 'TmallSourceComment_{}:start_urls'.format(today)

    # 日志相关设置
    settings = get_project_settings()
    lg = Logger(logger_module="Common",
                log_conf_path=settings.get("LOG_CONF_PATH"),
                log_file=settings.get("LOG_FILE_PATH") + 'Tmall_SourceComment_' + today + '.log',
                log_error_file=settings.get("LOG_FILE_PATH") + 'Tmall_SourceComment_Error_' + today + '.log',)

    def __init__(self, *args, **kwargs):
        super(TmallSourceCommentSpider, self).__init__(*args, **kwargs)
        # 基础构造网址
        self.base_url = "https://rate.tmall.com/list_detail_rate.htm?" \
                        "itemId={}&sellerId={}&currentPage={}&content=0&order=1"

    def start_requests(self):
        for param in self.start_urls:
            yield self.make_requests_from_url(param)

    def make_requests_from_url(self, param):
        headers = self.get_headers()
        # 初始传入的参数在此解析
        # params = {"item_id": item_id, "shop_name": shop_name, "seller_id": seller_id, "sku_id": sku_id}
        params = json.loads(param)
        # 拼接url
        item_id, shop_name = params["item_id"], params["shop_name"]
        seller_id, sku_id = params["seller_id"], params["sku_id"]
        current_page = 1
        url = self.base_url.format(item_id, seller_id, current_page)
        return scrapy.Request(url, dont_filter=True, callback=self.parse, headers=headers,
                              meta={'download_timeout': 5, 'max_retry_times': 3,
                                    'product_info': {"seller_id": seller_id,
                                                     "current_page": current_page, "item_id": item_id},
                                    'item': item})

    def parse(self, response):
        pass
