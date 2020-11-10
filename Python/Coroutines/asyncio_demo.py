# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  asyncio_demo
# Description  :
# Author       :  skymoon9406@gmail.com
# Date         :  2020/7/14
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import asyncio
import time
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

    async def crawl(self):
        # DON'T await here; start consuming things out of the queue, and
        # meanwhile execution of this function continues. We'll start two
        # coroutines for fetching and two coroutines for processing.
        all_the_coros = asyncio.gather(
            *[self._worker(i) for i in range(self.max_workers)])

        # place all URLs on the queue
        for url in self.urls:
            await self.fetching.put(url)

        # now put a bunch of `None`'s in the queue as signals to the workers
        # that there are no more items in the queue.
        for _ in range(self.max_workers):
            await self.fetching.put(None)

        # now make sure everything is done
        await all_the_coros

    async def _worker(self, i):
        while True:
            url = await self.fetching.get()
            if url is None:
                # this coroutine is done; simply return to exit
                return

            print("in", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print(f'Fetch worker {i} is fetching a URL: {url}')
            if url in ["http://www.google.com", "http://www.gamespot.com", "http://www.facebook.com"]:
                page = await self.fetch(url)
            else:
                page = await self.fetch2(url)
            self.process(page)
            await asyncio.sleep(1)
            print("out", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    async def fetch(self, url):
        print("Fetching URL: " + url)
        await asyncio.sleep(10)
        return f"the contents of {url}"

    async def fetch2(self, url):
        print("Fetching URL: " + url)
        await asyncio.sleep(5)
        return f"the contents of {url}"

    def process(self, page):
        print("processed page: " + page)


# main loop
c = Crawler(['http://www.google.com', 'http://www.yahoo.com',
             'http://www.cnn.com', 'http://www.gamespot.com',
             'http://www.facebook.com', 'http://www.evergreen.edu'])
asyncio.run(c.crawl())
