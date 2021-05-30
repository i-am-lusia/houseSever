"""
@creater: 2021/5/29 19:16
@author: lusia
@lastupdate: 2021/5/30 16:18
@lastauthor: lusia
@description: " 今日份营业请查收~ "
"""
import warnings

from bs4 import BeautifulSoup
import pymysql


class Parser():
    """ 解析页面 """

    def getErShouFangData(self, html, provice):
        """ 解析二手房页面 """
        if html is None:
            print("解析二手房页面为空")
            return

        btSoup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

        block = btSoup.findAll("div", {"class": "info clear"})
        if block is None or len(block) == 0:
            print("当前解析页面无二手房block信息！")
            return

        # 标题
        blockTitle = "null"
        # 必看好房
        isMust = False
        # 定位信息
        blockPosition = []
        # 房屋信息
        houseInfo = "null"
        # 关注信息
        follow = "null"
        # 近地铁
        subway = False
        # vr看装修
        isVrFutureHome = False
        # 满2年
        five = False
        # 满5年
        taxfree = False
        # 随时看房
        haskey = False
        # vr 看房
        vr = False

        for item in block:
            # 1、获取指定标签
            title = item.find("div", {"class": "title"}).find("a")
            must = item.find("div", {"class": "title"}).find("span")
            position = item.find("div", {"class": "flood"}).find("div", {"class": "positionInfo"}).findAll("a")
            houseType = item.find("div", {"class": "address"}).find("div", {"class": "houseInfo"})
            followInfo = item.find("div", {"class": "followInfo"})
            tags = item.find("div", {"class": "tag"}).findAll("span")

            # 2、根据标签获取相应值
            # 获取标题
            if title is not None:
                blockTitle = title.get_text()
            else:
                print("当前解析模板无标题标签")

            # 是否为必看好房
            if must is not None and must.get_text() == "必看好房":
                isMust = True
            else:
                print("当前解析模板无必看好房标签")

            # 获取定位信息
            blockPosition = []
            if position is not None and len(position) != 0:
                for i in position:
                    blockPosition.append(i.get_text())
            else:
                print("当前解析模板无定位信息")

            # 获取当前房屋类型信息
            if houseType is not None:
                houseInfo = houseType.get_text()
            else:
                print("当前解析模块无房型信息")

            # 获取当前房屋关注信息
            if followInfo is not None:
                follow = followInfo.get_text()
            else:
                print("当前解析模块房屋关注信息")

            # tag标签
            if tags is not None and len(tags) != 0:
                for i in tags:
                    tag = i.get_text()
                    if tag == '近地铁':
                        subway = True
                    elif tag == "VR看装修":
                        isVrFutureHome = True
                    elif tag == "VR房源":
                        vr = True
                    elif tag == "房本满二年":
                        five = True
                    elif tag == "房本满五年":
                        taxfree = True
            else:
                print("当前解析模板无tags")

            self.insertData(blockTitle, blockPosition, houseInfo, follow, isMust, subway, isVrFutureHome, five, vr,
                            taxfree,
                            haskey, provice)

    def insertData(self, title, position, houseInfo, follow, isMust, subway, isVrFutureHome, five, vr, taxfree, haskey,
                   provice):
        """ 将爬取的数据存入数据库 """
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='houseMessage',
            charset='utf8'
        )
        cursor = db.cursor()
        sql = " INSERT INTO houseIntroductionMap" \
              " ( place, area, title, isMust, subway, " \
              "isVrFutureHome, five, taxfree, haskey, vr," \
              " follow, house, proviceEng )" \
              " VALUES ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"," \
              " \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\") " % \
              (position[1], position[0], title, int(isMust), int(subway),
               int(isVrFutureHome), int(five), int(taxfree), int(haskey), int(vr),
               follow, houseInfo, provice)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
        print("数据导入数据库成功")
        db.close()
