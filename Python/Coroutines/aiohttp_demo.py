# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  asyncioDemo
# Description  :  利用协程进行数据抓取的代码demo
# Author       :  skymoon9406@gmail.com
# Date         :  2020/7/14
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
from aiohttp.client_exceptions import ClientConnectorError, ClientResponseError, ServerDisconnectedError
from aiohttp.http_exceptions import HttpProcessingError
import asyncio
import aiohttp
import sys
import os
CURRENT_PATH = os.getcwd()
PARENT_PATH = os.path.dirname(CURRENT_PATH)
sys.path.append(CURRENT_PATH)
sys.path.append(PARENT_PATH)
# --------------------------------导入模块和包------------------------------------#


class Crawler:
    """
    解释：
    （1）创建一个任务队列 fetching（asyncio.Queue()）
    （2）所有任务put进任务队列（self.fetching.put(url)）
    （3）建立两个处理任务的worker（all_the_coros）
    （4）两个work分别执行任务，哪个worker先执行完自己的任务就继续从任务队列（fetching）里面拿任务
    """

    def __init__(self, urls, max_workers=2):
        self.urls = urls
        # create a queue that only allows a maximum of two items
        self.fetching = asyncio.Queue()
        self.max_workers = max_workers

        self.headers = {}

    async def crawl(self):
        # DON'T await here; start consuming things out of the queue, and
        # meanwhile execution of this function continues. We'll start two
        # coroutines for fetching and two coroutines for processing.
        all_the_cors = asyncio.gather(
            *[self._worker(i) for i in range(self.max_workers)])

        # place all URLs on the queue
        for url in self.urls:
            await self.fetching.put(url)

        # now put a bunch of `None`'s in the queue as signals to the workers
        # that there are no more items in the queue.
        for _ in range(self.max_workers):
            await self.fetching.put(None)

        # now make sure everything is done
        await all_the_cors

    async def _worker(self, i):
        while True:
            url = await self.fetching.get()
            if url is None:
                # this coroutine is done; simply return to exit
                return
            print(f'Fetch worker {i} is fetching a URL: {url}')
            page = await self.fetch(url)
            self.process(page)
            await asyncio.sleep(0.1)

    async def fetch(self, url, num_retries=3):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, headers=self.headers) as response:
                    # async with session.get(url=url, headers=headers, proxy=self.proxies,
                    #                        verify_ssl=False) as response:
                    # raise_for_status(),如果不是200会抛出HttpProcessingError错误
                    response.raise_for_status()
                    return await response.text()
            except HttpProcessingError:
                # 如果不是200就重试，每次递减重试次数,每次重试之间间隔1秒
                if num_retries > 0:
                    await asyncio.sleep(1)
                    return await self.fetch(url, num_retries - 1)
                else:
                    print("========== 网址抓取错误：{} | 已经重试 {} 次 ==========".format(
                        url, num_retries))
            except (ClientConnectorError, ClientResponseError, ServerDisconnectedError):
                print("========== 连接网址响应错误: {} ==========".format(url))

    def process(self, page):
        print("processed page: " + page)


# main loop
c = Crawler(['http://www.google.com', 'http://www.yahoo.com',
             'http://www.cnn.com', 'http://www.gamespot.com',
             'http://www.facebook.com', 'http://www.evergreen.edu'])
asyncio.run(c.crawl())
