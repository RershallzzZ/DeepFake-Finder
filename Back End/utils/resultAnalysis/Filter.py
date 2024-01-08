import datetime
from setting import website_select
from sqlalchemy import extract, and_, text


def optionFilter(title, promulgator, year, monitorDate, category, website):
    filter_obj = []
    # 筛选标题、作者、类别、监控日期、年份
    for i in website:
        filter_obj.append(website_select[i].query.filter(
            and_(
                website_select[i].title.like("%" + title + "%") if title is not None and title != '' else text(''),
                website_select[i].promulgator.like(
                    "%" + promulgator + "%") if promulgator is not None and promulgator != '' else text(''),
                website_select[i].category.in_(category),
                and_(
                    extract('year', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                                '%Y-%m-%d').year
                    if monitorDate is not None and monitorDate != '' else text(''),
                    extract('month', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                                 '%Y-%m-%d').month
                    if monitorDate is not None and monitorDate != '' else text(''),
                    extract('day', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                               '%Y-%m-%d').day
                    if monitorDate is not None and monitorDate != '' else text('')
                ),
                extract('year', website_select[i].upload_time) == datetime.datetime.strptime(year, "%Y").year
                if year is not None and year != '' else text(''))).all())
    return filter_obj


# 筛选时长
def durationFilter(duration, sourceList):
    filterList_all = []

    for i in duration:
        if i == '3分钟以下':
            time = datetime.datetime.strptime('00:03:00', '%H:%M:%S')
            for j in sourceList:
                if j.duration.count(':') == 1:
                    target_duration = datetime.datetime.strptime(j.duration, '%M:%S')
                    if target_duration.minute < time.minute:
                        filterList_all.append(j)

        elif i == '3-10分钟':
            time1 = datetime.datetime.strptime('00:03:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('00:10:00', '%H:%M:%S')

            for j in sourceList:
                if j.duration.count(':') == 1:
                    target_duration = datetime.datetime.strptime(j.duration, '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute:
                        filterList_all.append(j)

        elif i == '10-30分钟':
            time1 = datetime.datetime.strptime('00:10:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('00:30:00', '%H:%M:%S')

            for j in sourceList:
                if j.duration.count(':') == 1:
                    target_duration = datetime.datetime.strptime(j.duration, '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.minute < time2.minute:
                        filterList_all.append(j)

        elif i == '30-60分钟':
            time1 = datetime.datetime.strptime('00:30:00', '%H:%M:%S')
            time2 = datetime.datetime.strptime('01:00:00', '%H:%M:%S')

            for j in sourceList:
                if j.duration.count(':') == 1:
                    target_duration = datetime.datetime.strptime(j.duration, '%M:%S')
                    if target_duration.minute >= time1.minute and target_duration.hour < time2.hour:
                        filterList_all.append(j)

        elif i == '60分钟以上':
            time = datetime.datetime.strptime('01:00:00', '%H:%M:%S')

            for j in sourceList:
                if j.duration.count(':') == 2:
                    target_duration = datetime.datetime.strptime(j.duration, '%H:%M:%S')
                    if target_duration.hour >= time.hour:
                        filterList_all.append(j)

    return filterList_all


def dfOptionFilter(title, promulgator, year, monitorDate, category, website):
    filter_obj = []
    # 筛选标题、作者、类别、监控日期、年份
    for i in website:
        filter_obj.append(website_select[i].query.filter(
            and_(
                website_select[i].title.like("%" + title + "%") if title is not None and title != '' else text(''),
                website_select[i].promulgator.like(
                    "%" + promulgator + "%") if promulgator is not None and promulgator != '' else text(''),
                website_select[i].category.in_(category),
                website_select[i].analyzed > 1,
                and_(
                    extract('year', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                                '%Y-%m-%d').year
                    if monitorDate is not None and monitorDate != '' else text(''),
                    extract('month', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                                 '%Y-%m-%d').month
                    if monitorDate is not None and monitorDate != '' else text(''),
                    extract('day', website_select[i].crawl_time) == datetime.datetime.strptime(monitorDate,
                                                                                               '%Y-%m-%d').day
                    if monitorDate is not None and monitorDate != '' else text('')
                ),
                extract('year', website_select[i].upload_time) == datetime.datetime.strptime(year, "%Y").year
                if year is not None and year != '' else text(''))).all())
    return filter_obj
