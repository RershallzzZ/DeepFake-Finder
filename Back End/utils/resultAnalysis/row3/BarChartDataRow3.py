from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter
from utils.resultAnalysis.row3.WordCloudDataRow3 import regex_change, delete_stopwords


def getBarChartDataRow3(title, promulgator, year, category, website, duration, monitorDate):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    titleTop10 = []
    titleNum = []

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj.append(durationFilter(duration, i))

    for i in filterObj:
        temp = []
        for j in i:
            temp.append(j.title)
            titleTop10.append(j.title)
        titleNum.append(temp)

    result_titleTop10 = []
    result_titleNum = []
    count = 0

    # 使用正则过滤
    for i in range(len(titleNum)):
        for j in range(len(titleNum[i])):
            titleNum[i][j] = regex_change(titleNum[i][j])
            titleTop10[count] = regex_change(titleTop10[count])
            count += 1

    # 清洗数据，并返回词袋字典
    titleTop10 = delete_stopwords(titleTop10)
    for i in range(len(titleNum)):
        titleNum[i] = delete_stopwords(titleNum[i])
        result_titleNum.append([])

    titleTop10 = sorted(titleTop10.items(), key=lambda d: d[1], reverse=True)

    for i in range(10 if len(titleTop10) >= 10 else len(titleTop10)):
        result_titleTop10.append(titleTop10[i][0])
        for j in range(len(titleNum)):
            result_titleNum[j].append(
                titleNum[j][titleTop10[i][0]] if titleTop10[i][0] in titleNum[j].keys() else 0)

    result_titleTop10.reverse()
    for i in range(len(result_titleNum)):
        result_titleNum[i].reverse()

    barChartData = {
        'websites': website,
        'data': {
            'titleTop10': result_titleTop10,
            'titleNum': result_titleNum
        }
    }

    return barChartData
