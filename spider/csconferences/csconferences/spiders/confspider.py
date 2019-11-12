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
        item = ConferenceItem()
        page = response.xpath('//*[@id="yw0"]/div[2]/div')
        # 赋值
        head = page.xpath('.//h5/text()').get()
        strs = head.split(':', 1)
        item['name'] = strs[1].strip()
        item['abbr'] = strs[0].split()[0]
        item['year'] = int(strs[0].split()[1])
        item['website'] = page.xpath('.//a/@href').get()
        item['paper_date'] = page.xpath(
            './/table/tr[1]/td[2]/div/text()').get().strip()
        item['noti_date'] = page.xpath(
            './/table/tr[2]/td[2]/div/text()').get().strip()
        item['s_date'] = page.xpath(
            './/table/tr[3]/td[2]/div/text()').get().strip()
        item['address'] = page.xpath(
            './/table/tr[4]/td[2]/div/text()').get().strip()
        tags = response.xpath('//*[@id="yw0"]/div[2]/div/div[1]/span')

        def mapstr(s):
            return s.strip()[:-1]

        def filterstr(s):
            return s == 'CCF' or s == 'CORE' or s == 'QUALIS'

        # 如果有评级
        if(len(tags) > 3):
            labels = list(map(mapstr, response.xpath(
                '//*[@id="yw0"]/div[2]/div/div[1]/text()').getall()))
            labs = list(filter(filterstr, labels))
            for i, val in enumerate(labs):
                if(val == 'CCF'):
                    item['rank_CCF'] = page.xpath(
                        './/div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()
                elif(val == 'CORE'):
                    item['rank_CORE'] = page.xpath(
                        './/div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()
                elif(val == 'QUALIS'):
                    item['rank_QUALIS'] = page.xpath(
                        './/div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()

        yield item
        self.index = self.index + 1
        next_url = self.base_url+str(self.index)
        yield scrapy.Request(next_url)
