# -*- coding: utf-8 -*-#
# --------------------------------设置工作路径------------------------------------#
from configparser import ConfigParser
from twisted.enterprise import adbapi
import logging
import pymysql
import time
import json
import os
import sys
abspath = os.path.split(os.path.realpath(__file__))[0]
father_path = os.path.dirname(abspath)
sys.path.append(abspath)
sys.path.append(father_path)
# --------------------------------导入模块和包------------------------------------#


class TmallSourceCommentPipelineByTwi(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool
        self.logger = logging.getLogger("TmallSourceComment")

    @classmethod
    def from_settings(cls, settings):
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        cfg = ConfigParser()
        cfg.read(abspath + "/resources/dbconf.ini")
        env = "online"
        db_params = dict(
            host=cfg.get(env, "host"),
            db=cfg.get(env, "db"),
            port=int(cfg.get(env, "port")),
            user=cfg.get(env, "user"),
            passwd=cfg.get(env, "password"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            # 出错自动重连
            cp_reconnect=True,
            # 最大连接数
            cp_max=20
        )
        # 连接池
        # 1.使用的第三方操作mysql的包     2.链接mysql需要的参数
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """

        result = self.db_pool.runInteraction(self.do_insert, item)
        # 给执行结果添加错误回调函数
        result.addErrback(self.sql_failed, item)
        # 交给下一个pipeline继续进行处理
        return item

    def do_insert(self, cursor, item):
        # 初始化SQL语句
        insert_sql = """
        insert ignore into tm_comment_info (content, comment_id, nickname, replies, item_id, 
        fetch_time, create_time, comment_total, after_count, pic_count, 
        store_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s)
        """
        # 产品信息
        sku_id = item["product_id"]["sku_id"]
        seller_id = item["product_id"]["seller_id"]
        # 评论数量, 包括追评数，有图评价数，总评数
        rage_count = item["rage_count"]
        after_count = rage_count["used"]  # 追评
        pic_count = rage_count["picNum"]  # 有图评价
        # 如果content=1则这里需要加起来, 如果content=0则不需要，total则为累计评论
        # total_count = rage_count["total"] + after_count + pic_count  # 总数
        total_count = rage_count["total"]
        # 页码
        current_page = item["current_page"]
        # 详细的评论列表
        result_list = item["comment_list"]
        for result in result_list:
            creation_time = result["rateDate"]
            content = result["rateContent"]
            comment_id = result["id"]
            nickname = result["displayUserNick"]

            # 追评解析为json格式
            append_comment = str(result["appendComment"]['content'])
            try:
                after_comment_creat_time = str(
                    result["appendComment"]["commentTime"])
                append_comment = {
                    "id": "zp" + str(comment_id),
                    "createTime": str(after_comment_creat_time),
                    "content": str(append_comment),
                }
                append_comment_str = json.dumps(
                    append_comment, separators=(',', ':'), ensure_ascii=False)
            except (KeyError, TypeError):
                self.logger.error("追评解析为json出错：" + str(append_comment))
                append_comment_str = None
            # 套餐类型
            # 颜色分类:白色;五星脚材质:铝合金脚;扶手类型:旋转升降扶手
            try:
                auction_sku = str(result['auctionSku'])
            except (KeyError, TypeError):
                auction_sku = None

            # 评论的回复
            replies = result["reply"]
            replies = None if len(replies) < 1 else str(replies)

            # 抓取时间
            fetch_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # **********************************************************************************************************
            #                                       数据写入Mysql中                                                     *
            # **********************************************************************************************************
            params = (
                content, str(comment_id), nickname, replies, str(sku_id),
                fetch_time, creation_time, str(total_count), str(
                    after_count), str(pic_count),
                str(seller_id)
            )
            cursor.execute(insert_sql, params)
            self.logger.info("=============== 写入到MySQL数据库成功: ===============\n"
                             "{}--{}--{}".format(content, creation_time, str(current_page)))

    def sql_failed(self, fail, item):
        """
        :param fail: 错误原因
        :param item: 执行sql错误的数据
        :return:
        """
        self.logger.error(fail)
        self.logger.error('出现问题的数据: {}'.format(item))
