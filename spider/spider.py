"""
@creater: 2021/5/29 19:16
@author: lusia
@lastupdate: 2021/5/29 19:16
@lastauthor: lusia
@description: " 今日份营业请查收~ "
"""

from downloader import Downloader
from parser import Parser
import pymysql


class Spider():

    def __init__(self):
        """ 构造函数,初始化属性 """
        self.downloader = Downloader()
        self.parser = Parser()
        self.cityList = []

    def getProviceCityName(self):
        """ 获取地址 """
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='houseMessage',
            charset='utf8'
        )
        cursor = db.cursor()
        sql = " SELECT * FROM proviceMap"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                provice = row[5]
                city = row[6]
                self.cityList.append({'provice': provice, 'city': city})
        except:
            print("Error: unable dataBase")
        db.close()

    def crawErShouFang(self):
        """ 爬取二手房 """
        typeUrl = 'ershoufang/'
        for item in self.cityList:
            for num in range(1, 101):
                # 1、 拼接地址
                url = 'https://' + dict(item).get('provice') + '.lianjia.com/' + typeUrl + dict(item).get(
                    'city') + '/pg' + str(num) + '/'
                print("拼接目标地址:" + url)
                # 2、 下载目标地址页面
                try:
                    html = self.downloader.downloader(url, dict(item).get('provice'))
                except Exception as e:
                    print("下载页面异常：" + e)
                # 3、 解析地址
                else:
                    try:
                        self.parser.getErShouFangData(html, dict(item).get('provice'))
                    except Exception as e:
                        print("解析页面错误" + e)
                    else:
                        print("解析页面成功：" + url)


if __name__ == "__main__":
    spider = Spider()
    spider.getProviceCityName()
    spider.crawErShouFang()
