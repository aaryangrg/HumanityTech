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
    
def create_databases():
    connector = mysql.connector.connect(host = "localhost" , user = "root" , passwd ="He@dhotkiller123")
    cursor = connector.cursor()

    #initializing databases for each state
    for key in all_state_ngos:
        cursor.execute("create database {}".format(key))
    
def write_to_database():
    #use csv files , write to database and then remove csv files.
    pass

class DataExtractor(scrapy.Spider):
    name = "dataextractor"

    def parse(self,response):
        #extract statename from response.url , open a csv file in append mode - make our headers , extract info and put into csv by statename
        ngo_info = {}
        state_name = response.url.split("/")[3].replace("-"," ")[0:-5:1].title()
        header = response.xpath("//h1[@class='npos-postheader entry-title']/text()").extract()[0]

        try : 
            header_parts = header.split(",")
            ngo_info["Name"] = header_parts[0].rstrip(" ")
            ngo_info["City"] = header_parts[1].lstrip(" ")
            
        except: #return lets me skip out of the function and not add the ngo
                return 

        all_info = response.xpath("//div[@class = 'npos-postcontent clearfix']/p/text()").extract()
        
        #using list comprehension to search of Phone,Tel,Mobile,Add,Purpose,Email,Website
        required_info = ["Phone","Mobile","Add","Tel","Purpose","Email","Website"]# +Name + City
        for field in required_info:
            available_info = [i for i in  all_info if field in i]
            if len(available_info) != 0 :
                field_info = available_info[0].split(":")[1].strip(" ")
                ngo_info[field] = field_info
            else:
                ngo_info[field] = "NOT AVAILABLE"

        #append current ngo data at the end of the state file
        f = open("{}.csv".format(state_name),"a",newline = "")
        writer = csv.writer(f)
        row = [ngo_info["Name"],ngo_info["Add"],ngo_info["City"],ngo_info["Email"],ngo_info["Phone"],ngo_info["Mobile"],ngo_info["Tel"],ngo_info["Purpose"]]
        writer.writerow(row)
        
    def start_requests(self):
        f = open('tempurls.txt', 'r')
        all_urls = f.readlines()
        for url in all_urls:
            yield scrapy.Request(url = url , callback= self.parse)
            
   # TODO  See if i can generate links.
   
#the spider which collects all links required.
class DataCollector(scrapy.Spider):
    global all_state_ngos
    name = "datacollector"
    start_urls = ["https://ngosindia.org/"] 

    def parse(self,response):
        state_links =  response.xpath("//a[@rel = 'noopener noreferrer']/@href").extract()[1::] # links to all the state wise ngo pages
        extracted_names = []

        #Extracting statenames from the link so that its easier to make databases with statenames directly
        for state_link in state_links: 
            statename = state_link.split(".org/")[1].rstrip("/").replace("-"," ").title()
            extracted_names.append(statename)

        #initializing the dictionary
        for state in extracted_names:
            all_state_ngos[state] = []

        #extracting all links for each state - goes in random order because of queuing in the scheduler. Adds links by key = StateName in all_state_ngos
        for mainstate in state_links:
            yield scrapy.Request(url = mainstate, callback = get_StateNgos)
        
    


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(DataCollector)

    print("[DONE EXTRACTING URLS]")
    print("[INITIATING DATA EXTRACTION!]")

    for key in all_state_ngos:
        f = open("tempurls.txt","w")
        for url in all_state_ngos[key]:
            f.write(url+"\n")
        yield runner.crawl(DataExtractor)
    reactor.stop()


"""// TODO reactor.run , Crawl() , reactor.stop()""" 
crawl()
reactor.run() 






"""
  WITH distinct_cities AS (
    SELECT 
      DISTINCT name
    FROM
      state
    WHERE
     Purpose like ... AND
     City in ()
  )

  SELECT
    *
  FROM
    state
  WHERE
    name in distinct_cities
  """


