const userList = [
    {
        'id|+1': 1,
        'username|1': ['rershall','Sakura','DeepFake Finder'],
        'email|1': ['2238174013@qq.com', '980870969@qq.com', '1043047701@qq.com'],
        'url|1': ['https://www.youtube.com/', 'https://www.bilibili.com/', 'https://vimeo.com/'],
        'create_time|1': ['2020-05-04','2020-04-24','2020-04-15','2020-05-14','2020-05-08'],
        'analyzed|1': [2, 3, 4],
    },
]

const userById = {
    id: 1,
    'username|1': ['rershall','Sakura','取名也是一门艺术','DeepFake Finder'],
    'email|1': ['2238174013@qq.com', '980870969@qq.com', '1043047701@qq.com'],
    'url|1': ['https://www.youtube.com/', 'https://www.bilibili.com/', 'https://vimeo.com/'],
    'create_time|1': ['2020-05-04','2020-04-24','2020-04-15','2020-05-14','2020-05-08'],
    'analyzed|1': [2, 3, 4],
}

export default [
    {
        url: '/deepfake-finder/earlywarning/config/list/search',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: {
                    total: '@integer(3,3)',
                    'userList|3': userList,
                },
            }
        },
    },
    {
        url: '/deepfake-finder/earlywarning/config',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: '新增通知用户成功',
            }
        },
    },
    //查询数据
    {
        url: '/deepfake-finder/earlywarning/config',
        type: 'get',
        response: _ => {
            return {
                code: 20000,
                data: userById,
            }
        },
    },

    //修改数据
    {
        url: '/deepfake-finder/earlywarning/config',
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
        url: '/deepfake-finder/earlywarning/config',
        type: 'delete',
        response: _ => {
            return {
                code: 20000,
                data: '删除成功',
            }
        },
    },
]
