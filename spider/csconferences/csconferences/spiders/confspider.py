import scrapy
from csconferences.items import ConferenceItem
from csconferences.conf import Conf

class ConfSpider(scrapy.Spider):
    name = 'conferences'
    base_url = 'https://www.myhuiban.com/conference/'

    def start_requests(self):
        self.conf = Conf()
        self.index = self.conf.readValue('index')
        yield scrapy.Request(self.base_url+str(self.index))

    def parse(self, response):
        if(response.status == 200):
            item = ConferenceItem()
            page = response.xpath('//*[@id="yw0"]/div[2]/div')
            # 赋值
            head = page.xpath('.//h5/text()').get()
            strs = head.split(':', 1)
            item['name'] = strs[1].strip()
            item['abbr'] = strs[0].split()[0]
            item['year'] = int(strs[0].split()[1])
            item['website'] = page.xpath('.//a/@href').get()
            item['paper_date'] = page.xpath('.//table/tr[1]/td[2]/div/text()').get().strip()
            item['noti_date'] = page.xpath('.//table/tr[2]/td[2]/div/text()').get().strip()
            item['s_date'] = page.xpath('.//table/tr[3]/td[2]/div/text()').get().strip()
            item['address'] = page.xpath('.//table/tr[4]/td[2]/div/text()').get().strip()
            # tags = page.xpath('//*[@id="yw0"]/div[2]/div/div[1]')
            # if(len(tags.xpath('.//span')) > 3):
            #     item['rank_CCF'] = page.xpath('.//div[1]/span[1]').get()
            #     item['rank_CORE'] = page.xpath('.///div[1]/span[2]').get()
            #     item['rank_QUALIS'] = page.xpath('.///div[1]/span[3]').get()
            yield item
            self.index = self.index + 1
            next_url = self.base_url+str(self.index)
            if(self.index <= 10):
                yield scrapy.Request(next_url)
