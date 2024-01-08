# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
from youtube.items import YoutubeItem
from youtube.settings import pagetable

# 本spider是从关键词搜索出来视频结果，
# 对结果进行一个预处理，包括标题、时长、url、上传时间、爬取时间、上传者。
# 但是不包括 类别、视频本身、哈希、截图和简介。

class YouspiderSpider(scrapy.Spider):

	# 由于需要支持关键词搜索和按时间排序 所以需要采用一个命令行的参数 argv
	# 默认排序是在后面添加 '&order=totalrank' 
	# 最新发布是在后面添加 '&order=pubdate'
	# 使用方法为 scrapy crawl youspider [-a keyword=deepfakes] [-a order=0] #0为默认  1为按上传时间
	def __init__(self, keyword = None, order = None):
		# 假设默认就是搜索deepfakes并且默认排序

		if keyword != None:
			self.start_urls = ('https://www.youtube.com/results?search_query=' + str(keyword)).split(' ')

		if order == 1:
			self.start_urls = (self.start_urls[0] + '&sp=CAI%253D').split(' ') #按上传日期排序

		self.start_urls = (self.start_urls[0] + "&page=" + str(pagetable['data'][0])).split(' ')#添加页面
	

	name = 'youspider'
	allowed_domains = ['youtube.com']
	start_urls = ['https://www.youtube.com/results?search_query=deepfakes']

	def parse(self, response):
		
		#当前页面的视频信息
		#列表的一个元素是一个视频块 还没有提取的 可以继续使用xpath
		links = response.xpath("//a[contains(@href, '/watch?')]")
		for i in range(1, len(links), 2):
			try:
				item = YoutubeItem()
				item['url'] = 'https://www.youtube.com/' + links[i].xpath("@href").extract()[0]
				item['title'] = links[i].xpath("@title").extract()[0]
				item['watchtime'] = links[i].xpath("../../div[@class='yt-lockup-meta ']").xpath("./ul/li")[1].xpath("./text()").extract()[0][:-6]
				item['duration'] = links[i].xpath("../span/text()").extract()[0][13:-1] #去掉每个前面都有的 ' - Duration: 8:42.'

				time.sleep(1)
				#
				yield scrapy.Request(url = item['url'], callback = self.playpage, meta = {'item': item})
			except:
				pass
			

		# 后续页面
		# 连续模式
		if pagetable["model"] == 0:
			for i in range(int(pagetable['data'][0]) + 1, int(pagetable['data'][1]) + 1):
				time.sleep(1)
				yield scrapy.Request(url = self.start_urls[0][:self.start_urls[0].index("&page=")] + "&page=" + str(i), callback = self.parseNextPage)
		else:
			for i in pagetable['data'][1:]:
				time.sleep(1)
				yield scrapy.Request(url = self.start_urls[0][:self.start_urls[0].index("&page=")] + "&page=" + str(i), callback = self.parseNextPage)

			

	def parseNextPage(self, response):

		links = response.xpath("//div[@class='yt-lockup-content']")
		for i in range(len(links)):
			try:
				item = YoutubeItem()
				item['url'] = 'https://www.youtube.com/' + links[i].xpath("./h3/a/@href").extract()[0]
				item['title'] = links[i].xpath("./h3/a/text()").extract()[0]
				item['watchtime'] = links[i].xpath("./div[@class='yt-lockup-meta ']/ul/li/text()").extract()[1][:-6]
				item['promulgator'] = links[i].xpath("./div[@class='yt-lockup-byline ']/a/text()").extract()[0]
				item['duration'] = links[i].xpath("./h3/span/text()").extract()[0][13:-1]
				time.sleep(1)
				#跳过有些是播放列表
				yield scrapy.Request(url = item['url'], callback = self.playpage, meta = {'item': item})
			except:
				pass


	def playpage(self, response):

		time.sleep(1)

		item = response.meta['item']

		try:
			item['upload_time'] = response.xpath("//meta[@itemprop='uploadDate']/@content").extract()[0]
			item['crawl_time'] = str(datetime.datetime.today())[:19]
			item['promulgator'] = response.xpath("//div[@class='yt-user-info']/a/text()").extract()[0]
			
			item['introduction'] = response.xpath("//div[@id='watch-description-text']/p/text()").extract()[0]
			
			rawcategory = response.xpath("//ul[@class='content watch-info-tag-list']/li/a/text()").extract()[0] #挂了代理访问的，多半结果会是英文的

			if ('Technology' in rawcategory) or ('科技' in rawcategory):
				item['category'] = '科技'
			elif ('娱乐' in rawcategory) or ('Entertainment' in rawcategory):
				item['category'] = '娱乐'
			elif ('Politics' in rawcategory) or ('政治' in rawcategory):
				item['category'] = '政治'
			else:
				item['category'] = '其他'
		
			yield item
			
		except:
			pass
			
