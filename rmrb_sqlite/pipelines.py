#!/usr/bin/python
# coding:utf-8

from items import RmrbSqliteItem
import sqlite3


class RmrbSqlitePipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == RmrbSqliteItem:  # 此句非必要，在多个items时可能需要用到
            conn = sqlite3.connect('rmrb.db')
            cur = conn.cursor()
            sql = "insert into t201703(title,publish,link,text) values (?,?,?,?)"
            cur.execute(sql, (item['title'], item['publish'], item['link'], item['text'],))
            conn.commit()
            cur.close()
            conn.close()
        return item
