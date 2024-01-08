#-*-coding:utf-8-*-

# 尚未解决的问题 如何把每个爬虫需要爬取的页面传递给它呢？
# 要不然就还是一个start 一个end 就不要离散模式了

from scrapyd_api import ScrapydAPI
import tablespider as table

# flask 部分，整合的时候应该删掉这部分而与前端的后端已经有的falsk进行整合
from flask import Flask, request, jsonify
import json
app = Flask(__name__)

# 路由到创建爬虫
@app.route("/deepfake-finder/monitorengine/crawler", methods = ['POST'])
def CreateSpider():

	data = json.loads(request.get_data(as_text=True))

	if data['url'] == '':
		return jsonify({"code": 400, "data": "新增爬虫失败, url是必须的"})

	spider = createSpider(url = data['url'], keyword = data['keyword'], time = data['time'], start = data['start'], end = data['end'])

	if spider != {}:
		return jsonify({"code": 20000, "data": f"新增爬虫成功, 该爬虫的id为{spider['id']}"})
	else:
		return jsonify({"code": 400, "data": "新增爬虫失败"})


# 路由到依据keyword 和 time 获取爬虫列表
@app.route("/deepfake-finder/monitorengine/crawler/list/search", methods = ['POST'])
def SpiderList():
	
	data = json.loads(request.get_data(as_text=True))
	spiders = spiderList(data['keyword'], data['time'])
	
	senddata = {}
	senddata['code'] = 20000
	senddata['data'] = {}
	senddata['data']['crawlerList'] = []

	for spider in spiders:
		t_spider = {}
		t_spider['id'] = spider['id']
		t_spider['url'] = spider['url']
		t_spider['keyword'] = spider['keyword']
		t_spider['time'] = spider['time']
		t_spider['start'] = spider['start']
		t_spider['end'] = spider['end']
		t_spider['jobid'] = spider['jobid']

		senddata['data']['crawlerList'].append(t_spider)

	return json.dumps(senddata)



# 通过id获取某个爬虫的信息
@app.route("/deepfake-finder/monitorengine/crawler", methods = ['GET'])
def ReturnSpider():

	id0 = request.args.get("id")
	spider = returnSpider(id0)

	if spider == {}:
		return json.dumps({"code":400, "data": "不存在该爬虫"})

	senddata = {}
	senddata['code'] = 20000
	senddata['data'] = spider

	return json.dumps(senddata)



# 通过id更新某个爬虫的参数 就post吧 
@app.route("/deepfake-finder/monitorengine/crawler/update", methods = ['POST'])
def UpdateSpider():
	
	data = json.loads(request.get_data(as_text=True))

	spider = updateSpider(data['id'], data['url'], data['keyword'], data['time'], data['start'], data['end'])

	if spider != {}:
		return jsonify({"code": 20000, "data": f"新增爬虫成功, id = {spider['id']}"})
	else:
		return jsonify({"code": 400, "data": "新增爬虫失败"})



# 通过id删除某个爬虫 就post吧
@app.route("/deepfake-finder/monitorengine/crawler/delete", methods = ['POST'])
def DropSpider():
	
	data = json.loads(request.get_data(as_text=True))

	if dropSpider(data['id']):
		return jsonify({"code": 20000, "data": "删除爬虫成功"})
	else:
		return jsonify({"code": 400, "data": "删除爬虫失败"})



# 启动/暂停/停止 爬虫 级post吧
# 传入的数据就是 开启 暂停 关闭
@app.route("/deepfake-finder/monitorengine/crawler/state", methods = ['POST'])
def ChangeSpider():
	
	data = json.loads(request.get_data(as_text=True))

	## 改变状态有多种情况，同时 状态不是直接就能修改的 而是要从爬虫服务器进行请求的
	# 有原来是未开始的 现在给启动
	# 有原来是启动的 现在暂停(停止)
	# 有排队等待的 现在暂停(停止)
	# 运行结束的 再启动没有意义 不予启动
	# 暂停中的 现在就启动
	# 原来是什么状态的 现在进行修改为相同状态 直接pass 
	## 

	# 先通过id 获得爬虫
	spider = returnSpider(data['id']) 

	if spider == {}:
		return jsonify({"code": 400, "data": "no该爬虫不存在"})

	if data['state'] == '开启':
		backstate = startSpider(data['id'])
	elif data['state'] == '暂停' or data['state'] == '关闭':
		backstate = stopSpider(data['id'])

	if backstate == False:
		return jsonify({"code": 400, "data": "fu 修改爬虫失败"})

	return jsonify({"code": 20000, "data": "修改爬虫成功"})




