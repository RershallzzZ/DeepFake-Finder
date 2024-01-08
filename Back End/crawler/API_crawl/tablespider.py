#-*-coding:utf-8-*-

# 存放爬虫信息的数据表

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
    Boolean
)

#读取数据库的配置文件

with open('./config.json', 'r') as f:
    config = json.loads(f.read())['rules']


username = config['username']
password = config['password']
dbname = config['dbname']
host = config['host']
port = config['port']
tablename = config['tablename']

engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4')
Session = sessionmaker(bind=engine)
Base = declarative_base(engine)

class SPIDER(Base):
    
    __tablename__ = tablename

    id = Column(Integer, primary_key=True)
    url = Column(String(255)) #爬虫爬取的站点的url
    keyword = Column(String(255)) #爬虫关键词
    order = Column(Boolean) #爬虫是否按照时间排序
    state = Column(Integer) #0 未开始, 1 暂停中, 2 运行中, 3 排队等待中, 4 运行结束， 没有关闭状态
    jobid = Column(String(255)) #爬虫的jobid
    recording =  Column(String(255)) #爬虫暂停文件的记录位置
    name = Column(String(255)) #爬虫的名字 主要是区分YouTube爬虫和bilibili的爬虫
    start = Column(Integer) #该爬虫爬取的起始页面
    end = Column(Integer) #该爬虫爬取的结束页面


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