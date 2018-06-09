# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


def ends_filter(value):

    if "查看地图" in value:
        tp_list = value.split('\n')
        v_list = [v.strip for v in tp_list if "查看地图" not in v]
        return "".join(v_list).strip()
    elif "发布于拉勾网" in value:
        return value.replace("发布于拉勾网", "").strip()
    elif "/" in value:
        return value.replace("/", '').strip()
    else:
        return value.strip()


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    # salary = scrapy.Field()
    # job_city = scrapy.Field()
    # work_years = scrapy.Field()
    # degree_need = scrapy.Field()
    # job_type = scrapy.Field()
    # tags = scrapy.Field()
    # publish_time = scrapy.Field()
    # job_advantage = scrapy.Field()
    # job_desc = scrapy.Field()
    # work_addr = scrapy.Field()
    salary = scrapy.Field(input_processor=MapCompose(ends_filter))
    job_city = scrapy.Field(input_processor=MapCompose(ends_filter))
    work_years = scrapy.Field(input_processor=MapCompose(ends_filter))
    degree_need = scrapy.Field(input_processor=MapCompose(ends_filter))
    job_type = scrapy.Field()
    tags = scrapy.Field(output_processor=Join(","))
    publish_time = scrapy.Field(input_processor=MapCompose(ends_filter))
    #job_advantage = scrapy.Field(output_processor=MapCompose(ends_filter))
    job_advantage = scrapy.Field(output_processor=Join(","))
    job_desc = scrapy.Field(output_processor=MapCompose(ends_filter))
    work_addr = scrapy.Field(input_processor=MapCompose(remove_tags, ends_filter))
    company_name = scrapy.Field()
    company_url = scrapy.Field()

    def insert_values(self):
        self['job_desc'] = " ".join(list(self['job_desc']))

        insert_sql = """
        insert into lagou_job(title, url, salary, job_city, work_years,
        degree_need, job_type, publish_time, tags, job_advantage, job_desc, work_addr,
        company_url, company_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
        """

        params = (
            self["title"], self["url"], self["salary"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"], self["publish_time"],
            self["tags"], self["job_advantage"], self["job_desc"], self["work_addr"],
            self["company_url"], self["company_name"]
        )

        return insert_sql, params
