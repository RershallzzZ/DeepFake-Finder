from collections import Counter
from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter


def lowerNDem(myList, dropDem=2):
    '''lower the dimention of a list [dropDem] times'''
    tempList = []  # 临时列表
    for i in range(dropDem):
        tempList = []
        for myListItem in myList:  # 探索第二高维
            if type(myListItem) == list:  # 若第二高维不是0维
                for myListItemItem in myListItem:  # 分解第二高维
                    tempList.append(myListItemItem)  # 填充进临时列表
            else:  # 若第二高维是0维
                tempList.append(myListItem)  # 填充进临时列表
        myList = tempList  # 原列表替换
    return myList


def getBarChartDataRow4(title, promulgator, year, category, website, duration, monitorDate):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']
    top10_author = []
    top10_count = []
    top10_website = []
    result_author = []

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in range(len(filterList)):
        filterObj.append(durationFilter(duration, filterList[i]))
    for i in filterObj:
        temp = []
        for j in i:
            temp.append(j.promulgator)
        result_author.append(temp)
    for i in range(len(result_author)):
        result_author[i] = list(Counter(result_author[i]).items())
        for j in range(len(result_author[i])):
            result_author[i][j] = list(result_author[i][j])
            result_author[i][j].append(website[i])
    result_author = lowerNDem(result_author, dropDem=1)
    result_author = sorted(result_author, key=lambda r: r[1], reverse=True)

    for i in range(10 if len(result_author) >= 10 else len(result_author)):
        top10_author.append(result_author[i][0])
        top10_count.append(result_author[i][1])
        top10_website.append(result_author[i][2])

    top10_author.reverse()
    top10_count.reverse()
    top10_website.reverse()

    barChartData = {
        'author': top10_author,
        'count': top10_count,
        'website': top10_website,
    }

    return barChartData
