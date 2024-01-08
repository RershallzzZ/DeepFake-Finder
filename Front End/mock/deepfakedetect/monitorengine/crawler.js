import Mock from 'mockjs'

const crawlerList = [
    {
        'id|+1': 1,
        'state|1': [-1, 0, 1],
        'url|1': ['https://www.youtube.com/', 'https://www.bilibili.com/', 'https://vimeo.com/'],
        'keyword|1': ['deepfake', '维尼熊', '特朗普', '奥巴马', 'AI换脸'],
        'time|1': [true, false],
        'len|1': [1, 2, 3],
    },
]

const changeCrawler = {
    id: 1,
    'state|1': [-1, 0, 1],
    'url|1': ['https://www.youtube.com/', 'https://www.bilibili.com/', 'https://vimeo.com/'],
    'keyword|1': ['deepfake', '维尼熊', '特朗普', '奥巴马', 'AI换脸'],
    'time|1': [true, false],
    'len|1': [1, 2, 3],
}

export default [
    //搜索
    {
        url: '/deepfake-finder/monitorengine/crawler/list/search',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: {
                    total: '@integer(3,3)',
                    'list|3': crawlerList,
                },
            }
        },
    },

    //新增爬虫
    {
        url: '/deepfake-finder/monitorengine/crawler',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: '新增爬虫成功',
            }
        },
    },

    //查询数据
    {
        url: '/deepfake-finder/monitorengine/crawler',
        type: 'get',
        response: _ => {
            return {
                code: 20000,
                data: changeCrawler,
            }
        },
    },

    //修改数据
    {
        url: '/deepfake-finder/monitorengine/crawler/update',
        type: 'put',
        response: _ => {
            return {
                code: 20000,
                data: '修改成功',
            }
        },
    },

    //删除
    {
        url: '/deepfake-finder/monitorengine/crawler/delete',
        type: 'delete',
        response: _ => {
            return {
                code: 20000,
                data: '删除成功',
            }
        },
    },

    //更新爬虫状态
    {
        url: '/deepfake-finder/monitorengine/crawler/state',
        type: 'put',
        response: _ => {
            return {
                code: 20000,
                data: '更新爬虫状态成功',
            }
        },
    },
]
