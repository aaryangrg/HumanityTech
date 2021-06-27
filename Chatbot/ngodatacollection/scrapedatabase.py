import scrapy



all_state_ngo_links= [] #global variable so that its value doesnt change in a particular iteration , will be refreshed to empty using main control loop
def get_StateNgos(response):
    page_links = response.xpath("//ul[@class = 'lcp_catlist']/li/a/@href").extract() #this code will extract all the links (of ngo pages) within a particular state page- return type [list of strings]
    all_state_ngo_links.extend(page_links)
    next_page = response.xpath("//a[@class = 'lcp_nextlink']/@href").extract()[0] #finding the next page link , so keep iterating in while until we get a empty list - return type list of strings , in this case one string
    if next_page is not None:
        yield scrapy.Request(url = next_page ,callback=get_StateNgos)
    else :
        return all_state_ngo_links
    
    
    pass

def extract_info():
    pass
class DataCollector(scrapy.Spider):
    name = "datacollector"
    start_urls = ["https://ngosindia.org/"] 

    def parse(self,response):
        state_links =  response.xpath("//a[@rel = 'noopener noreferrer']/@href").extract()[1::] # links to all the state wise ngo pages
        extracted_names = []
        for state_link in state_links: #Extracting statenames from the link so that its easier to make databases with statenames directly
            statename = state_link.split(".org/")[1].rstrip("/").replace("-"," ").title()
            extracted_names.append(statename)
        
        #creating a dictionary to hold state-wise all ngo page links
        state_ngos = {}
        #extract all links per state and store as key-value in a dictionary for future use.
        for i in range(len(extracted_names)):
            main_statepage_response = scrapy.Request(url = state_links[i])
            state_ngos[extracted_names[i]] = get_StateNgos(main_statepage_response)
            all_state_ngo_links.clear()
            
           
            #ngodata = response.xpath("//div[@class = 'npos-postcontent-clearfix']/p"/text()).extract() - method to extract the text information per page of the ngo.(everything except ngo name/title,city)
        

            





        
