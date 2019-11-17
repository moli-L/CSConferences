import scrapy
from csconferences.items import ConferenceItem
from csconferences.conf import Conf
import re
import datetime


class ConfSpider_All(scrapy.Spider):
    name = 'conference_all'
    handle_httpstatus_list = [404] 
    base_url = "http://www.allconferences.com/search/index/Category__parent_id:12290/Conference__start_date__from:01-01-2014/showLastConference:1/page:"
    allowed_domains = ["allconferences.com"]

    def start_requests(self):
        self.conf = Conf()
        self.page = self.conf.readValue('page_all')
        self.limit = self.conf.readValue('limit_all')
        self.s_num = 0
        self.f_num = 0
        self.f_page = 0
        self.f_db = 0
        self.err_date = 0
        self.p = re.compile(r"^(?:([A-Z]+)\-{1,2})?([A-Z]{3,30})?\s?(\d{4})?\s?([^_\(]*)(?:\((?:.*\()?([^0-9\-]{2,30})[\-\s]?(\d{4})?.*\)\s*)*(?:[_\-—]*([^\(.]*))?")
        # 重试失败链接
        if(self.page > self.limit):
            errList = list(self.conf.getErrorIndexList("error_index_all"))
            self.conf.emptyErrList('error_index_all')
            for i in errList:
                yield scrapy.Request("http://www.allconferences.com/c/"+i, callback=self.parse_item)
        # 爬取数据
        while(self.page <= self.limit):
            yield scrapy.Request(self.base_url+str(self.page), callback=self.parse)
            self.page += 1

    def parse(self, response):
        if(response.status == 404):
            self.f_page += 1
            print("(PAGE: %s) response (%s)" % (self.page, response.status))
        links = response.xpath('//*[starts-with(@id,"conference")]/div/div[@class="conferenceHead"]/h2/a/@href').getall()
        for next_url in links:
            yield scrapy.Request(next_url, callback=self.parse_item)

    def parse_item(self, response):
        def handleStr(s, default=None):
            return default if s==None or isEmptyStr(s) else s.strip()

        def isEmptyStr(s):
            return s=='' or s.strip()==''

        def mapstr(s):
            return s and s.strip()

        def filterDate(s):
            return 'Event Date' in s or 'End Date' in s or 'Paper Submission' in s

        def formatDate(t):
            return datetime.datetime.strptime(t, r'%b %d, %Y').strftime(r"%Y-%m-%d")

        def parseTitle(title, item):
            # 正则表达式匹配结果共7个匹配项：
            # 1：组织  
            # 2：缩写
            # 3：年份
            # 4：全称
            # 5：缩写  标记2 5不同的(5加strip)，过滤组织、长字段(最长30)
            # 6：年份  标记3 6不同的
            # 7：检索  过滤和缩写相同的
            orgas = ['ACM', 'IEEE', 'SPIE']
            # indexes = ['EI', 'SCOPUS', 'JA', 'IEEE', 'ISI', 'EBSCO']
            r = self.p.match(title)
            if(r):
                (o, ab1, y1, fname, ab2, y2, ix) = r.groups()
                # 组织
                item['organization'] = o if(o in orgas) else ''
                # 缩写
                ab2 = mapstr(ab2)
                if(ab1 and ab2 and ab1 == ab2):
                    item['abbr'] = ab1
                elif(ab1 and ab2 and ab1 != ab2):
                    item['abbr'] = ab1+"|"+ab2
                    item['need_confirm'] = 1
                elif(ab1 and ab1 not in orgas and len(ab1) != 30):
                    item['abbr'] = ab1
                elif(ab2 and ab2 not in orgas and 'EI' not in ab2 and 'IEEE' not in ab2 and 2 < len(ab2) < 30):
                    item['abbr'] = ab2
                else:
                    item['need_confirm'] = 1
                # 年份
                if(y1 and y2 and y1 == y2):
                    item['year'] = y1
                elif(y1 and y2 and y1 != y2):
                    item['need_confirm'] = 1
                elif(y1):
                    item['year'] = y1
                elif(y2):
                    item['year'] = y2
                # 全称
                item['name'] = mapstr(fname)
                # 检索
                if(ix and ix != ab1 and ix != ab2):
                    item['indexes'] = mapstr(ix)
            else:
                item['name'] = title
                item['need_confirm'] = 1
        
        # 解析 缩写+年份 字串
        def parseTuple(str, item):
            if(str and not isEmptyStr(str) and len(str) != 30):
                r = re.match(r'^(\w+)(?:[\s\-]+(\d{4}))?\s*$', str)
                if(r):
                    (x, y) = r.groups()
                    if(item.get('abbr', '') == ''):
                        item['abbr'] = x
                    elif(x != item.get('abbr', '')):
                        item['abbr'] = item['abbr'] + "|" + x
                        item['need_confirm'] = 1
                    # 日期
                    if(not y):
                        return
                    elif(not item.get('year', None)):
                        item['year'] = y
                    elif(item.get('year', None) != y):
                        item['need_confirm'] = 1

        TAG = response.url.split('/')[-1]
        if(response.status == 404):
            self.f_num += 1
            print("(INDEX: %s) response (%s)" % (TAG, response.status))
            self.conf.addErrorIndex('error_index_all', TAG)
        else:
            item = ConferenceItem()
            box = response.xpath('//*[@id="layoutContent"]/div[@class="conference-info"]')
            # 标题
            # (): 括号内是缩写 + 年份(可能没有)
            # 句末 )- , -- , _: 后面是可检索的数据库，_处于句中，不具有此含义
            # 句首 --: 前面是组织，多是ACM,IEEE
            # 目前发现的格式：
            # 1. 缩写 年份 (第几届) 全称_检索
            # 2. (年份：极少数没有) (第几届) 全称 (缩写 年份)--检索
            # 3. 组织--(缩写) 年份 (第几届) 全称 (缩写 年份)--/-检索  (最后是双横或单横)
            # 4. 年份 (第几届) 全称 (缩写 年份)-检索     (这一条可看作上一条少了'组织--')
            # 5. (年份) 全称 (缩写 年份)+     (最后括号里内容可能出现两次)  -- 这种格式比例较高
            # 总的说来，可以划分为：
            # | 组织-- | 缩写 | 年份 | 第几届 全称 | (缩写 年份) | -/--检索
            title = box.xpath('div[1]/h1/text()').get()
            parseTitle(title, item)
            # 简写 + 年份
            abbr = box.xpath('h2/span/text()').get() # 存在以下四种情况：1.None；2.缩写 年份；3.缩写；4.title(占满30个字符)
            parseTuple(abbr, item)
            # 地点
            place = box.xpath('p[2]/a/text()').getall()
            item["address"] = ",".join(list(map(lambda s: s.replace(',',''), filter(lambda s: s.strip()!='' and s.strip()!=',', place))))
            # 关键日期
            d = response.xpath('//*[@id="layoutContent"]/table/tr/td')
            dates = list(filter(filterDate, d.xpath('string(.)').getall()))
            if(len(dates) == 1):
                item['s_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[0]).group(1))
            elif(len(dates) == 2):
                if('Paper Submission' in dates[0] or 'Paper Submission' in dates[1]):
                    self.err_date += 1
                    self.conf.addErrorIndex('ERROR_DATE_ALL', TAG)
                item['s_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[0]).group(1))
                item['e_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[1]).group(1))
            else:
                item['s_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[0]).group(1))
                item['e_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[1]).group(1))
                item['paper_date'] = formatDate(re.search(r"[^:]+:\s*(.{12}).*", dates[2]).group(1))
            if(not item.get('year', None)):
                item['year'] = item['s_date'][:4]
            # 官网
            web = response.xpath("//*[@id='layoutContent']/div[@class='conference-options']/button[2]/@onclick").get()
            temp = re.findall(r".+?'(.+?)'", web)[-1]
            item["website"] = temp if temp.startswith('http') else ''
            # 描述
            des = response.xpath('//*[@id="conferenceDescription"]/div')
            item["description"] = handleStr(des.xpath('string(.)').get(), '')
            yield item

    def savaIndex(self):
        print('【Finish】request Success:%s  Fail:%s  Fail_Page:%s  Fail_DB:%s  ERR_DATE:%s' %  (self.s_num, self.f_num, self.f_page, self.f_db, self.err_date))
        self.conf.writeValue('page_all', self.page)
        self.conf.save()

    def errorIndex(self, index='unknow'):
        self.f_num += 1
        self.f_db += 1

    def successDB(self):
        self.s_num += 1