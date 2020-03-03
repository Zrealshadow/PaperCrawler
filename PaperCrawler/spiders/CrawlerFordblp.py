import scrapy
from PaperCrawler.items import ConferenceItem,PaperItem

class CrawlerFordblp(scrapy.Spider):
    name='dblp'
    start_urls=[
        # "https://dblp.uni-trier.de/db/conf/",
        # # "https://dblp.uni-trier.de/db/journals/",
        # # "https://dblp.uni-trier.de/db/series/"
    ]

    def __init__(self,category=None,*args,**kwargs):
        # super(CrawlerFordblp,self).__init__(*args,**kwargs)
        with open('/Users/e1ixir/vscodeProject/PaperCrawler/confpath.txt') as f:
            self.start_urls=f.readlines()


    def parse(self,response):
        #指定了需要爬取议会的信息
        '''

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
        '''
        self.logger.info("start parse Conf url {}".format(response.url))
        yield scrapy.Request(response.url,callback=self.parse_oneType_conf)
            
    
    def parse_oneType_conf(self,response):
        conf_type=response.xpath('//div[@id="main"]/header/h1/text()').extract()[0]
       
        conf_intro_xml_links=response.xpath('//div[@id="main"]/ul/li/nav[@class="publ"]/ul/li[2]/\
            div[@class="body"]/ul[1]/li[last()]/a/@href').extract()
        

        Selectors=response.xpath("//cite[@class='data' and @itemprop='headline']")
        oneyear_conf_links=response.xpath('//ul[@class="publ-list"]/li/cite/a[@class="toc-link"]\
            /@href').extract()
        
        for i,se in enumerate(Selectors):
            conf_Authors_url=se.xpath('./span[@itemprop="author"]/a/@href').extract()
            conf_Authors_text=se.xpath('./span[@itemprop="author"]/a/span/text()').extract()
            conf_Authors=[ (a,b) for a , b in zip(conf_Authors_url,conf_Authors_text)]
            # ( Author_page_url, Author_name) possibly there are no editors for one conference
            
            conf_Name=se.xpath('./span[@class="title" and @itemprop="name"]/text()').extract()[0]
            conf_intro_xml_link=conf_intro_xml_links[i]
            href=se.xpath('./a[@class="toc-link"]/@href').extract()
            conf_ID=href[0] if len(href)!=0 else ""
            item=ConferenceItem()
            item["ConfID"]=conf_ID
            item["ConfName"]=conf_Name
            item["ConfType"]=conf_type
            item["ConfEdits"]=conf_Authors
            item["ConfDetail"]=conf_intro_xml_link
            yield item
            #xml file url **no parse
        
        self.logger.info("for one type Conf:{} \n confs' introductions have been parsed".format(conf_type))
   
        for i,link in enumerate(oneyear_conf_links):
            self.logger.info("start parse papers in one confs :{}".format(link))
            yield scrapy.Request(link,callback=self.parse_paper)


    def parse_paper(self,response):
        Selectors=response.xpath('//ul[@class="publ-list"]')
        if len(Selectors)==1:
            se=Selectors[0]
            paper_selectors=se.xpath('./li[@class="entry inproceedings"]')

            for pse in paper_selectors:
                paper_xml_link=pse.xpath('./nav/ul/li[2]/div[2]/ul[1]/li[last()]/a/@href')\
                    .extract()[0]
                paper_author_url=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                    /span[@itemprop="author"]/a/@href').extract()
                paper_author_name=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                    /span[@itemprop="author"]/a/span/text()').extract()
                paper_author=[(url,name) for url,name in zip(paper_author_url,paper_author_name)]

                title=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                    /span[@itemprop="name"]/text()').extract()[0]
                item=PaperItem()
                item['PaperDetail']=paper_xml_link
                item['Papertitle']=title
                item['PaperAuthors']=paper_author
                item['Papersub']=[]
                item['PaperConfurlID']=response.url

                self.logger.info("Finished Paper {} \n title {} ".format(paper_xml_link,title))
                yield item
        elif len(Selectors)>1:
            selectors=Selectors[1:]
            headers=response.xpath('//header[position()>1]/h2/text()').extract()
            for i,bse in enumerate(selectors):
                if i<len(headers):
                    subject=headers[i]
                else:
                    subject=""
                paper_selectors=bse.xpath('./li[@class="entry inproceedings"]')
                for pse in paper_selectors:
                    paper_xml_link=pse.xpath('./nav/ul/li[2]/div[2]/ul[1]/li[last()]/a/@href')\
                        .extract()[0]
                    paper_author_url=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                        /span[@itemprop="author"]/a/@href').extract()
                    paper_author_name=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                        /span[@itemprop="author"]/a/span/text()').extract()
                    paper_author=[(url,name) for url,name in zip(paper_author_url,paper_author_name)]

                    title=pse.xpath('./cite[@class="data" and @itemprop="headline"]\
                        /span[@itemprop="name"]/text()').extract()[0]
                    item=PaperItem()
                    item['PaperDetail']=paper_xml_link
                    item['Papertitle']=title
                    item['PaperAuthors']=paper_author
                    item['Papersub']=subject
                    item['PaperConfurlID']=response.url

                    self.logger.info("Finished Paper {} \n title {} ".format(paper_xml_link,title))
                    yield item
            