# -*- coding:utf-8 -*-
import re
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Spider(object):
	def __init__(self):
		# self.my_url = "http://www.pm25.com/news.html"
		self.my_url = "http://www.cpnn.com.cn/"
		self.data = []
		self.reg_list = []
		self.reg_list.append(u"<li><a href='(.*?)' title='(.*?)'><img src=(.*?) Border=0  width=455 height=300 ></a></li>")
		# self.reg_list.append(u'<li><a href="http://www.pm25.com/news(.*?)".*?><i>•</i>(.*?)</a></li>')

	def getHtml(self):
		url = self.my_url
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
		}
		req = urllib2.Request(url=url, headers=headers)
		print url
		try:
			htmlValue = urllib2.urlopen(req).read()
		except Exception, e:
			print "faild to get the value in page code " + str(e)
			return ""
		# print htmlValue
		return htmlValue

	def findData(self, htmlValue):
		print "XXXXXXXXXX"
		data_items = re.findall(self.reg_list[0], htmlValue, re.S)
		print data_items
		fileHandle = open('test.txt', 'w')
		idx = 0
		for item in data_items:
			tmp = {}
			if idx < 5:
				link_ = 'http://www.cpnn.com.cn' + str(item[0])[1:len(str(item[0]))]
			idx += 1
			img_ = 'http://www.cpnn.com.cn' + str(item[2])[2:len(str(item[2]))-1]
			tmp["link"] = link_
			tmp["title"] = str(item[1])
			tmp["img"] = img_
			self.data.append(tmp)
			fileHandle.write(link_ + '\n')
			fileHandle.write(str(item[1]) + '\n')
			fileHandle.write(img_ + '\n')
			print tmp
		print len(self.data)
		# fileHandle.close()


def main():
	spider = Spider()
	htmlValue = spider.getHtml()
	spider.findData(htmlValue)


if __name__ == '__main__':
	main()
