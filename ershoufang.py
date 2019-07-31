# -*- coding:utf-8 -*-
import requests
from lxml import etree
import re
import csv


class Spider(object):
    def __init__(self):
        self.url = 'https://dl.ke.com/ershoufang/{}/pg{}y1y2/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }

    def response(self, url):
        response = requests.get(url=url, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def parse(self, response, write):
        tree = etree.HTML(response)
        title = tree.xpath('//ul[@class="sellListContent"]//li[@class="clear"]/div[@class="info clear"]/div/a/text()')
        address = tree.xpath(
            '//ul[@class="sellListContent"]//div[@class="info clear"]//div[@class="positionInfo"]/a/text()')  # 有空值
        content = tree.xpath(
            '//ul[@class="sellListContent"]//div[@class="info clear"]//div[@class="houseInfo"]/text()')  # 有空值
        gzl = tree.xpath(
            '//ul[@class="sellListContent"]//div[@class="info clear"]//div[@class="followInfo"]/text()')  # 有空值
        x_pr = tree.xpath(
            '//ul[@class="sellListContent"]//div[@class="info clear"]//div[@class="totalPrice"]/span/text()')
        s_pr = tree.xpath(
            '//ul[@class="sellListContent"]//div[@class="info clear"]//div[@class="unitPrice"]/span/text()')
        new_content = []
        new_gzl = []
        for i in range(1, len(content), 2):
            new_content.append(content[i])
            new_gzl.append(gzl[i])

        for a, b, c, d, e, f in zip(title, address, new_content, new_gzl, x_pr, s_pr):
            write.writerow([a, b, re.sub('|\n', '', c), re.sub(' |\n', '', d), e, f])

    def crawl(self, url, write):
        response = self.response(url)
        self.parse(response, write)

    def main(self):
        address_list = ['shahekou', 'zhongshan', 'xigang', 'gaoxinyuanqu', 'ganjingzi']
        key = ['标题', '小区', '详情', '关注量', '总价(万)', '每平方米价格']
        for address in address_list:
            with open('{}.csv'.format(address), 'a', newline='') as fp:
                write = csv.writer(fp)
                write.writerow(key)
                print('现在爬取%s的二手房信息' % address)
                flag = eval(input("是否继续爬取，继续输入1，跳过该区域的爬取输入0"))
                if flag == 1:
                    page_max = eval(input("请输入爬取的页数"))
                    for page in range(1, page_max + 1):
                        new_url = self.url.format(address, page)
                        self.crawl(new_url, write)
                        print('第%s页爬取完成' % page)
                    print('已完成%s爬取' % address)
                    print('\n')
                elif flag == 0:
                    continue
