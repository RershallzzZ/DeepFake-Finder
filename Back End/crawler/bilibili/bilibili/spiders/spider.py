# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
from bilibili.items import BilibiliItem

# 本spider是从关键词搜索出来视频结果，
# 对结果进行一个预处理，包括标题、时长、url、上传时间、爬取时间、上传者。
# 但是不包括 类别、视频本身、哈希、截图和简介。

class SpiderSpider(scrapy.Spider):
	# 由于需要支持关键词搜索和按时间排序 所以需要采用一个命令行的参数 argv
	# 默认排序是在后面添加 '&order=totalrank' 
	# 最新发布是在后面添加 '&order=pubdate'
	# 使用方法为 scrapy crawl spider [-a keyword=deepfakes] [-a order=0] #0为默认  1为按上传时间
	def __init__(self, keyword = None, order = None):
		# 假设默认就是搜索deepfakes并且默认排序

		if keyword != None:
			self.start_urls = ('https://search.bilibili.com/all?keyword=' + str(keyword) + '&from_source=nav_suggest_new').split(' ')

		if order == 1:
			self.start_urls = (self.start_urls[0] + '&order=pubdate').split(' ')
	

	name = 'spider'
	allowed_domains = ['bilibili.com']
	start_urls = ['https://search.bilibili.com/all?keyword=deepfakes&from_source=nav_suggest_new']

	def parse(self, response):
		
		#当前页面的视频信息
		#列表的一个元素是一个视频块 还没有提取的 可以继续使用xpath
		listli = response.xpath("//ul[@class='video-list clearfix']/li")
		for i in range(len(listli)):
			item = BilibiliItem()

			item['title'] = listli[i].xpath(".//a/@title").extract_first()
			item['url'] = 'https://' + listli[i].xpath(".//a/@href").extract_first()[2:]
			item['crawl_time'] = str(datetime.datetime.today())[:19]
			item['duration'] = listli[i].xpath(".//a/div[@class='img']/span[@class='so-imgTag_rb']/text()").extract_first()
			for j in listli[i].xpath(".//span"):
				if j.xpath(".//@title").extract() == ['观看']:
					item['watchtime'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				elif j.xpath(".//@title").extract() == ['上传时间']:
					item['upload_time'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				elif j.xpath(".//@title").extract() == ['up主']:
					item['promulgator'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				else:
					pass

			time.sleep(2)
			#yield item
			yield scrapy.Request(url = item['url'], callback = self.playpage, meta = {'item': item})
			
			

		time.sleep(2)

		#后续的下一页
		pagesnum = len(response.xpath("//ul[@class='pages']/li").extract())
		for i in range(2, pagesnum):
			time.sleep(2)
			yield scrapy.Request(url = (self.start_urls[0] + "&page=" + str(i)), callback = self.parseNextPage)

	def parseNextPage(self, response):

		listli = response.xpath("//ul[@class='video-list clearfix']/li")
		for i in range(len(listli)):
			item = BilibiliItem()

			item['title'] = listli[i].xpath(".//a/@title").extract_first().replace("'", '‘').replace('"', '“')
			item['url'] = 'https://' + listli[i].xpath(".//a/@href").extract_first()[2:]  #又没有加https！
			item['crawl_time'] = str(datetime.datetime.today())[:19]
			item['duration'] = listli[i].xpath(".//a/div[@class='img']/span[@class='so-imgTag_rb']/text()").extract_first()
			for j in listli[i].xpath(".//span"):
				if j.xpath(".//@title").extract() == ['观看']:
					item['watchtime'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				elif j.xpath(".//@title").extract() == ['上传时间']:
					item['upload_time'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				elif j.xpath(".//@title").extract() == ['up主']:
					item['promulgator'] = j.xpath(".//text()").extract()[0].replace(' ','').replace('\n', '')
				else:
					pass

			time.sleep(2)
			#yield item
			#获取详细信息
			yield scrapy.Request(url = item['url'], callback = self.playpage, meta = {'item': item})

	def playpage(self, response):

		time.sleep(2)

		item = response.meta['item']

		category = response.xpath("//div[@class='video-data']/span/a/text()").extract_first()

		if category == '科技':
			item['category'] = category
		elif category == '娱乐':
			item['category'] = category
		else:
			item['category'] = '其他'

		item['introduction'] = str(response.xpath("//div[@class='info open']/text()").extract_first()).replace("'", '’').replace('"', '“')

		yield item
