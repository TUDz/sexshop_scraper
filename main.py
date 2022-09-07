from utils import HEADERS
from scrapy import Selector
import pandas as pd
import requests
from cleaning import format_excel

def run():
    url_list = []
    main_URL = []
    names = []
    address = []
    hours = []

    res = requests.get('https://sexshopsnearme.com', headers=HEADERS)
    sel = Selector(text=res.text)

    if sel.xpath("//a[contains(text(), 'Local Guides')]").extract():
        local_guide_url = sel.xpath("//a[contains(text(), 'Local Guides')]/@href").extract_first()
        res = requests.get(local_guide_url, headers=HEADERS)
        sel = Selector(text=res.text)

        flag = True
        while flag:
            if sel.xpath("//h2[contains(a/text(), 'Sex Shops in')]/a/@href").extract():
                url_list = url_list + sel.xpath("//h2[contains(a/text(), 'Sex Shops in')]/a/@href").extract()
                
                if sel.xpath('//a[contains(@class, "next")]'):
                    next_page_link = sel.xpath('//a[contains(@class, "next")]/@href').extract_first()
                    res = requests.get(next_page_link, headers=HEADERS)
                    sel = Selector(text=res.text)
                else:
                    flag = False
        
    for url in url_list:
        print(f'Scrapped URL -> {url}')
        tmp_url = requests.get(url, headers=HEADERS)

        sel = Selector(text=tmp_url.text)
        content_tables = sel.xpath("//table/*/tr")
        for table in content_tables:
            if table.xpath('td[1]/text()').extract_first():
                names.append(table.xpath('td[1]/text()').extract_first())
                address.append(table.xpath('td[2]/text()').extract_first())
                hours.append(table.xpath('td[3]/text()').extract_first())
                main_URL.append(url)
            elif table.xpath('td[1]/a/text()').extract_first():
                names.append(table.xpath('td[1]/a/text()').extract_first())
                address.append(table.xpath('td[2]/text()').extract_first())
                hours.append(table.xpath('td[3]/text()').extract_first())
                main_URL.append(url)
            
    db = pd.DataFrame({
        'URL': main_URL,
        'CITY': '',
        'NAMES': names,
        'ADDRESS': address,
        'HOURS': hours
    })

    tmp = (db['URL'].str.split("-in-", 1, expand=True))
    db['CITY'] = tmp[1]
    db['CITY'] = db['CITY'].str.replace('-',' ')
    db['CITY'] = db['CITY'].str.replace('/','')
    db['CITY'] = db['CITY'].str.title()
        
    ## Format final Excel
    format_excel(db)


if __name__ == "__main__":
    run()