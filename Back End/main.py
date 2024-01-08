import sys

sys.path.append('./classification')
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_script import Manager
from werkzeug.utils import secure_filename
import db_config
import hashlib
import datetime
from exts import db
from utils.query2dict import queryToDict
from utils.getImagePath import get_image_path
from utils.resultAnalysis.row1.LineChartData import getLineChartData
from utils.resultAnalysis.row1.BarChartData import getBarChartData
from utils.resultAnalysis.row2.PieChartData import getPieChartData
from utils.resultAnalysis.row2.BarChartDataRow2 import getBarChartDataRow2
from utils.resultAnalysis.row2.RaddarChartData import getRaddarChartData
from utils.resultAnalysis.row3.WordCloudDataRow3 import WordCloudTitle
from utils.resultAnalysis.row3.BarChartDataRow3 import getBarChartDataRow3
from utils.resultAnalysis.row4.WordCloudDataRow4 import WordCloudAuthor
from utils.resultAnalysis.row4.BarChartDataRow4 import getBarChartDataRow4
from compression_detection import compression_detection
from classification.detect_from_video import test_full_image_network
from sqlalchemy import text, and_
from setting import *

app = Flask(__name__)
app.config.from_object(db_config)
db.init_app(app)
manage = Manager(app)
CORS(app)  # 允许跨域
app.app_context().push()
db.create_all()


@app.route('/video/<website>/<filename>', methods=['GET', 'POST'])
def get_video(website, filename):
    video_path = os.path.join(VIDEO_PATH, website)
    return send_from_directory(video_path, filename)


@app.route('/result/<website>/<filename>', methods=['GET', 'POST'])
def get_result_video(website, filename):
    return send_from_directory(os.path.join(RESULT_PATH, website), filename)


@app.route('/image/<website>/<video_name>/<filename>', methods=['GET', 'POST'])
def get_image(website, video_name, filename):
    return send_from_directory(os.path.join(os.path.join(IMAGE_PATH, website), video_name), filename)


@app.route('/screenshot/<website>/<filename>', methods=['GET', 'POST'])
def get_screenshot(website, filename):
    screenshot_path = os.path.join(SCREENSHOT_PATH, website)
    return send_from_directory(screenshot_path, filename)


@app.route('/deepfake-finder/website', methods=['GET'])
def get_website():
    all_website_name = []
    for i in Crawler.query.all():
        all_website_name.append(i.name)
    all_website_name = list(set(all_website_name))
    all_website_name.sort()
    all_website_list = []
    for i in all_website_name:
        all_website_list.append({
            'value': i,
            'label': i
        })
    # all_website_list.append({
    #     'value': 'vimeo',
    #     'label': 'vimeo'
    # })
    res = {
        'code': 20000,
        'data': {
            'websiteList': all_website_list
        }
    }
    return jsonify(res)


# 系统首页
@app.route('/deepfake-finder/profile', methods=['GET'])
def getProfile():
    monitorWebsite = len(website_select)
    downloadVideo = 0
    detectVideo = 0
    deepfakeVideo = 0
    for i in website_select.values():
        downloadVideo = downloadVideo + i.query.count()
        detectVideo = detectVideo + i.query.filter(i.analyzed >= 1).count()
        deepfakeVideo = deepfakeVideo + i.query.filter(i.analyzed > 1).count()

    profileData = {
        'monitorWebsite': monitorWebsite,
        'downloadVideo': downloadVideo,
        'detectVideo': detectVideo,
        'deepfakeVideo': deepfakeVideo,
    }
    response = {
        'code': 20000,
        'data': profileData
    }
    return jsonify(response)


