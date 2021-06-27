import scrapy
import mysql.connector 
from scrapy.crawler import CrawlerProcess
from scrapy.http.request import Request
import csv
import pickle 
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

all_state_ngos = {}
main_state_links = []
def get_StateNgos(response):
    global all_state_ngos
    url = response.url
    state_name =  url.split("/")[3].replace("-"," ").title()
    page_links = response.xpath("//ul[@class = 'lcp_catlist']/li/a/@href").extract() #this code will extract all the links (of ngo pages) within a particular state page- return type [list of strings]
    all_state_ngos[state_name] += page_links
    next_page = response.xpath("//a[@class = 'lcp_nextlink']/@href").extract_first() #finding the next page link , so keep iterating in while until we get a empty list - return type list of strings , in this case one string
    if next_page is not None:
        yield scrapy.Request(url = next_page ,callback=get_StateNgos)
    else :
        pass

#this spider extracts the main statepages to extract and pass to DataCollector which will parse all statelinks in sequence by state
class BaseLinker(scrapy.Spider):
    name = "baselinker"
    start_urls = ["https://ngosindia.org/"]
    def parse(self,response):
        global main_state_links
        state_links =  response.xpath("//a[@rel = 'noopener noreferrer']/@href").extract()[1::] # links to all the state wise ngo pages
        extracted_names = []
        state_links[-1],state_links[-2] = state_links[-2],state_links[-1]
        #Extracting statenames from the link so that its easier to make databases with statenames directly
        for state_link in state_links: 
            statename = state_link.split(".org/")[1].rstrip("/").replace("-"," ").title()
            extracted_names.append(statename)

        #initializing the dictionary
        for state in extracted_names:
            all_state_ngos[state] = []

        main_state_links = list(state_links)



#Extracting links for all NGO's per state in sequential manner
class DataCollector(scrapy.Spider):
    global all_state_ngos
    name = "datacollector"

    def parse(self,response):
        url = response.url
        state_name =  url.split("/")[3].replace("-"," ").title()
        page_links = response.xpath("//ul[@class = 'lcp_catlist']/li/a/@href").extract() #this code will extract all the links (of ngo pages) within a particular state page- return type [list of strings]
        all_state_ngos[state_name] += page_links
        next_page = response.xpath("//a[@class = 'lcp_nextlink']/@href").extract_first() #finding the next page link , so keep iterating in while until we get a empty list - return type list of strings , in this case one string
        if next_page is not None:
            yield scrapy.Request(url = next_page ,callback = self.parse)
        else :
            pass
    
    """def start_requests(self):
        f = open("tempstate.txt","r")
        initial_url = f.readline().rstrip("\n")
        yield scrapy.Request(url = initial_url,callback=self.parse)"""
    
    
    
configure_logging()
runner = CrawlerRunner()

"""@defer.inlineCallbacks
def crawl():
    yield runner.crawl(BaseLinker)
    #forcing per state extraction to be sequential
    for link in main_state_links:
        f = open("tempstate.txt","w")
        f.write(link+"\n")
        yield runner.crawl(DataCollector)
    #reactor.stop()

crawl()
reactor.run()"""
process = CrawlerProcess()
process.crawl(BaseLinker)
process.crawl(DataCollector, start_urls= main_state_links)
process.start()



f = open("bin2.dat","wb")
pickle.dump(all_state_ngos,f)
f.close()
