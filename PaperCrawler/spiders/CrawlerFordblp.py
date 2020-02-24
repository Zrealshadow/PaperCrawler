import scrapy
from PaperCrawler.items import ConferenceItem

class CrawlerFordblp(scrapy.Spider):
    name='dblp'
    start_urls=[
        "https://dblp.uni-trier.de/db/conf/",
        "https://dblp.uni-trier.de/db/journals/",
        "https://dblp.uni-trier.de/db/series/"
    ]

    def parse(self,response):
        # parse every conference or journals or series web page
        
        # for one type conference 
        conf_links=response.xpath('//div[@class="hide-body"]/ul/li/a/@href').extract()
        for l in conf_links:
            yield scrapy.Request(l,callback=self.parse_oneType_conf)


        #next page 
        # url prefix
        prefix=response.url.split('?')[0]

        next_page_link=response.xpath('//div[@id="browse-conf-output"]/p')[1]\
            .xpath('./a')[1].xpath('./@href').extract()
        
        if len(next_page_link)!=0:
            next_page_link=prefix+next_page_link[0]
            yield scrapy.Request(next_page_link,callback=self.parse)
            
    def parse_oneType_conf(self,response):
        conf_type=response.xpath('//div[@id="main"]/header/h1/text()').extract()[0]
       
        conf_intro_xml_links=response.xpath('//div[@id="main"]/ul/li/nav[@class="publ"]/ul/li[2]/\
            div[@class="body"]/ul[1]/li[last()]/a/@href').extract()
        

        Selectors=response.xpath("//cite[@class='data' and @itemprop='headline']")

        for i,se in enumerate(Selectors):
            conf_Authors_url=se.xpath('./span[@itemprop="author"]/a/@href').extract()
            conf_ID=se.xpath('./span[@class="title" and @itemprop="name"]/text()').extract()[0]
            conf_intro_xml_link=conf_intro_xml_links[i]
            item=ConferenceItem()
            item["ConfID"]=conf_ID
            item["ConfType"]=conf_type
            item["ConfEdits"]=conf_Authors_url
            item["ConfDetail"]=conf_intro_xml_link
            yield item
            #xml file url **no parse


        oneyear_conf_links=response.xpath('//ul[@class="publ-list"]/li/cite/a[@class="toc-link"]\
            /@href').extract()
        for i,link in enumerate(oneyear_conf_links):
            yield scrapy.Request(link,callback=self.parse_paper)


    def parse_paper(self,response):
        pass