### =============================================
#
# 以下代码式真实和远端爬虫服务器交互和数据库交互的部分
#
### =============================================


# 读取部署爬虫服务器的配置
with open('./config.json', 'r') as f:
    config = json.loads(f.read())['crawlServer']

scrapyd = ScrapydAPI(f"http://{config['ip']}:{config['port']}")

# 创建一个爬虫 并放入数据库中, 返回一个spider spider是字典
def createSpider(url, keyword, time, start = '', end = ''):

	if url == '':
		return {}

	# 插入到数据库中
	try:
		with table.get_session() as s:
			newspider = table.SPIDER(url = url, order = (0 if time == '' else time), keyword = keyword, state = 0, jobid = '', start = start, end = end)
			s.add(newspider)
			s.flush()

			newspiderid = newspider.id
			newspider.recording = 'recording/spider' + str(newspiderid)

			newspider.name = ('youspider' if 'youtube' in url else 'bispider')
			s.add(newspider)

			spider = {}
			spider['id'] = newspider.id
			spider['url'] = newspider.url
			spider['keyword'] = newspider.keyword
			spider['time'] = newspider.order
			spider['jobid'] = newspider.jobid
			spider['state'] = newspider.state
			spider['name'] = newspider.name
			spider['start'] = newspider.start
			spider['end'] = newspider.end

			s.commit()
	except:
		return {}

	return spider

# 获取某个爬虫的信息 spider是一个字典
def getState(spider):

	# 如果这个爬虫是还没有开始的或者已经知道结束了的。就直接返回
	if spider['state'] == 0 or spider['state'] == 4 or spider['state'] == 1:
		return spider

	# 显然这种情况是不合理的 
	if spider['jobid'] == '':
		return None

	# 否则就要查询一下，再返回
	state = scrapyd.job_status(config['project'], spider['jobid'])

	if state == 'running':
		spider['state'] = 2
	elif state == 'pending':
		spider['state'] = 3
	elif state == 'finished':
		spider['state'] = 4
	else:
		spider['state'] = 7 #7就是未知状态

	#更新到数据库中
	with table.get_session() as s:
		oldspider = s.query(table.SPIDER).get(spider['id'])
	
		if oldspider == None:
			return True
		# 不需要更新id
		oldspider.url = spider['url']
		oldspider.keyword = spider['keyword']
		oldspider.order = spider['time']
		oldspider.jobid = spider['jobid'] 
		oldspider.state = spider['state'] 
		oldspider.name = spider['name']
		oldspider.start = spider['start'] 
		oldspider.end = spider['end'] 

		s.add(oldspider)
		s.commit()

	return spider

# 刷新传入的列表中的爬虫的信息 返回一个spider的列表,spider是字典
def updateState(spiders):

	for i in range(len(spiders)):
		spiders[i] = getState(spiders[i])
	
	return spiders

# 所有爬虫的信息 返回一个spider的列表 spider是字典
def getAllSpider():

	backqueue = []

	with table.get_session() as s:

		spiders = s.query(table.SPIDER).all()

		for oldspider in spiders:

			spider = {}
			spider['id'] = oldspider.id
			spider['url'] = oldspider.url
			spider['keyword'] = oldspider.keyword
			spider['time'] = oldspider.order
			spider['jobid'] = oldspider.jobid
			spider['state'] = oldspider.state
			spider['name'] = oldspider.name
			spider['start'] = oldspider.start
			spider['end'] = oldspider.end


			backqueue.append(spider)

	backqueue = updateState(backqueue)

	return backqueue

# 遍历爬虫的队列，返回一个符合筛选条件的spider的列表 spider 是字典
def spiderList(keyword, time):

	backqueue = []

	with table.get_session() as s:
		spiders = s.query(table.SPIDER).all()

		for oldspider in spiders:
			if oldspider.keyword == keyword and oldspider.order == (0 if time == '' else time):

				spider = {}
				spider['id'] = oldspider.id
				spider['url'] = oldspider.url
				spider['keyword'] = oldspider.keyword
				spider['time'] = oldspider.order
				spider['jobid'] = oldspider.jobid
				spider['state'] = oldspider.state
				spider['name'] = oldspider.name
				spider['start'] = oldspider.start
				spider['end'] = oldspider.end


			backqueue.append(spider)

	backqueue = updateState(backqueue)

	return backqueue

