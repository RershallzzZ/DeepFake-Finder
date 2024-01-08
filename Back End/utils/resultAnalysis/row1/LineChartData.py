from setting import website_select
from utils.resultAnalysis.Filter import optionFilter, durationFilter


def getLineChartData(title, promulgator, year, monitorDate, category, website, duration):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    all_year = []
    df_year = []
    crawlerCount = []
    dfCount = []

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj = filterObj + i
    filterObj = durationFilter(duration, filterObj)
    for j in filterObj:
        all_year.append(j.upload_time.year)
        if j.analyzed > 1:
            df_year.append(j.upload_time.year)

    all_year.sort()
    df_year.sort()
    # 获取年份列表
    if all_year:
        result_year = list(range(min(all_year), max(all_year) + 1))
        for i in result_year:
            # 获取downloadVideo列表
            crawlerCount.append(all_year.count(i))
            # 获取deepfakeVideo列表
            dfCount.append(df_year.count(i))
    # 处理一下查询不到搜索结果且没指定年份的情况
    else:
        result_year = []
        for i in website:
            for j in website_select[i].query.all():
                result_year.append(j.upload_time.year)
        result_year = list(set(result_year))
        result_year.sort()
        for i in range(0, len(result_year)):
            crawlerCount.append(0)
            dfCount.append(0)

    lineChart_Data = {
        'year': result_year,
        'deepfakeVideo': dfCount,
        'downloadVideo': crawlerCount
    }
    return lineChart_Data
