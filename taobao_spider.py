import requests
from lxml import etree
import time
import random
import pandas as pd
"""
    Written by Zijun Xi
    Date: 2019/9/27
"""


class Spider:
    '''京东随机选取100部图书商品每书10条评论爬虫'''
    def __init__(self):
        self.url = None
        self.cookie = 'shshshfpa=1dec07d1-31c1-d395-b409-c19ab27d8de0-1531147936; shshshfpb=2a0eeb4d693334d7e85fb1f8d3f3f4a605b43769f7c217e0621b61bd57; __jdu=1553345717454455955504; mt_xid=V2_52007VwMWVl9aV14ZSR9ZAWIGFlZVXFZeHkwpVAdnBUBVXwtODRlMH0AAZAAWTg1dAF0DTkoIDWcDQFNbWwJSL0oYXA17AhpOXV5DWhhCHFsOZQciUG1YYlMfTx1ZAGQHEmJeX1s%3D; areaId=7; ipLoc-djd=7-420-45534-0; PCSYCityID=CN_410000_410200_410202; user-key=851d3dca-aaa0-47a5-a3d1-b4cba8ea7744; cn=0; unpl=V2_ZzNtbUEAFhF8DRRdfxhaB2JTFFURUREQd18TVitMCw1kCxoJclRCFX0UR1xnGloUZAEZX0dcQxVFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsdWAdlBhZbQlFGEXANQlBzHVgBZgYibUVncyV8D0VXfhlsBFcCIh8WC0ASdwFOUzYZWAFlARdZRFdFEHENQ1B%2fEVgBYwIXbUNnQA%3d%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_2fd584c850734a79b7c43fd3adf9299e|1569598452338; shshshfp=e4692fc09e869eb8a131f9313f907646; __jda=122270672.1553345717454455955504.1553345717.1568709832.1569595855.6; __jdc=122270672; 3AB9D23F7A4B3C9B=6442ZN2AYTQNOA3LG2FNGXFN2RC4IKKFPMBAILZO4XTZ5WF2FIXMLCOGE7W6FUTZKDAQCQTIDOJPYVHFMWGGNPOAAE; shshshsID=acb4d916af2f63ae802589a494d0ac43_58_1569599865122; __jdb=122270672.63.1553345717454455955504|6.1569595855'
        self.data = []
        self.COUNT = 0

    def request(self, url):
        '''请求体'''
        headers = {
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                          '537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
        }
        # proxy = {
        #     'https': '125.123.124.207:9999'
        # }
        resp = requests.get(url, headers=headers)
        resp.encoding = 'gbk'
        return resp.text

    @staticmethod
    def random_id_generator():
        ids = []
        while True:
            rand_id = random.randint(12000001, 12999999)
            if rand_id not in ids:
                ids.append(rand_id)
            if len(ids) == 10000:
                break
        return ids

    @staticmethod
    def clean_comment(comment: str):
        '''清除冗余词汇'''
        comment = comment.replace('使用心得：', '').replace('\xa0', '')
        return comment

    def parse(self, text):
        '''解析网页，抓取所需商品评论数据'''
        html = etree.HTML(text)
        divs = html.xpath("//div[@id='hidcomment']/div[@class='item']")
        for div in divs:
            self.COUNT += 1
            try:
                comment = div.xpath(".//div[@class='comment-content']/text()")[0]
            except Exception as e:
                print(e)
                comment = ''
            info = {
                '商品评论': self.clean_comment(comment)
            }
            self.data.append(info)
            print(info)

    def to_csv(self, filename):
        '''保存数据文件到相对路径'''
        df = pd.DataFrame(self.data)
        df.to_csv(f'{filename}.csv', index_label=None, index=None, encoding='gbk')

    def main(self):
        ids = self.random_id_generator()
        for i, id in enumerate(ids):
            try:
                print(f'-----正在爬取第{i + 1}本图书：{id}的数据-----')
                url = f'https://item.jd.com/{id}.html'
                text = self.request(url)
                self.parse(text)
                print('**************************************')
                print(f'***  当前爬取到的评论总数为：{self.COUNT}  ***')
                print('**************************************')

                assert self.COUNT <= 1000, '爬取的商品评论数超过1000条！'  # 当抓取到商品评论的数量为1k时停止

                time.sleep(random.randint(2, 5))
            except Exception as ex:
                self.to_csv('comment_data')
                print(ex)
        self.to_csv('comment_data')


if __name__ == '__main__':
    spi = Spider()
    spi.main()

