from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter


def getBarChartDataRow2(title, promulgator, year, monitorDate, category, website, duration):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    result_politics = []
    result_entertainment = []
    result_tech = []
    result_others = []

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj.append(durationFilter(duration, i))

    for i in filterObj:
        politicsCount = 0
        entertainmentCount = 0
        techCount = 0
        othersCount = 0

        for k in i:
            if k.category == '政治':
                politicsCount = politicsCount + 1
            elif k.category == '娱乐':
                entertainmentCount = entertainmentCount + 1
            elif k.category == '科技':
                techCount = techCount + 1
            elif k.category == '其他':
                othersCount = othersCount + 1

        result_politics.append(politicsCount)
        result_entertainment.append(entertainmentCount)
        result_tech.append(techCount)
        result_others.append(othersCount)

    barChartData = {
        'websites': website,
        'data': {
            'politics': result_politics,
            'entertainment': result_entertainment,
            'tech': result_tech,
            'others': result_others
        }
    }
    return barChartData