@app.route('/deepfake-finder/dashboard/linechart', methods=['GET'])
def getDashboardLineChart():
    title = ''
    promulgator = ''
    year = ''
    monitorDate = ''
    category = []
    website = []
    duration = []
    lineChartData = getLineChartData(title, promulgator, year, monitorDate, category, website, duration)
    response = {
        'code': 20000,
        'data': lineChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/dashboard/piechart', methods=['GET'])
def getDashboardPieChart():
    title = ''
    promulgator = ''
    year = ''
    monitorDate = ''
    category = []
    website = []
    duration = []
    pieChartData = getPieChartData(title, promulgator, year, monitorDate, category, website, duration)
    response = {
        'code': 20000,
        'data': pieChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/dashboard/barchart', methods=['GET'])
def getDashboardBarChart():
    title = ''
    promulgator = ''
    year = ''
    monitorDate = ''
    category = []
    website = []
    duration = []

    barChartData = getBarChartDataRow2(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': barChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/dashboard/raddarchart', methods=['GET'])
def getDashboardRaddarChart():
    title = ''
    promulgator = ''
    year = ''
    monitorDate = ''
    category = []
    website = []
    duration = []

    raddarChartData = getRaddarChartData(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': raddarChartData
    }
    return jsonify(response)


# 视频采集展示页面
@app.route('/deepfake-finder/download/search', methods=['POST'])
def download_search():
    page = request.json['page']
    size = request.json['size']
    searchMap = request.json['searchMap']
    keyword = searchMap['title']
    website = searchMap['website']

    paginate_obj = website_select[website].query.filter(
        website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text('')).paginate(page=page,
                                                                                                             per_page=size,
                                                                                                             error_out=False)
    total = website_select[website].query.filter(
        website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text('')).count()

    video_list = paginate_obj.items
    result = []
    for i in video_list:
        temp = queryToDict(i)
        temp.pop('sha256')
        temp.pop('promulgator')
        temp.pop('introduction')
        temp.pop('video_path')
        temp.pop('screenshot_path')
        temp.pop('fast_analyzed')
        temp.pop('deep_analyzed')
        temp.pop('state')
        temp.pop('result_path')
        temp.pop('image_path')
        temp.pop('compression_mode')
        result.append(temp)
    response = {
        'code': 20000,
        'data': {
            'total': total,
            'list': result
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/download/delete', methods=['DELETE'])
def download_delete():
    id = request.json['id']
    website = request.json['website']
    target = website_select[website].query.filter(website_select[website].id == id).first()
    db.session.delete(target)
    db.session.commit()
    response = {
        'code': 20000,
        'flag': True,
        'message': '删除成功',
    }
    return jsonify(response)


@app.route('/deepfake-finder/download/video', methods=['GET'])
def download_video():
    id = request.args.get('id')
    website = request.args.get('website')
    target = website_select[website].query.filter(website_select[website].id == id).first()
    path = target.video_path
    response = {
        'code': 20000,
        'data': {
            'path': path,
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/download/screenshot', methods=['GET'])
def download_screenshot():
    id = request.args.get('id')
    website = request.args.get('website')
    target = website_select[website].query.filter(website_select[website].id == id).first()
    path = target.screenshot_path
    response = {
        'code': 20000,
        'data': {
            'path': path,
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/detectresult/search', methods=['POST'])
def detectresult_search():
    size = request.json['size']
    page = request.json['page']
    searchMap = request.json['searchMap']
    keyword = searchMap['title']
    website = searchMap['website']
    analyzed = searchMap['analyzed']

    paginate_obj = website_select[website].query.filter(
        and_(website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text('')),
        # website_select[website].download == 1,
        website_select[website].analyzed >= 1,
        website_select[website].analyzed == analyzed if analyzed is not None else text('')).paginate(
        page=page,
        per_page=size,
        error_out=False)

    total = website_select[website].query.filter(
        and_(website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text('')),
        # website_select[website].download == 1,
        website_select[website].analyzed > 0,
        website_select[website].analyzed == analyzed if analyzed is not None else text('')).count()

    video_list = paginate_obj.items
    result = []
    for i in video_list:
        temp = queryToDict(i)
        temp.pop('sha256')
        temp.pop('promulgator')
        temp.pop('introduction')
        temp.pop('video_path')
        temp.pop('screenshot_path')
        temp.pop('fast_analyzed')
        temp.pop('deep_analyzed')
        temp.pop('state')
        temp.pop('result_path')
        temp.pop('image_path')
        temp.pop('compression_mode')
        result.append(temp)

    response = {
        'code': 20000,
        'data': {
            'total': total,
            'list': result
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/detectresult/delete', methods=['DELETE'])
def detectresult_delete():
    id = request.json['id']
    website = request.json['website']
    target = website_select[website].query.filter(website_select[website].id == id).first()
    db.session.delete(target)
    db.session.commit()
    response = {
        'code': 20000,
        'flag': True,
        'message': '删除成功',
    }
    return jsonify(response)


@app.route('/deepfake-finder/detectresult/screenshot', methods=['GET'])
def detectresult_screenshot():
    id = request.args.get('id')
    website = request.args.get('website')
    target = website_select[website].query.filter(website_select[website].id == id).first()
    path = target.screenshot_path
    response = {
        'code': 20000,
        'data': {
            'path': path,
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/detectresult/result', methods=['GET'])
def detectresult_result():
    id = request.args.get('id')
    website = request.args.get('website')
    target = website_select[website].query.filter(website_select[website].id == id).first()
    image = None
    image_6 = None
    result_video = None
    fast_analyzed = None
    deep_analyzed = None
    if target.image_path is not None:
        split = '/' if '/' in target.video_path else '\\'
        video_fn = target.video_path.split(split)[-1]
        image, image_6 = get_image_path(target.image_path, video_fn)
        fast_analyzed = target.fast_analyzed
    if target.result_path is not None:
        result_video = target.result_path
        deep_analyzed = target.deep_analyzed
    res = {
        'code': 20000,
        'data': {
            'image': image,
            'image_6': image_6,
            'resultVideo': result_video,
            'fastAnalyzed': fast_analyzed,
            'deepAnalyzed': deep_analyzed
        }
    }
    return jsonify(res)


@app.route('/deepfake-finder/earlywarning/config/list/search', methods=['POST'])
def earlywarning_config_search():
    page = request.json['page']
    size = request.json['size']
    searchMap = request.json['searchMap']
    keyword = searchMap['keyword']
    analyzed = searchMap['analyzed']

    paginate_obj = WarningUser.query.filter(
        and_(WarningUser.username.like("%" + keyword + "%") if len(keyword) != 0 and keyword is not None else text(''),
             WarningUser.analyzed == analyzed if analyzed is not None else text(''))).paginate(
        page=page,
        per_page=size,
        error_out=False)
    total = WarningUser.query.filter(
        and_(WarningUser.username.like("%" + keyword + "%") if len(keyword) != 0 and keyword is not None else text(''),
             WarningUser.analyzed == analyzed if analyzed is not None else text(''))).count()

    warning_user_list = paginate_obj.items
    result = []
    for i in warning_user_list:
        temp = queryToDict(i)
        result.append(temp)

    response = {
        'code': 20000,
        'data': {
            'total': total,
            'list': result
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/earlywarning/config', methods=['POST'])
def earlywarning_config_add():
    website_name = request.json['url']
    username = request.json['username']
    email = request.json['email']
    analyzed = request.json['analyzed']
    create_time = request.json['create_time']
    url = name_2_url[website_name]
    if len(create_time) != 0 and create_time is not None:
        create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d')
        new_warning_user = WarningUser(url=url, username=username, email=email, analyzed=analyzed,
                                       create_time=create_time)
    else:
        new_warning_user = WarningUser(url=url, username=username, email=email, analyzed=analyzed)

    db.session.add(new_warning_user)
    db.session.commit()
    res = {
        'code': 20000,
        'data': '新增监控用户成功',
    }
    return jsonify(res)


@app.route('/deepfake-finder/earlywarning/config', methods=['GET'])
def earlywarning_config_getById():
    id = request.args.get('id')
    warning_user_obj = WarningUser.query.filter(WarningUser.id == id).first()
    warning_user_obj = queryToDict(warning_user_obj)
    warning_user_obj['url'] = url_2_name[warning_user_obj['url']]
    res = {
        'code': 20000,
        'data': warning_user_obj
    }
    return jsonify(res)


@app.route('/deepfake-finder/earlywarning/config', methods=['PUT'])
def earlywarning_config_update():
    id = request.json['id']
    website_name = request.json['url']
    username = request.json['username']
    email = request.json['email']
    analyzed = request.json['analyzed']
    create_time = request.json['create_time']
    url = name_2_url[website_name]
    warning_user_obj = WarningUser.query.filter(WarningUser.id == id).first()
    warning_user_obj.username = username
    warning_user_obj.email = email
    warning_user_obj.analyzed = analyzed
    warning_user_obj.url = url
    if create_time != '' and create_time is not None:
        create_time = datetime.datetime.strptime(create_time, '%Y-%m-%d')
        warning_user_obj.create_time = create_time
    else:
        warning_user_obj.create_time = None

    db.session.commit()
    res = {
        'code': 20000,
        'data': '修改成功',
    }
    return jsonify(res)


@app.route('/deepfake-finder/earlywarning/config', methods=['DELETE'])
def earlywarning_config_delete():
    id = request.json['id']
    target = WarningUser.query.filter(WarningUser.id == id).first()
    db.session.delete(target)
    db.session.commit()
    response = {
        'code': 20000,
        'data': '删除成功',
    }
    return jsonify(response)


@app.route('/deepfake-finder/monitorengine/crawler/list/search', methods=['POST'])
def monitorengine_crawler_search():
    page = request.json['page']
    size = request.json['size']
    searchMap = request.json['searchMap']
    keyword = searchMap['keyword']
    state = searchMap['state']

    paginate_obj = Crawler.query.filter(
        and_(Crawler.keyword.like("%" + keyword + "%") if len(keyword) != 0 and keyword is not None else text(''),
             Crawler.state == state if state is not None else text(''))).paginate(
        page=page,
        per_page=size,
        error_out=False)
    total = Crawler.query.filter(
        and_(Crawler.keyword.like("%" + keyword + "%") if len(keyword) != 0 and keyword is not None else text(''),
             Crawler.state == state if state is not None else text(''))).count()

    crawler_list = paginate_obj.items
    result = []
    for i in crawler_list:
        temp = queryToDict(i)
        result.append(temp)

    response = {
        'code': 20000,
        'data': {
            'total': total,
            'list': result
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/monitorengine/crawler/website', methods=['GET'])
def monitorengine_crawler_website():
    websiteOptions = [{'url': v, 'name': k} for k, v in name_2_url.items()]
    res = {
        'code': 20000,
        'data': websiteOptions
    }
    return jsonify(res)


@app.route('/deepfake-finder/monitorengine/crawler', methods=['POST'])
def monitorengine_crawler_add():
    name = request.json['url']
    keyword = request.json['keyword']
    time = request.json['time']
    len = request.json['len']
    url = name_2_url[name]
    new_crawler = Crawler(url=url, name=name, keyword=keyword, time=time, len=len)
    db.session.add(new_crawler)
    db.session.commit()
    res = {
        'code': 20000,
        'data': '新增爬虫成功',
    }
    return jsonify(res)


@app.route('/deepfake-finder/monitorengine/crawler/update', methods=['PUT'])
def monitorengine_crawler_update():
    id = request.json['id']
    name = request.json['url']
    keyword = request.json['keyword']
    time = request.json['time']
    len = request.json['len']
    url = name_2_url[name]
    crawler_obj = Crawler.query.filter(Crawler.id == id).first()
    crawler_obj.name = name
    crawler_obj.keyword = keyword
    crawler_obj.time = time
    crawler_obj.len = len
    crawler_obj.url = url
    db.session.commit()
    res = {
        'code': 20000,
        'data': '修改成功',
    }
    return jsonify(res)


@app.route('/deepfake-finder/monitorengine/crawler', methods=['GET'])
def monitorengine_crawler_getById():
    id = request.args.get('id')
    crawler_obj = Crawler.query.filter(Crawler.id == id).first()
    crawler_obj = queryToDict(crawler_obj)
    crawler_obj['url'] = crawler_obj['name']
    crawler_obj.pop('name')
    crawler_obj.pop('state')
    res = {
        'code': 20000,
        'data': crawler_obj
    }
    return jsonify(res)


@app.route('/deepfake-finder/monitorengine/crawler/delete', methods=['DELETE'])
def monitorengine_crawler_delete():
    id = request.json['id']
    target = Crawler.query.filter(Crawler.id == id).first()
    db.session.delete(target)
    db.session.commit()
    response = {
        'code': 20000,
        'data': '删除成功',
    }
    return jsonify(response)


@app.route('/deepfake-finder/monitorengine/crawler/state', methods=['PUT'])
def monitorengine_crawler_update_state():
    id = request.json['id']
    state = request.json['state']
    crawler_obj = Crawler.query.filter(Crawler.id == id).first()
    crawler_obj.state = state
    db.session.commit()
    res = {
        'code': 20000,
        'data': '更新爬虫状态成功',
    }
    return jsonify(res)


@app.route('/deepfake-finder/monitorengine/detection/list/search', methods=['POST'])
def monitorengine_detection_search():
    page = request.json['page']
    size = request.json['size']
    searchMap = request.json['searchMap']
    keyword = searchMap['title']
    website = searchMap['website']

    paginate_obj = website_select[website].query.filter(
        and_(website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text(''),
             # website_select[website].download == 1
             )).paginate(page=page,
                         per_page=size,
                         error_out=False)
    total = website_select[website].query.filter(
        and_(website_select[website].title.like("%" + keyword + "%") if len(keyword) != 0 else text(''),
             # website_select[website].download == 1
             )).count()

    video_list = paginate_obj.items
    result = []
    for i in video_list:
        temp = queryToDict(i)
        temp.pop('sha256')
        temp.pop('promulgator')
        temp.pop('introduction')
        temp.pop('video_path')
        temp.pop('screenshot_path')
        temp.pop('fast_analyzed')
        temp.pop('deep_analyzed')
        temp.pop('result_path')
        temp.pop('image_path')
        temp.pop('compression_mode')
        result.append(temp)

    response = {
        'code': 20000,
        'data': {
            'total': total,
            'list': result
        }
    }
    return jsonify(response)


@app.route('/deepfake-finder/monitorengine/detection/manual/<video_list>', methods=['POST'])
def monitorengine_detection_manual(video_list):
    video_id = request.json['id']
    detect_mode = request.json['detectType']
    website = request.json['website']
    for i in video_id:
        video_obj = website_select[website].query.filter(website_select[website].id == i).first()
        video_obj.state = 0
    db.session.commit()

    for i in video_id:
        video_obj = website_select[website].query.filter(website_select[website].id == i).first()
        if video_obj.analyzed == 0:
            predicted_class = compression_detection.classify_video(video_obj.video_path)
            video_obj.compression_mode = predicted_class
        else:
            predicted_class = video_obj.compression_mode
        image_path = os.path.join(IMAGE_PATH, website, str(video_obj.id))
        result_path = os.path.join(RESULT_PATH, website, str(video_obj.id) + '.mp4')
        if predicted_class in ['0.6', '0.77', 'original']:
            predicted_class = '0.77'
            fake_prediction = test_full_image_network(video_obj.video_path, model=model_select[predicted_class],
                                                      output_path=result_path,
                                                      detect_mode=detect_mode, image_path=image_path,
                                                      start_frame=0, end_frame=None, cuda=cuda)

        else:
            fake_prediction = None

        if fake_prediction is not None:
            print("预测结果", fake_prediction)
            if video_obj.analyzed == 0:
                video_obj.analyzed = fake_prediction
                if detect_mode == 1:
                    video_obj.image_path = image_path
                    video_obj.fast_analyzed = fake_prediction
                elif detect_mode == 2:
                    video_obj.result_path = result_path
                    video_obj.deep_analyzed = fake_prediction
            else:
                if detect_mode == 1:
                    video_obj.image_path = image_path
                    # video_obj.analyzed = fake_prediction
                    video_obj.fast_analyzed = fake_prediction
                elif detect_mode == 2:
                    video_obj.result_path = result_path
                    video_obj.analyzed = fake_prediction
                    video_obj.deep_analyzed = fake_prediction

            video_obj.state = 1
            db.session.commit()
        else:
            video_obj.state = -1
            db.session.commit()

    response = {
        'code': 20000,
        'message': '所选视频检测完毕'
    }
    return jsonify(response)


# 结果综合分析页面
# row1
@app.route('/deepfake-finder/resultanalysis/row1/linechart', methods=['POST'])
def getLineChart():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    monitorDate = searchMap['monitorDate']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']

    lineChartData = getLineChartData(title, promulgator, year, monitorDate, category, website, duration)
    response = {
        'code': 20000,
        'data': lineChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/resultanalysis/row1/barchart', methods=['POST'])
def getBarChart():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    monitorDate = searchMap['monitorDate']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']

    barChartData = getBarChartData(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': barChartData
    }
    return jsonify(response)


# row2
@app.route('/deepfake-finder/resultanalysis/row2/piechart', methods=['POST'])
def getPieChart():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    monitorDate = searchMap['monitorDate']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']

    pieChartData = getPieChartData(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': pieChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/resultanalysis/row2/barchart', methods=['POST'])
def getBarChart2():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    monitorDate = searchMap['monitorDate']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']

    barChartData = getBarChartDataRow2(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': barChartData
    }
    return jsonify(response)


@app.route('/deepfake-finder/resultanalysis/row2/raddarchart', methods=['POST'])
def getRaddarChart():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    monitorDate = searchMap['monitorDate']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']

    raddarChartData = getRaddarChartData(title, promulgator, year, monitorDate, category, website, duration)

    response = {
        'code': 20000,
        'data': raddarChartData
    }
    return jsonify(response)


# row3
@app.route('/deepfake-finder/resultanalysis/row3/wordcloud', methods=['POST'])
def getWordCloud_title():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']
    monitorDate = searchMap['monitorDate']

    wordCloudData = WordCloudTitle(title, promulgator, year, category, website, duration, monitorDate)

    response = {
        'code': 20000,
        'data': wordCloudData
    }
    return jsonify(response)


@app.route('/deepfake-finder/resultanalysis/row3/barchart', methods=['POST'])
def getBarChart3():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']
    monitorDate = searchMap['monitorDate']

    barChartData = getBarChartDataRow3(title, promulgator, year, category, website, duration, monitorDate)

    response = {
        'code': 20000,
        'data': barChartData
    }
    return jsonify(response)


# row4
@app.route('/deepfake-finder/resultanalysis/row4/wordcloud', methods=['POST'])
def getWordCloud_author():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']
    monitorDate = searchMap['monitorDate']

    wordCloudData = WordCloudAuthor(title, promulgator, year, category, website, duration, monitorDate)

    response = {
        'code': 20000,
        'data': wordCloudData
    }
    return jsonify(response)


@app.route('/deepfake-finder/resultanalysis/row4/barchart', methods=['POST'])
def getBarChart4():
    searchMap = request.json['searchMap']
    title = searchMap['title']
    promulgator = searchMap['promulgator']
    year = searchMap['year']
    category = searchMap['category']
    website = searchMap['website']
    duration = searchMap['duration']
    monitorDate = searchMap['monitorDate']

    barChartData = getBarChartDataRow4(title, promulgator, year, category, website, duration, monitorDate)

    response = {
        'code': 20000,
        'data': barChartData
    }
    return jsonify(response)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    cache_path = os.path.join(CACHE_PATH, filename)
    file.save(cache_path)
    # 对文件名进行包装，为了安全,不过对中文的文件名显示有问题
    upload_hash = hashlib.sha256(open(cache_path, 'rb').read()).hexdigest()
    video_obj = Upload.query.filter_by(sha256=upload_hash).first()
    print("upload!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if video_obj is None:
        from shutil import copyfile
        split = '/' if '/' in cache_path else '\\'
        video_type = cache_path.split(split)[-1].split('.')[1]
        filepath = os.path.join(VIDEO_PATH, 'upload', upload_hash + '.' + video_type)
        # filepath = f'video/upload/{upload_hash}.mp4'
        print("filepath", cache_path)
        copyfile(src=cache_path, dst=filepath)
        new_upload_video = Upload(sha256=upload_hash, video_path=filepath)
        db.session.add(new_upload_video)
        db.session.commit()
    else:
        filepath = video_obj.video_path

    res = {
        "code": 20000,
        "data": {"path": filepath}
    }
    return res


@app.route('/upload/detect', methods=['POST'])
def detect_upload():
    video = request.json['video']
    detect_mode = request.json['detectMode']
    video_path = video['path']
    filename = video['filename']
    print(video_path, filename)
    upload_hash = hashlib.sha256(open(video_path, 'rb').read()).hexdigest()
    print("hash:")
    video_obj = Upload.query.filter_by(sha256=upload_hash).first()

    image = None
    image_6 = None
    result_video = None
    fast_analyzed = None
    deep_analyzed = None

    if video_obj.analyzed == 0:
        predicted_class = compression_detection.classify_video(video_path)
        result_path = os.path.join(RESULT_PATH, 'upload', filename)
        image_path = os.path.join(IMAGE_PATH, 'upload', filename.split('.')[0])
        if predicted_class in ['0.6', '0.77', 'original']:
            fake_prediction = test_full_image_network(video_path, model=model_select[predicted_class],
                                                      output_path=result_path,
                                                      detect_mode=detect_mode, image_path=image_path,
                                                      start_frame=0, end_frame=None, cuda=cuda)
        else:
            fake_prediction = None

        if fake_prediction is not None:
            print("预测结果", fake_prediction)
            video_obj.analyzed = fake_prediction
            video_obj.compression_mode = predicted_class
            if detect_mode == 1:
                video_obj.image_path = image_path
                image, image_6 = get_image_path(video_obj.image_path, filename)
                video_obj.fast_analyzed = fake_prediction
                fast_analyzed = fake_prediction
            elif detect_mode == 2:
                video_obj.result_path = result_path
                result_video = result_path
                video_obj.deep_analyzed = fake_prediction
                deep_analyzed = fake_prediction
            db.session.commit()



    else:
        if detect_mode == 1:
            if video_obj.image_path is None:
                image_path = os.path.join(IMAGE_PATH, 'upload', filename.split('.')[0])
                fake_prediction = test_full_image_network(video_path,
                                                          model=model_select[video_obj.compression_mode],
                                                          image_path=image_path, detect_mode=detect_mode,
                                                          start_frame=0, end_frame=None, cuda=cuda)
                if fake_prediction is not None:
                    video_obj.image_path = image_path
                    video_obj.fast_analyzed = fake_prediction
                    image, image_6 = get_image_path(video_obj.image_path, filename)
                    db.session.commit()
                    fast_analyzed = fake_prediction

            else:
                fast_analyzed = video_obj.fast_analyzed
                image, image_6 = get_image_path(video_obj.image_path, filename)
        elif detect_mode == 2:
            if video_obj.result_path is None:
                result_path = os.path.join(RESULT_PATH, 'upload', filename)
                fake_prediction = test_full_image_network(video_path,
                                                          model=model_select[video_obj.compression_mode],
                                                          output_path=result_path, detect_mode=detect_mode,
                                                          start_frame=0, end_frame=None, cuda=cuda)
                if fake_prediction is not None:
                    video_obj.analyzed = fake_prediction
                    video_obj.deep_analyzed = fake_prediction
                    video_obj.result_path = result_path
                    result_video = result_path
                    db.session.commit()
                    deep_analyzed = fake_prediction
            else:
                deep_analyzed = video_obj.deep_analyzed
                result_video = video_obj.result_path

    res = {
        'code': 20000,
        "data": {
            'result': {
                'image': image,
                'image_6': image_6,
                'resultVideo': result_video,
                'fastAnalyzed': fast_analyzed,
                'deepAnalyzed': deep_analyzed
            }
        }
    }
    return jsonify(res)


if __name__ == '__main__':
    manage.run()
