import scrapy
import json
from scrapy.crawler import CrawlerProcess
import pandas as pd

def make_headers(Header_String, Separator=': ', strip_cookie=True, strip_cl=True, Stripped_Headers: list = []) -> dict:
    Temp_Header = dict()
    for i in Header_String.split('\n'):
        i = i.strip()
        if i and Separator in i:
            j = ''
            k = i.split(Separator)[0]
            if len(i.split(Separator)) == 1:
                j = ''
            else:
                j = i.split(Separator)[1]
            if k[:1] == ":":
                continue
            if strip_cookie and k.lower() == 'cookie':
                continue
            if strip_cl and k.lower() == 'content-length':
                continue
            if k in Stripped_Headers:
                continue
            Temp_Header[k] = j
    return Temp_Header


class CodeSpider(scrapy.Spider):
    name = 'code'
    custom_settings = {
    "FEEDS":{"ND_Crawl.csv" : {"format" : "csv", "overwrite":False}}}
    main_data = []
    headers = """accept: */*
    accept-encoding: gzip, deflate, br
    accept-language: en-US,en;q=0.9
    authorization: undefined
    cache-control: no-cache
    content-length: 66
    content-type: application/json
    cookie: ASP.NET_SessionId=lnxrdmxv4u4orl2visytqxsx
    origin: https://firststop.sos.nd.gov
    pragma: no-cache
    referer: https://firststop.sos.nd.gov/search/business
    sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    sec-fetch-dest: empty
    sec-fetch-mode: cors
    sec-fetch-site: same-origin
    user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"""
    headers = make_headers(headers,strip_cookie=False)
    
    def start_requests(self): 
        form_data = {"SEARCH_VALUE":"X","STARTS_WITH_YN":True,"ACTIVE_ONLY_YN":True}
        request_body = json.dumps(form_data)
        yield scrapy.Request('https://firststop.sos.nd.gov/api/Records/businesssearch',
                            method="POST",
                            body=request_body,
                            headers=self.headers,callback=self.parse )

    def parse(self, response):
        for Business_UID,data in response.json()['rows'].items():
            data['TITLE'] = ' | '.join(data['TITLE'])
            yield scrapy.Request(f'https://firststop.sos.nd.gov/api/FilingDetail/business/{Business_UID}/false',headers=self.headers,callback=self.parse_each_business,cb_kwargs=data)
            
        
    def parse_each_business(self,response,**kwargs):
        data = kwargs
    
        columns = 'Filing Type,Status,Standing - AR,Standing - RA,Standing - Other,Formed In,Term of Duration,Initial Filing Date,Principal Address,Mailing Address,AR Due Date,Commercial Registered Agent,Delayed Effective Date,Registered Agent,Filing Subtype,Owner Name,Owner Address,Nature of Business,Expiration Date,Owners'.split(',')
        for col in columns:
            data[col] = None
        for row in response.json()['DRAWER_DETAIL_LIST']:
            data[row['LABEL']] = row['VALUE']
            
        yield data
            
            
process = CrawlerProcess()
process.crawl(CodeSpider)
process.start()
