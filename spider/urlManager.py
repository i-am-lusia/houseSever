"""
@creater: 2021/5/29 19:16
@author: lusia
@lastupdate: 2021/5/29 19:16
@lastauthor: lusia
@description: " 今日份营业请查收~ "
"""

class UrlManager():
    """ 初始化属性 """

    def __init__(self):
        self.newUrls = set()
        self.oldUrls = set()

    """ 单个添加新的url """

    def addNewUrl(self, url):
        if url is None:
            print("当前url为空")
            return
        if url not in self.newUrls and url not in self.oldUrls:
            self.newUrls.add(url)

    """ 批量添加新的url """

    def addNewUrls(self, urls):
        if urls is None or len(urls) == 0:
            print("当前urls集为空")
            return
        for url in urls:
            self.addNewUrl(url)

    """ 获取新的url """

    def getNewUrls(self):
        newUrl = self.newUrls.pop()
        self.oldUrls.add(newUrl)
        return newUrl

    """ 判断是否存在新的url """

    def checkNewUrls(self):
        return len(self.newUrls) != 0
