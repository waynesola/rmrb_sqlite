#!/usr/bin/python
# -*- coding:UTF-8 -*-

import scrapy
from bs4 import BeautifulSoup
import arrow
import urlparse
import datetime
from ..items import RmrbSqliteItem
import re


class AllArticles(scrapy.Spider):
    name = "all"
    allowed_domains = ["paper.people.com.cn"]
    start_urls = [
        "http://paper.people.com.cn"
    ]

    # def parse(self, response):
    #     item = RmrbSqliteItem()
    #     request_article = scrapy.Request(
    #         "http://paper.people.com.cn/rmrb/html/2017-04/24/nw.D110000renmrb_20170424_1-06.htm",
    #         callback=self.parse_article)
    #     request_article.meta['item'] = item
    #     yield request_article

    # # 爬取指定天数，通过range(n)指定天数
    # def parse(self, response):
    #     # 用arrow指定日期区间
    #     start = datetime.datetime(2017, 4, 24)
    #     end = datetime.datetime(2017, 4, 24)
    #     c_date = arrow.now()
    #     c_ym = c_date.format('YYYY-MM')
    #     c_d = c_date.format('DD')
    #     url = "http://paper.people.com.cn/rmrb/html/" + c_ym + "/" + c_d + "/node_642.htm"
    #     yield url
    #     for r in arrow.Arrow.range('day', start, end):
    #         c_ym = r.format('YYYY-MM')
    #         c_d = r.format('DD')
    #         url = "http://paper.people.com.cn/rmrb/html/" + c_ym + "/" + c_d + "/nbs.D110000renmrb_01.htm"
    #         yield scrapy.Request(url, callback=self.parse_section)
    #

    #

    def parse(self, response):
        url = "http://paper.people.com.cn"
        yield scrapy.Request(url, callback=self.parse_item)

    def parse_section(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        # ###################################补全搜索版块链接的代码，2017年4月24日21:12:51
        rs = soup.find_all("div", class_="right_title-name").ul.find_all('a')

        for r in rs:
            href = r.get('href')
            re.sub('./', '', href)
            url = urlparse.urljoin(response.url, href)
            yield scrapy.Request(url, callback=self.parse_item)

    # 爬取某版块所有文章，传递到parse_article()
    def parse_item(self, response):
        request_article = scrapy.Request(
            "http://paper.people.com.cn/rmrb/html/2017-04/24/nbs.D110000renmrb_03.htm",
            callback=self.parse_article)
        yield request_article
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        ds = soup.find('table', width="265", style="margin-top:3px;").find_all('a')
        for d in ds:
            href = d.get('href')
            url = urlparse.urljoin(response.url, href)
            request_article = scrapy.Request(url, callback=self.parse_article)
            yield request_article

    # 爬取某篇文章标题、正文、发表日期、链接
    def parse_article(self, response):
        item = RmrbSqliteItem()
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        temp = "    "
        h3 = soup.find('div', class_="text_c").find('h3')
        h1 = soup.find('div', class_="text_c").find('h1')
        h2 = soup.find('div', class_="text_c").find('h2')
        h4 = soup.find('div', class_="text_c").find('h4')
        if h3:
            temp = temp + h3.get_text() + '\n    '
        if h1:
            temp = temp + h1.get_text() + '\n    '
        if h2:
            temp = temp + h2.get_text() + '\n    '
        if h4:
            temp = temp + h4.get_text() + '\n'
        ps = soup.find('div', style="display:none", id="articleContent").find_all('p')
        for p in ps:
            temp += p.get_text()
            temp += "\n"
        item['text'] = temp
        item['title'] = soup.find('title').get_text()
        item['link'] = response.url
        publish_temp = re.sub('\s', '', soup.find('div', id="riqi_", style="float:left;").get_text())
        item['publish'] = publish_temp[4:]
        yield item
