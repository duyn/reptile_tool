
import requests
import time
from lxml import etree
import xlsxwriter


class Spider(object):
    def __init__(self):
        self.url = "https://bj.zu.ke.com/zufang/pg{}/#contentList"

    def get_html(self, page):
        """获取网站html代码"""
        self.url.format(page)
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers).text
        return response

    def parse_html(self, htmlcode, data):
        """解析html代码"""
        content = etree.HTML(htmlcode)
        results = content.xpath('///div[@class="content__article"]/div[1]/div')
        for result in results[:]:
            community = result.xpath('./div[1]/p[@class="content__list--item--title twoline"]/a/text()')[0].replace('\n',
                                                                                                                    '').strip().split()[
                0]
            address = "-".join(result.xpath('./div/p[@class="content__list--item--des"]/a/text()'))
            landlord = result.xpath('./div/p[@class="content__list--item--brand oneline"]/text()')[0].replace('\n',
                                                                                                              '').strip() if len(
                result.xpath('./div/p[@class="content__list--item--brand oneline"]/text()')) > 0 else ""
            postime = result.xpath('./div/p[@class="content__list--item--time oneline"]/text()')[0]
            introduction = ",".join(result.xpath('./div/p[@class="content__list--item--bottom oneline"]/i/text()'))
            price = result.xpath('./div/span/em/text()')[0]
            description = "".join(result.xpath('./div/p[2]/text()')).replace('\n', '').replace('-', '').strip().split()
            area = description[0]
            count = len(description)
            if count == 6:
                orientation = description[1] + description[2] + description[3] + description[4]
            elif count == 5:
                orientation = description[1] + description[2] + description[3]
            elif count == 4:
                orientation = description[1] + description[2]
            elif count == 3:
                orientation = description[1]
            else:
                orientation = ""
            pattern = description[-1]
            floor = "".join(result.xpath('./div/p[2]/span/text()')[1].replace('\n', '').strip().split()).strip() if len(
                result.xpath('./div/p[2]/span/text()')) > 1 else ""
            date_time = time.strftime("%Y-%m-%d", time.localtime())
            """数据存入字典"""
            data_dict = {
                "community": community,
                "address": address,
                "landlord": landlord,
                "postime": postime,
                "introduction": introduction,
                "price": '￥' + price,
                "area": area,
                "orientation": orientation,
                "pattern": pattern,
                "floor": floor,
                "date_time": date_time
            }
            data.append(data_dict)

    def excel_storage(self, response):
        """将字典数据写入excel"""
        workbook = xlsxwriter.Workbook('./zufangInfo.xlsx')
        worksheet = workbook.add_worksheet()
        """设置标题加粗"""
        bold_format = workbook.add_format({'bold': True})
        worksheet.write('A1', '小区名称', bold_format)
        worksheet.write('B1', '租房地址', bold_format)
        worksheet.write('C1', '房屋来源', bold_format)
        worksheet.write('D1', '发布时间', bold_format)
        worksheet.write('E1', '租房说明', bold_format)
        worksheet.write('F1', '房屋价格', bold_format)
        worksheet.write('G1', '房屋面积', bold_format)
        worksheet.write('H1', '房屋朝向', bold_format)
        worksheet.write('I1', '房屋户型', bold_format)
        worksheet.write('J1', '房屋楼层', bold_format)
        worksheet.write('K1', '查看日期', bold_format)

        row = 1
        col = 0
        for item in response:
            worksheet.write_string(row, col + 0, item['community'])
            worksheet.write_string(row, col + 1, item['address'])
            worksheet.write_string(row, col + 2, item['landlord'])
            worksheet.write_string(row, col + 3, item['postime'])
            worksheet.write_string(row, col + 4, item['introduction'])
            worksheet.write_string(row, col + 5, item['price'])
            worksheet.write_string(row, col + 6, item['area'])
            worksheet.write_string(row, col + 7, item['orientation'])
            worksheet.write_string(row, col + 8, item['pattern'])
            worksheet.write_string(row, col + 9, item['floor'])
            worksheet.write_string(row, col + 10, item['date_time'])
            row += 1
        workbook.close()

    def main(self):
        all_datas = []
        """网站总共100页，循环100次"""
        for page in range(1, 100):
            html = self.get_html(page)
            self.parse_html(html, all_datas)
        self.excel_storage(all_datas)
