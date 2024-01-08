from utils.query2dict import queryToDict
import datetime
from setting import website_select
from utils.resultAnalysis.Filter import optionFilter


def getBarChartData(title, promulgator, year, monitorDate, category, website, duration):
    if len(website) == 0:  # websites为空，返回所有网站数据
        website = website_select.keys()
        website = list(website)
    if len(category) == 0:
        category = ['政治', '娱乐', '科技', '其他']
    if len(duration) == 0:
        duration = ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上']

    filterList = optionFilter(title, promulgator, year, monitorDate, category, website)
    filterObj = []
    for i in filterList:
        filterObj = filterObj + i
    (resultDuration, resultDfCount, resultCrawlerCount) = getNumberOfDuration(duration, filterObj)
    barChartData = {
        'duration': resultDuration,
        'deepfakeVideo': resultDfCount,
        'downloadVideo': resultCrawlerCount,
    }
    return barChartData


def getNumberOfDuration(duration, sourceList):  # 都是按照[)取值
    result_duration = []
    result_crawlerCount = []
    result_dfCount = []

    for i in duration:
        crawlerCount = 0
        dfCount = 0
        if i == '3分钟以下':
            time = datetime.datetime.strptime('00:03:00', '%H:%M:%S')
            for k in sourceList:
                if queryToDict(k)['duration'].count(':') == 1:
                    target_duration = datetime.datetime.strptime(queryToDict(k)['duration'], '%M:%S')
                    if target_duration.minute < time.minute:
                        crawlerCount = crawlerCount + 1
                    if target_duration.minute < time.minute and queryToDict(k)['analyzed'] > 1:
                        dfCount = dfCount + 1

            result_duration.append(i)
            result_crawlerCount.append(crawlerCount)
            result_dfCount.append(dfCount)

        elif i == '3-10分钟':
            time1 = datetime.datetime.strptime('00:03:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('00:10:00', '%H:%M:%S')

            for k in sourceList:
                if queryToDict(k)['duration'].count(':') == 1:
                    target_duration = datetime.datetime.strptime(queryToDict(k)['duration'], '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute:
                        crawlerCount = crawlerCount + 1
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute and \
                            queryToDict(k)['analyzed'] > 1:
                        dfCount = dfCount + 1

            result_duration.append(i)
            result_crawlerCount.append(crawlerCount)
            result_dfCount.append(dfCount)

        elif i == '10-30分钟':
            time1 = datetime.datetime.strptime('00:10:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('00:30:00', '%H:%M:%S')

            for k in sourceList:
                if queryToDict(k)['duration'].count(':') == 1:
                    target_duration = datetime.datetime.strptime(queryToDict(k)['duration'], '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute:
                        crawlerCount = crawlerCount + 1
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute and \
                            queryToDict(k)['analyzed'] > 1:
                        dfCount = dfCount + 1

            result_duration.append(i)
            result_crawlerCount.append(crawlerCount)
            result_dfCount.append(dfCount)

        elif i == '30-60分钟':
            time1 = datetime.datetime.strptime('00:30:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('01:00:00', '%H:%M:%S')

            for k in sourceList:
                if queryToDict(k)['duration'].count(':') == 1:
                    target_duration = datetime.datetime.strptime(queryToDict(k)['duration'], '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.hour < time2.hour:
                        crawlerCount = crawlerCount + 1
                    if target_duration.minute >= time1.minute and target_duration.hour < time2.hour and \
                            queryToDict(k)['analyzed'] > 1:
                        dfCount = dfCount + 1

            result_duration.append(i)
            result_crawlerCount.append(crawlerCount)
            result_dfCount.append(dfCount)

        elif i == '60分钟以上':
            time = datetime.datetime.strptime('01:00:00', '%H:%M:%S')

            for k in sourceList:
                if queryToDict(k)['duration'].count(':') == 2:
                    target_duration = datetime.datetime.strptime(queryToDict(k)['duration'], '%H:%M:%S')
                    if target_duration.hour >= time.hour:
                        crawlerCount = crawlerCount + 1
                    if target_duration.hour >= time.hour and queryToDict(k)['analyzed'] > 1:
                        dfCount = dfCount + 1

            result_duration.append(i)
            result_crawlerCount.append(crawlerCount)
            result_dfCount.append(dfCount)

    return (result_duration, result_dfCount, result_crawlerCount)
