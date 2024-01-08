#-*-coding:utf-8-*_

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import contextlib
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    DateTime,
    String,
    Boolean,
    Text,
    Date
)

#之所以是.youtube/config/ 是因为spider在import的时候 需要向上跳一级
#读取数据库的配置文件
#为了兼容downloader能够 打开table
try:
    with open('./youtube/config.json', 'r') as f:
        config = json.loads(f.read())['rules']
except:
    with open("./config.json", 'r') as f:
        config = json.loads(f.read())['rules']


username = config['username']
password = config['password']
dbname = config['dbname']
host = config['host']
port = config['port']
tablename = config['tablename']

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4')
Session = sessionmaker(bind=engine)
Base = declarative_base(engine)

class Movie(Base):
    
    __tablename__ = tablename

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    url = Column(String(255), unique=True)
    promulgator = Column(String(255))
    introduction = Column(Text(25500))
    sha256 = Column(String(255))
    duration = Column(String(255))
    upload_time = Column(Date)
    crawl_time = Column(DateTime)
    video_path = Column(String(255))
    screenshot_path = Column(String(255))
    download = Column(Boolean)
    analyzed = Column(Integer)
    fast_analyzed = Column(Integer, default=0)
    deep_analyzed = Column(Integer, default=0)
    state = Column(Integer, default = -1)  # -1代表待检测 0代表检测中 1代表已检测
    watchtime = Column(String(255))
    category = Column(String(255))
    result_path = Column(String(255))
    image_path = Column(String(255))
    compression_mode = Column(String(255))


@contextlib.contextmanager
def get_session():
    s = Session()
    try:
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()

# 创建表
Base.metadata.create_all(engine)