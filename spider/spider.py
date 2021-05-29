"""
@creater: 2021/5/29 19:16
@author: lusia
@lastupdate: 2021/5/29 19:16
@lastauthor: lusia
@description: " 今日份营业请查收~ "
"""

from urlManager import UrlManager
import pymysql


class Spider():

    def __init__(self):
        """ 构造函数,初始化属性 """
        self.urls = UrlManager()
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

    def setUrl(self, type):
        """
            拼接爬取的目标地址
            type为判断房的性质类型
            0二手房 1新房 2租房 3海外 4商业办公 5小区
            目前仅支持二手房

        """
        typeUrl = ''
        if type == 0: typeUrl='ershoufang/'
        for item in self.cityList:
            for num in range (1, 101):
                url = 'https://' + dict(item).get('provice') + '.lianjia.com/' + typeUrl + dict(item).get('city') + '/pg' + str(num) + '/'
                print("拼接目标地址:" + url)



if __name__ == "__main__":
    spider = Spider()
    spider.getProviceCityName()
    spider.setUrl(0)