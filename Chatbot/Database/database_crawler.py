# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess


class DatabaseCrawlerSpider(CrawlSpider):
    name = 'database_crawler'
    allowed_domains = ['ngosindia.org'] # to restrict functionality to just this website.
    start_urls = ['https://ngosindia.org/']

    le_main_pages = LinkExtractor(restrict_xpaths="//a[@rel = 'noopener noreferrer']")#main state pages)
    main_pages_rule =  Rule(le_main_pages, follow = True)

    le_next_page = LinkExtractor(restrict_xpaths="//a[@class = 'lcp_nextlink']")#extracts next page
    next_page_rule = Rule(le_next_page,follow = True)#do this on every page

    le_ngo_details = LinkExtractor(restrict_xpaths="//ul[@class = 'lcp_catlist']/li/a")#extracts ngo links for each page
    ngo_details_rule = Rule(le_ngo_details, callback='parse_item', follow = False)#parses each of those extarcted links

    rules = (
        ngo_details_rule,next_page_rule,main_pages_rule
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item


process = CrawlerProcess()
process.crawl(DatabaseCrawlerSpider)
process.start()