import scrapy
from csconferences.items import ConferenceItem
from csconferences.conf import Conf


class ConfSpider(scrapy.Spider):
    name = 'conference_hb'
    handle_httpstatus_list = [404, 500] 
    base_url = 'https://www.myhuiban.com/conference/'
    allowed_domains = ["myhuiban.com"]

    def start_requests(self):
        self.conf = Conf()
        self.index = self.conf.readValue('index_hb')
        self.limit = self.conf.readValue('limit_hb')
        self.s_num = 0
        self.f_num = 0
        while(self.index <= self.limit):
            yield scrapy.Request(self.base_url+str(self.index))
            self.index += 1

    def parse(self, response):
        def handleStr(s, default=None):
            return default if s==None or isEmptyStr(s) else s.strip()

        def isEmptyStr(s):
            return s=='' or s.strip()==''

        # 去掉空格和最后一个字符
        def mapstr(s):
            return s.strip()[:-1]

        def filterstr(s):
            return s == 'CCF' or s == 'CORE' or s == 'QUALIS'
        
        if(response.status == 404 or response.status == 500):
            self.f_num += 1
            print("(INDEX: %s) response (%s)" % (self.index, response.status))
        else:
            item = ConferenceItem()
            page = response.xpath('//*[@id="yw0"]/div[2]/div')
            # 赋值
            head = page.xpath('.//h5/text()').get()
            strs = head.split(':', 1)
            item['name'] = handleStr(strs[1], '')
            s=strs[0].split()
            item['abbr'] = ' '.join(s[:-1])
            item['year'] = int(s[-1])
            item['website'] = handleStr(page.xpath('.//a/@href').get(), '')
            item['paper_date'] = handleStr(page.xpath('.//table/tr[1]/td[2]/div/text()').get())
            item['noti_date'] = handleStr(page.xpath('.//table/tr[2]/td[2]/div/text()').get())
            item['s_date'] = handleStr(page.xpath('.//table/tr[3]/td[2]/div/text()').get())
            item['address'] = handleStr(page.xpath('.//table/tr[4]/td[2]/div/text()').get(), '')
            tags = response.xpath('//*[@id="yw0"]/div[2]/div/div[1]/span')
            # 如果有评级
            if(len(tags) > 3):
                labs = list(filter(filterstr, map(mapstr, response.xpath('//*[@id="yw0"]/div[2]/div/div[1]/text()').getall())))
                for i, val in enumerate(labs):
                    if(val == 'CCF'):
                        item['rank_CCF'] = page.xpath('.//div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()
                    elif(val == 'CORE'):
                        item['rank_CORE'] = page.xpath('.//div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()
                    elif(val == 'QUALIS'):
                        item['rank_QUALIS'] = page.xpath('.//div[@class="hidden-phone"]/span[%s]/text()' % (i+1)).get()
            yield item

    def savaIndex(self):
        print('【Finish】request Success:%s  Fail:%s' %  (self.s_num, self.f_num))
        self.conf.writeValue('index', self.index)

    def errorIndex(self, index='unknow'):
        self.f_num += 1
        self.conf.addErrorIndex("error_index_hb", index)

    def successDB(self):
        self.s_num += 1