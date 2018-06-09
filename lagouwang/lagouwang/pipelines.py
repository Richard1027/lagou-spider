# # --*-- coding: utf8 --*--
#
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

#
# class LagouwangPipeline(object):
#
#     def __init__(self, dbpool):
#         self.dbpool = adbapi.ConnectionPool('pymysql', db='spider', user='root', passwd='mysqladmin')
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparams = dict(
#             host = settings['mysql_host'],
#             port = settings['mysql_port'],
#             db = settings['mysql_dbname'],
#             user = settings['mysql_user'],
#             passwd = settings['mysql_passwd'],
#             charset = 'utf8',
#             cursorclass = pymysql.cursors.DictCursor,
#             use_unicode = True,
#         )
#
#         dbpool = adbapi.ConnectionPool("pymysql", **dbparams)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider)
#
#     def hand_error(self, failure, item, spider):
#         print(failure)
#
#     def do_insert(self, cursor, item):
#         insert_sql, params = item.insert_values()
#         print(insert_sql, params)
#         cursor.execute(insert_sql, params)
#         return item


class LagouwangPipeline(object):

    # def process_item(self, item, spider):
    #     return item

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            "pymysql",
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='mysqladmin',
            db='spider',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):

        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.hand_error, item, spider)

    def hand_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.insert_values()
        cursor.execute(insert_sql, params)
        return item
