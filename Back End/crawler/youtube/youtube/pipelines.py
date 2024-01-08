# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from youtube.items import YoutubeItem
import youtube.table as table

class YoutubePipeline(object):
	def process_item(self, item, spider):
		with table.get_session() as s:
			#当前视频在数据库中已经有了就不用插了。
			if s.query(table.Movie).filter(f'{table.Movie.__tablename__}.url' == item['url']).first() == None:
				movie = table.Movie(url = item['url'], download = 0, analyzed = 0, title = item['title'], crawl_time = item['crawl_time'], watchtime = item['watchtime'], upload_time = item['upload_time'], promulgator = item['promulgator'], duration = item['duration'], introduction = item['introduction'], category = item['category'])
				s.add(movie)
				s.commit()

		return item