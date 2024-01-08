from exts import db


class Youtube(db.Model):
    __tablename__ = 'youtube'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    promulgator = db.Column(db.String(255))
    introduction = db.Column(db.Text(25500))
    sha256 = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    upload_time = db.Column(db.Date)
    crawl_time = db.Column(db.DateTime)
    video_path = db.Column(db.String(255))
    screenshot_path = db.Column(db.String(255))
    download = db.Column(db.Boolean)
    analyzed = db.Column(db.Integer)
    fast_analyzed = db.Column(db.Integer, default=0)
    deep_analyzed = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=-1)  # -1代表待检测 0代表检测中 1代表已检测
    watchtime = db.Column(db.String(255))
    category = db.Column(db.String(255))
    result_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    compression_mode = db.Column(db.String(255))


class Bilibili(db.Model):
    __tablename__ = 'bilibili'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255), unique=True)
    promulgator = db.Column(db.String(255))
    introduction = db.Column(db.Text(25500))
    sha256 = db.Column(db.String(255))
    duration = db.Column(db.String(255))
    upload_time = db.Column(db.Date)
    crawl_time = db.Column(db.DateTime)
    video_path = db.Column(db.String(255))
    screenshot_path = db.Column(db.String(255))
    download = db.Column(db.Boolean)
    analyzed = db.Column(db.Integer)  # 0代表未检测 1代表无疑似 2代表低疑似 3代表中疑似 4代表高疑似
    fast_analyzed = db.Column(db.Integer, default=0)
    deep_analyzed = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, default=-1)  # -1代表待检测 0代表检测中 1代表已检测
    watchtime = db.Column(db.String(255))
    category = db.Column(db.String(255))
    result_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    compression_mode = db.Column(db.String(255))


class Upload(db.Model):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sha256 = db.Column(db.String(255))
    video_path = db.Column(db.String(255))
    analyzed = db.Column(db.Integer, default=0)
    fast_analyzed = db.Column(db.Integer, default=0)
    deep_analyzed = db.Column(db.Integer, default=0)
    result_path = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    compression_mode = db.Column(db.String(255))


class Crawler(db.Model):
    __tablename__ = 'crawler'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state = db.Column(db.Integer, default=-1)  # 爬虫状态 -1表示关闭 0表示暂停 1表示开启
    url = db.Column(db.String(255), nullable=False)
    keyword = db.Column(db.String(255))
    time = db.Column(db.Boolean, default=False)
    len = db.Column(db.Integer, default=0)
    name = db.Column(db.String(255))


class WarningUser(db.Model):
    __tablename__ = 'warning_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    analyzed = db.Column(db.Integer, nullable=False)  # 预警阈值
    create_time = db.Column(db.Date)
