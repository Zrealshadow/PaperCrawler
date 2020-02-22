import scrapy

class PaperCrawler(scrapy.Spider):
    name='ArXiv'
    start_urls=["https://arxiv.org/archive/cs"]
    offset_years=2
    org_url='https://arxiv.org'
    def __init__(self,category=None,*args,**kwargs):
        super(PaperCrawler,self).__init__(*args,**kwargs)


    def parse(self,response):
        years_links=response.xpath('/html/body/main/div//ul[1]/li[last()]//a/@href').extract()
        static_links=[ self.org_url+i for i in years_links]
        for l in static_links:
            yield scrapy.Request(l,callback=self.parse_month)
    
    def parse_month(self,response):
        month_links=response.xpath('/html/body/div/ul[1]/li/a[1]/@href').extract()
        static_links=[self.org_url+i for i in month_links]
        for l in static_links:
            yield scrapy.Request(l,callback=self.parse_page)

    def parse_page(self,response,item):
        pass


