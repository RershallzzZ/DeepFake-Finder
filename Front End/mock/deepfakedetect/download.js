const list = [
    {
        'id|+1': 10,
        crawl_time: "@datetime('yyyy-MM-dd HH:mm:ss')",
        title: '@ctitle()',
        publishtime: "@datetime('yyyy-MM-dd')",
        duration: "@time('m:ss')",
        'category|1': ['政治', '娱乐', '科技', '其他'], // 4选 其1
        url: "@url('http')",
        'isDownload|1': [0, 1],
    },
]

export default [
    {
        url: '/deepfake-finder/download/search',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: {
                    total: '@integer(3000,5000)',
                    'list|20': list,
                },
            }
        },
    },
    {
        url: '/deepfake-finder/download/delete',
        type: 'delete',
        response: config => {
            console.log('213123', config.body)
            return {
                code: 20000,
                flag: true,
                message: '删除成功',
            }
        },
    },
    {
        url: '/deepfake-finder/download/path',
        type: 'get',
        response:config=>{
            console.log(config.query)
            return {
                code:20000,
                data:{
                    path:'videos/777.mp4'
                }
            }
        }
    },
    {
        url:'/deepfake-finder/download/snapshot',
        type:'get',
        response:config=>{
            console.log(config.query)
            return {
                code:20000,
                data:{
                    path:'snapshots/shot.png'
                }
            }
        }
    }
]