# 根据id 返回一个spider spider是字典
def returnSpider(id):

	with table.get_session() as s:
		oldspider = s.query(table.SPIDER).get(id)
		
		spider = {}
		if oldspider == None:
			return spider

		spider['id'] = oldspider.id
		spider['url'] = oldspider.url
		spider['keyword'] = oldspider.keyword
		spider['time'] = oldspider.order
		spider['jobid'] = oldspider.jobid
		spider['state'] = oldspider.state
		spider['name'] = oldspider.name
		spider['start'] = oldspider.start
		spider['end'] = oldspider.end


	# 该爬虫不存在
	if spider == {}:
		return {}

	# 查询这个爬虫的状态
	spider = getState(spider)

	return spider


# 通过id修改某个spider的参数信息 返回一个spider spider是字典
def updateSpider(id, url, keyword, time, start, end):

	with table.get_session() as s:
		oldspider = s.query(table.SPIDER).get(id)

		if oldspider == None:
			# 不存在这个spider 那就新建一个和更新后的相等即可
			return createSpider(url, keyword, time)

		spider = {}

		spider['id'] = oldspider.id
		spider['url'] = oldspider.url
		spider['keyword'] = oldspider.keyword
		spider['time'] = oldspider.order
		spider['jobid'] = oldspider.jobid
		spider['state'] = oldspider.state
		spider['name'] = oldspider.name
		spider['start'] = oldspider.start
		spider['end'] = oldspider.end

		# 获取当前想要更新的spider的信息，如果在运行就停止掉
		spider = getState(spider)

		if str(spider['state']) == '2' or str(spider['state']) == '3':
			stopSpider(spider['id'])

		# 不需要修改id
		# 下列这些参数 没有传入 自然认为是不用修改的
		oldspider.url = url
		oldspider.keyword = oldspider.keyword if keyword == None else keyword 
		oldspider.order = (0 if time == '' else time)
		oldspider.jobid = '' # 修改后的爬虫就和一个新爬虫是一样的  所以没有jobid
		oldspider.state = 0 # 爬虫的状态就要改为新建状态
		oldspider.name = ('youspider' if 'youtube' in url else 'bispider')
		oldspider.start = oldspider.start if start == None else start 
		oldspider.end = oldspider.end if end == None else end 

		s.add(oldspider)
		s.commit() 

		return spider

# 通过id删除某个spider 返回删除成功与否
def dropSpider(id):
	
	try:
		with table.get_session() as s:
			oldspider = s.query(table.SPIDER).get(id)
		
			if oldspider == None:
				return True

			spider = {}

			spider['id'] = oldspider.id
			spider['url'] = oldspider.url
			spider['keyword'] = oldspider.keyword
			spider['time'] = oldspider.order
			spider['jobid'] = oldspider.jobid
			spider['state'] = oldspider.state
			spider['name'] = oldspider.name
			spider['start'] = oldspider.start
			spider['end'] = oldspider.end

			# 获取当前想要更新的spider的信息，如果在运行就停止掉
			spider = getState(spider)

			if str(spider['state']) == '2' or str(spider['state']) == '3':
				stopSpider(spider['id'])

			s.delete(oldspider)
			s.commit()

			return True
	except:
		return False

# 启动爬虫 输入一个id 返回成功与否
def startSpider(id):

	settings = {"JOBDIR":f"recording/spider{id}"}
	with table.get_session() as s:
		spider = s.query(table.SPIDER).get(id)

		if spider == None:
			return False

		# 如果该爬虫 已经在排队中、运行中、已经运行结束了 就直接不再启动 直接返回ture 也不需要修改什么信息到数据库
		if str(spider.state) == '2' or str(spider.state) == '3' or str(spider.state) == '4':
			return True

		# 曾经是被暂停了的
		if spider.jobid != '':
			scrapyd.schedule(config['project'], spider.name, settings = settings, jobid = spider.jobid, keyword = spider.keyword, order = spider.order)
		else:
			jobid = scrapyd.schedule(config['project'], spider.name, settings = settings, keyword = spider.keyword, order = spider.order)
			spider.jobid = jobid

		s.add(spider)
		s.commit()

		spider.state = 3 # 默认假设 刚放进去就会在排队中
	
	return True

# 停止爬虫(包含了暂停) 输入一个id 返回成功与否
def stopSpider(id):

	with table.get_session() as s:
		spider = s.query(table.SPIDER).get(id)
		
		if spider == None:
			return True
		# 没有在排队或者运行中就不需要停止
		if str(spider.state) != '2' and str(spider.state) != '3':
			return True

		# 这个地方不能一直发送关闭信号，否则对方会保存状态来不及 继续运行就会报错 但是只关闭一次，又关闭掉啊 所以只能拜托前端 再多关几次？
		scrapyd.cancel(config['project'], spider.jobid)
		#scrapyd.cancel(config['project'], spider.jobid)

		spider.state = 1

		s.add(spider)
		s.commit()
	
	return True

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8964)