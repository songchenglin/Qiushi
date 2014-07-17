#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
from PIL import Image
from platform import python_version

def ShowImages(path):
    if os.path.isfile(path):
        im = Image.open(path)
        im.show()

class HtmlTools:
    BgnCharToNoneRex = re.compile(r'(\t|\n| |<a.*?>|<img.*?>)')
    EndCharToNoneRex = re.compile(r'<.*?>')
    BgnPartRex = re.compile(r'<p.*?>')
    CharToNewLineRex = re.compile(r'(<br/>|</p>|<tr>|</?div>)')
    CharToNextTabRex = re.compile(r'<td>')
    ReplaceTable = [
        ('&','\"'),
        ]
    def ReplaceChar(self,x):
        x = self.BgnCharToNoneRex.sub('',x)
        x = self.EndCharToNoneRex.sub('',x)
        x = self.BgnPartRex.sub('\n',x)
        x = self.CharToNewLineRex.sub('\n',x)
        x = self.CharToNextTabRex.sub('\t',x)
        for tab in self.ReplaceTable:
            x = x.replace(tab[0],tab[1])
        return x
class QiuBai:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.url = 'http://www.qiushibaike.com/8hr/page'
        self.HtmlTool = HtmlTools()
        self.cache_path = os.path.join(os.getcwd(), 'Cache')
        #print self.cache_path
        if not os.path.isdir(self.cache_path):
            os.makedirs(self.cache_path)
    def GetPage(self,PageNum):
        myUrl = self.url + '/' + PageNum
        myUrlReq = urllib2.Request(myUrl)
        myUrlReq.add_header('User-Agent','Mozilla/4.0')
        try:
            myResp = urllib2.urlopen(myUrlReq)
            myPage = myResp.read()
            myResp.close()
            return myPage
        except:
            print 'Can\'t connect to %s' % myUrl
            return None
    def GetItems(self,page):
        unicodePage = page.decode('utf-8')
        reObj = re.compile(r'<div.*?class="content".*?title="(.*?)">(.*?)</div>',re.S)
        myItems = reObj.findall(unicodePage)
        #self.pages.append(myItems)
        #for item in myItems:
        #    print item[0],item[1],item[2]
        return myItems
    def DownloadImages(self, page, items):
        print u'加载中.........'
        unicodePage = page.decode('utf-8')
        for item in items:
            imgFile = os.path.join(self.cache_path, item[0].replace(':', '-')+'.jpg')
            #print imgFile
            reStr = r'<div class="content" title="%s">.{0,150}</div>\s*<div class="thumb">.*?<img src="(.*?)"' % item[0]
            reResult = re.search(reStr, unicodePage, re.S)
            if reResult is None:
                continue
            imgUrl = reResult.group(1)
            #print imgUrl
            #continue
            myUrlReq = urllib2.Request(imgUrl)
            myUrlReq.add_header('User-Agent','Mozilla/4.0')
            try:
                myResp = urllib2.urlopen(myUrlReq)
                imgData = myResp.read()
                fd = open(imgFile,'wb')
                fd.write(imgData)
                fd.close()
                myResp.close()
            except:
                print 'Download %s failed.' % imgUrl
                pass
    def startQiuBai(self):
        while 1:
            page = self.GetPage(str(self.page))
            items = self.GetItems(page)
            self.DownloadImages(page,items)
            for item in items:
                imgFile = os.path.join(self.cache_path, item[0].replace(':', '-')+'.jpg')
                print u'第%d页: ' % self.page,
                if os.path.isfile(imgFile):
                    print item[0], u' 亲，这条段子有图片，输入任意字符来显示'
                else:
                    print item[0]
                print self.HtmlTool.ReplaceChar(item[1])
                usrInput = raw_input()
                if usrInput == 'exit':
                    print 'Exit the program'
                    return None
                elif usrInput is not '':
                    ShowImages(imgFile)
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
