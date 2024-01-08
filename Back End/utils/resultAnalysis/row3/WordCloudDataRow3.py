from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter
import jieba
import os
import re
from collections import Counter

WORDCLOUD_TXT_DIR = os.path.join('utils', 'resultAnalysis', 'row3')
stopword_file = os.path.join(WORDCLOUD_TXT_DIR, 'stopwords.txt')
user_dict = os.path.join(WORDCLOUD_TXT_DIR, 'user_dict.txt')

# 加载自定义字典
jieba.load_userdict(user_dict)


# 按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


def regex_change(line):
    regex1 = 'deepfake'
    regex2 = 'deepfakes'
    regex3 = 'ai'
    regex4 = 'al'
    line = re.sub(regex1, 'DeepFake', line, flags=re.IGNORECASE)
    line = re.sub(regex2, 'DeepFake', line, flags=re.IGNORECASE)
    line = re.sub(regex3, 'AI', line, flags=re.IGNORECASE)
    line = re.sub(regex4, 'AI', line, flags=re.IGNORECASE)

    return line


# 剔除停用词并分词
def delete_stopwords(lines):
    stopwords = read_file(stopword_file)
    all_words = []

    for line in lines:
        all_words += [word for word in jieba.cut(line, cut_all=False) if
                      word not in stopwords and not word.isdigit() and len(word) > 1]
    dict_words = dict(Counter(all_words))
    return dict_words


def WordCloudTitle(title, promulgator, year, category, website, duration, monitorDate):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    chosen_title = []

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj = filterObj + i
    filterObj = durationFilter(duration, filterObj)

    for i in filterObj:
        chosen_title.append(i.title)

    # 使用正则过滤
    for i in range(len(chosen_title)):
        chosen_title[i] = regex_change(chosen_title[i])

    # 清洗数据，并返回词袋字典
    bowWords_all = delete_stopwords(chosen_title)

    # 对词袋字典进行排序
    resultWords_chosen = sorted(bowWords_all.items(), key=lambda d: d[1], reverse=True)

    wordCloudData = dict(resultWords_chosen)
    wordCloudData = [{'name': name, 'value': value} for name, value in wordCloudData.items()]

    return wordCloudData
