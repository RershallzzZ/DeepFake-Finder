from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter


def getPieChartData(title, promulgator, year, monitorDate, category, website, duration):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    df_high = 0
    df_medium = 0
    df_low = 0
    df_none = 0

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj = filterObj + i
    filterObj = durationFilter(duration, filterObj)

    for i in filterObj:
        if i.analyzed == 4:
            df_high += 1
        elif i.analyzed == 3:
            df_medium += 1
        elif i.analyzed == 2:
            df_low += 1
        elif i.analyzed == 1:
            df_none += 1
    pieChartData = {
        'high': df_high,
        'medium': df_medium,
        'low': df_low,
        'none': df_none,
    }
    return pieChartData
