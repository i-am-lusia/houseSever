"""
@creater: 2021/5/29 19:16
@author: lusia
@lastupdate: 2021/5/29 19:16
@lastauthor: lusia
@description: " 用于往数据库中存放指定的基础数据 "
"""

import xlrd
import pymysql

class BaseData():

    def __init__(self):
        self.provice = []

    def getProviceData(self):
        """ 读取省份Excel表数据 """
        workbook = xlrd.open_workbook('provice.xlsx')
        mySheet = workbook.sheet_by_name('Sheet1')
        for i in range(1, mySheet.nrows):
            self.provice.append({
                'provice': mySheet.row_values(i)[1],
                'proviceEng': mySheet.row_values(i)[3],
                'id': int(mySheet.row_values(i)[4]),
                'city': mySheet.row_values(i)[5],
                'cityEng': mySheet.row_values(i)[6],
            })

    def saveProviceDataToDB(self):
        if len(self.provice) == 0 :
            return
        db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            database='houseMessage',
            charset='utf8'
        )
        cursor = db.cursor()
        for item in self.provice:
            sql = " INSERT INTO proviceMap" \
              " ( id, provice, proviceEng, city, cityEng) " \
              " VALUES ( \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % \
              (dict(item).get('id'), dict(item).get('provice'),dict(item).get('proviceEng'),dict(item).get('city'),dict(item).get('cityEng'))
            try:
                cursor.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
            print("数据导入数据库成功")
        db.close()






if __name__ == "__main__":
    baseData = BaseData()
    baseData.getProviceData()
    baseData.saveProviceDataToDB()