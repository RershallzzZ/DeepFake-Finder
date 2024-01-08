#-*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

import logging

import table

class getScreenshot(object):
	"""docstring for getScreenshot"""
	def __init__(self):

		logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.logger = logging.getLogger(__name__)


		#设置浏览器
		self.setBrowser()

	def setBrowser(self):
		#浏览器部分

		try:
			self.browser = webdriver.Chrome()
		except:
			self.logger.error("启动浏览器失败...")
			exit(0)
		self.browser.maximize_window()
		self.logger.info("浏览器创建成功...")

	def quit0(self):
		"""退出函数"""
		try:
			self.browser.close()
			self.browser.quit()
		except:
			self.logger.error("关闭浏览器失败...")


	
	def dealDB(self):
		"""从数据库中读取数据，进行简单的处理"""

		self.logger.info("正在从数据库中获取需要的信息...")

		#从数据库中获取信息
		while True:
			with table.get_session() as s:
				movie = s.query(table.Movie).filter_by(screenshot_path = None).first()
				if movie == None:
					break
				#15列数据 一行是一条记录

				
				#将url进行访问，返回一个字典包含信息
				try:
					self.getInfo(id0 = movie.id, url = movie.url)
				except Exception as e:
					self.logger.error("getInfo()出错")
					self.logger.error(e)
					self.logger.info("一般这个地方出错是由于网络或者其他原因导致浏览器加载不成功是的js获取失败...")
					continue

				movie.screenshot_path = f"screenshot/bilibili/{movie.id}.png"
				# 提交
				s.commit()
				self.logger.info(f'url={movie.url}快照提交成功...')
				


		self.quit0()

	def getInfo(self, id0, url):
		"""在浏览器中输入网址，获取信息"""

		self.logger.info("正在获取url='" + url + "'的快照...")

		try:
			self.browser.get(url)
			
		except:
			self.logger.error("建立连接失败...")
			exit(0)

		#这个值应该根据网速来进行调整
		time.sleep(4)
		
		self.browser.save_screenshot('../../../screenshot/bilibili/' + str(id0) + '.png')

if __name__ == '__main__':

	getscreenshot = getScreenshot()

	getscreenshot.dealDB()