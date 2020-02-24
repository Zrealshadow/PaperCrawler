import scrapy
from PaperCrawler.items import DataAboutPaper

class PaperCrawler(scrapy.Spider):
    name='ArXiv'
    start_urls=["https://arxiv.org/archive/cs"]
    offset_years=2
    years=2
    org_url='https://arxiv.org'
    offset_max_page=4
    ONEPAGEPAPERS=25
    # 25 papers in one page
    def __init__(self,category=None,*args,**kwargs):
        super(PaperCrawler,self).__init__(*args,**kwargs)


    def parse(self,response):
        years_links=response.xpath('/html/body/main/div//ul[1]/li[last()]//a/@href').extract()
        static_links=[self.org_url+i for i in years_links]
        cnt=0
        for i,l in enumerate(static_links):
            if i>=self.offset_years and cnt<self.years:
                self.logger.info("Parse Year {} from now, url:{}".format(i,l))
                yield scrapy.Request(l,callback=self.parse_year)
                cnt+=1
            else:
                continue
    
    def parse_year(self,response):
        main_links=response.xpath('/html/body/div/ul[1]/li/a[1]/@href').extract()
        paper_num=[ int(i) for i in response.xpath('/html/body/div/ul[1]/li/b/text()').extract()]
        crosslisting_num=[ int(i) for i in response.xpath('/html/body/div/ul[1]/li/i/text()').extract()]
        max_paper_num_list=[ i[0]+i[1] for i in zip(crosslisting_num,paper_num)]
        pageurls=[]
        for main_link,max_paper_num in zip(main_links,max_paper_num_list):
            offset_page=1
            pageurls.append(self.org_url+main_link)
            while offset_page<self.offset_max_page and offset_page*self.ONEPAGEPAPERS<max_paper_num:
                page_url=self.org_url+main_link+"skip="+str(offset_page*self.ONEPAGEPAPERS)+"&show=25"
                self.logger.info("Create Page Url {}".format(page_url))
                pageurls.append(page_url)
                offset_page+=1

        # self.logger.info("\n\n the pageurls type {}\n{} ".format(type(pageurls),pageurls))

        for url in pageurls:
            self.logger.info('Parse all pages url {},type(url),{}'.format(url,type(url)))
            yield scrapy.Request(url,callback=self.parse_page)
            

    def parse_page(self,response):
        links=response.xpath('//dt/span/a[1]/@href').extract()
        static_links=[self.org_url+i for i in links]
        for l in static_links:
            self.logger.info('Parse one Page url {}'.format(l))
            yield scrapy.Request(l,callback=self.parse_paper)

    def parse_paper(self,response):
        item=DataAboutPaper()
        item['abstract']=response.xpath('//blockquote/text()').extract()
        item['authors']=response.xpath('//div[@class="authors"]/a/text()').extract()
        item['pdfurl']=self.org_url+response.xpath('//div[@class="full-text"]/ul/li[1]/a/@href')\
            .extract()[0]
        item['main_subject']=response.xpath("//td[@class='tablecell subjects']/span/text()")\
            .extract()[0].split('(')[0].rstrip()
        rsubject=response.xpath("//td[@class='tablecell subjects']/text()").extract()
        if len(rsubject)>1:
            rsubject=rsubject[1].split(';')[1:]
        item['related_subject']=[sub.split('(')[0].rstrip().lstrip() for sub in rsubject]
        item['timestamp']=response.xpath('//div[@class="submission-history"]/text()').extract()[-1].strip('\n')
        ##
        i=DataAboutPaper()
        i['abstract']='ererere'
        i['pdfurl']='cccc'
        item['it']=i
        self.logger.info('Finishing Parsing one Page,Return item')
        yield item




