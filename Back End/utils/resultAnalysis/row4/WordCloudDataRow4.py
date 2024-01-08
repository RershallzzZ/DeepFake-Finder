from utils.resultAnalysis.Filter import optionFilter, durationFilter
from setting import website_select
from collections import Counter


def WordCloudAuthor(title, promulgator, year, category, website, duration, monitorDate):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    chosen_author = []
    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj = filterObj + i
    filterObj = durationFilter(duration, filterObj)
    for i in filterObj:
        chosen_author.append(i.promulgator)

    chosen_author = sorted(dict(Counter(chosen_author)).items(), key=lambda d: d[1], reverse=True)
    wordCloudData = dict(chosen_author)
    wordCloudData = [{'name': name, 'value': value} for name, value in wordCloudData.items()]

    return wordCloudData
