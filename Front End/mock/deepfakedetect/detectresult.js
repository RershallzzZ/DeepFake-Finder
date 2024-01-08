const list = [
    {
        'id|+1': 10,
        crawl_time: "@datetime('yyyy-MM-dd HH:mm:ss')",
        title: '@ctitle()',
        upload_time: "@datetime('yyyy-MM-dd')",
        duration: "@time('m:ss')",
        'category|1': ['政治', '娱乐', '科技', '其他'], // 4选 其1
        url: "@url('http')",
        'analyzed|1': [1, 2, 3, 4],
    },
]

export default [
    {
        url: '/deepfake-finder/detectresult/search',
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
        url: '/deepfake-finder/detectresult/delete',
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
        url: '/deepfake-finder/detectresult/image/path',
        type: 'get',
        response: config => {
            console.log(config.query)
            return {
                code: 20000,
                data: {
                    path: [
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_97.png',
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_144.png',
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_591.png',
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_731.png',
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_1603.png',
                        'image/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e/keyframe_289.png',
                    ],
                },
            }
        },
    },
    {
        url: '/deepfake-finder/detectresult/result/path',
        type: 'get',
        response: config => {
            console.log(config.query)
            return {
                code: 20000,
                data: {
                    // path: 'result/upload/8b314f64634de7ee489406d289f86d67c79e1d77e57c7a7d07e8d6d14dbdc84e.mp4',
                    path: 'result/upload/1.flv'
                },
            }
        },
    },
    {
        url:'/deepfake-finder/detectresult/snapshot',
        type:'get',
        response:config=>{
            console.log(config.query)
            return {
                code:20000,
                data:{
                    path:'screenshot/youtube/2.png'
                }
            }
        }
    }
]
