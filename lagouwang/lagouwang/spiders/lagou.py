import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagouwang.items import LagouItemLoader, LagouItem


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/jobs/list_%E8%BD%AF%E4%BB%B6%E6%B5%8B%E8%AF%95?px=default&city=%E6%B7%B1%E5%9C%B3#filterBox']

    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171015132411-12af3b52-3a51-466f-bfae-a98fc96b4f90; LGUID=20171015132412-13eaf40f-b169-11e7-960b-525400f775ce; SEARCH_ID=070e82cdbbc04cc8b97710c2c0159ce1; ab_test_random_num=0; X_HTTP_TOKEN=d1cf855aacf760c3965ee017e0d3eb96; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsXIrWUxpNGLE2g_bKzlUCXPTRJMHxfCs6L20RqgCpUq%26wd%3D%26eqid%3Dee53adaf00026e940000000559e354cc; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_hotjob; login=false; unick=""; _putrc=""; JSESSIONID=ABAAABAAAFCAAEG50060B788C4EED616EB9D1BF30380575; _gat=1; _ga=GA1.2.471681568.1508045060; LGSID=20171015203008-94e1afa5-b1a4-11e7-9788-525400f775ce; LGRID=20171015204552-c792b887-b1a6-11e7-9788-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }


    rules = (
        Rule(LinkExtractor(allow=(r'zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=(r'gongsi/j\d\.html',)), follow=True),
        Rule(LinkExtractor(allow=(r'jobs/.*',), restrict_css=("div#s_position_list ul.item_con_list"),), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        Item_loader = LagouItemLoader(item=LagouItem(), response=response)

        # TITLE
        Item_loader.add_xpath("title", "//div[@class='job-name']/@title")
        # URL
        Item_loader.add_value("url", response.url)
        # salary
        Item_loader.add_xpath("salary", "//dd[@class='job_request']/p/span[1]/text()")
        # job_city
        Item_loader.add_xpath("job_city", "//dd[@class='job_request']/p/span[2]/text()")
        # work_years
        Item_loader.add_xpath("work_years", "//dd[@class='job_request']/p/span[3]/text()")
        # degree_need
        Item_loader.add_xpath("degree_need", "//dd[@class='job_request']/p/span[4]/text()")
        # job_type
        Item_loader.add_xpath("job_type", "//dd[@class='job_request']/p/span[5]/text()")
        # tags
        Item_loader.add_xpath("tags", "//li[@class='labels']/text()")
        # publish-time
        Item_loader.add_xpath("publish_time", "//p[@class='publish_time']/text()")
        # job_advantage
        Item_loader.add_xpath("job_advantage", "//dd[@class='job-advantage']/p/text()")
        # job_desc
        Item_loader.add_xpath("job_desc", "//dd[@class='job_bt']/div/p/text()")
        # work_addr
        Item_loader.add_xpath("work_addr", "//div[@class='work_addr']/a/text()")
        # company_name
        Item_loader.add_xpath("company_name", "//dl[@class='job_company']/dt/a/img/@alt")
        # company_url
        Item_loader.add_xpath("company_url", "//dl[@class='job_company']/dt/a/@href")




        lagou_item_loader = Item_loader.load_item()
        return lagou_item_loader

        # #Item_loader.add_css("title", "div.job-name:: attr(title)")
        # Item_loader.add_value("url", response.url)
        # Item_loader.add_value("url_object_id", response.url)
        # Item_loader.add_css("salary", "span.salary::text")
        # Item_loader.add_xpath("job_city", ".//*[@class='job_request']/p/span[2]/text()")
        # Item_loader.add_xpath("work_years", ".//*[@class='job_request']/p/span[3]/text()")
        # Item_loader.add_xpath("degree_need", ".//*[@class='job_request']/p/span[4]/text()")
        # Item_loader.add_xpath("job_type", ".//*[@class='job_request']/p/span[5]/text()")
        # Item_loader.add_css("tags", "li.labels::text")
        # Item_loader.add_css("publish_time", "p.publish_time::text")
        # Item_loader.add_css("job_advantage","dd.job_advantage p::text")
        # Item_loader.add_css("job_desc", "dd.job_bt div p::text")
        # Item_loader.add_css("work_addr", "div.work_addr")
        # Item_loader.add_css("company_name", "dl.job_company a img::attr(alt)")
        # Item_loader.add_css("company_url", "dl.job_company dt a::attr(href)")


