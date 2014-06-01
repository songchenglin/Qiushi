#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
from platform import python_version

class QiuBai:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.url = 'http://www.qiushibaike.com/8hr/page'
    def GetPage(self,PageNum):
        myUrl = self.url + '/' + PageNum
        myResp = urllib2.urlopen(myUrl)
        if myResp == None:
            print 'Can\'t connect to %s' % myUrl
            return None
        myPage = myResp.read()
        myResp.close()
        return myPage
    def GetItems(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<div.*?class="content".*?title="(.*?)">(.*?)</div>',re.S)
        myItems = reObj.findall(unicodePage)
        return myItems
        #self.pages.append(myItems)
        #for item in myItems:
        #    print item[0],item[1]
    def startQiuBai(self):
        while 1:
            page = self.GetPage(str(self.page))
            items = self.GetItems(page)
            for item in items:
                print u'第%d页: ' % self.page ,
                print item[0],item[1]
                usrInput = raw_input()
                if usrInput == 'exit':
                    print 'Exit the program'
                    return None
            self.page += 1
        
__author__ = 'SongChenglin'
if __name__ == '__main__':
    print u"""
==============================================
=
=    * 浏览糗事百科上最热门糗事
=
=    * 开发环境:Python 2.7.6
=
=    * 当前环境:Python %s
=
=    * 回车浏览下一条段子，输入exit退出
=
=    * Author: SongChenglin
=
=    * Mail: songchenglin92@gmail.com
=
=    * Github: github.com/songchenglin
=
==============================================
""" % python_version()
    qiuBai = QiuBai()
    qiuBai.startQiuBai()
