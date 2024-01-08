const barChartData = {
    'videoTitle|10': ['@ctitle()'],
    'youtube|10': ['@integer(500,1000)'],
    'bilibili|10': ['@integer(500,1000)'],
    'aiqiyi|10': ['@integer(500,1000)'],
}
const wordCloudData = {
    'list|100': [
        {
            name: '@ctitle()',
            value: '@integer(300,1000)',
        },
    ],
}

export default [
    {
        url: '/deepfake-finder/resultanalysis/row3/barchart',
        type: 'post',
        response: config => {
            const website = config.body.searchMap.website
            if (website.length == 0 || website.length == 2) {
                return {
                    code: 20000,
                    data: {
                        websites: ['youtube', 'bilibili'],
                        videoTitle: [
                            'DeepFake',
                            '换脸',
                            'Trump',
                            '刘亦菲',
                            'Obama',
                            '迪丽热巴',
                            '杨幂',
                            '人工智能',
                            'Video',
                            'AI',
                        ].reverse(),
                        youtube: [285, 12, 200, 110, 87, 32, 22, 22, 25, 10].reverse(),
                        bilibili: [245, 270, 15, 31, 20, 54, 32, 22, 15, 12].reverse(),
                    },
                }
            } else if (website[0] == 'youtube') {
                return {
                    code: 20000,
                    data: {
                        websites: ['youtube'],
                        videoTitle: [
                            'DeepFake',
                            'Trump',
                            '刘亦菲',
                            'Obama',
                            '迪丽热巴',
                            'Video',
                            '杨幂',
                            '人工智能',
                            'AI',
                            'Donald',
                        ].reverse(),
                        youtube: [285, 200, 110, 87, 32, 22, 22, 20, 10, 5].reverse(),
                    },
                }
            } else if (website[0] == 'bilibili') {
                return {
                    code: 20000,
                    data: {
                        websites: ['bilibili'],
                        videoTitle: [
                            '换脸',
                            'DeepFake',
                            '刘亦菲',
                            '迪丽热巴',
                            '杨幂',
                            '人工智能',
                            'Obama',
                            'Video',
                            'Trump',
                            'AI',
                        ].reverse(),
                        bilibili: [270, 245, 54, 33, 32, 22, 20, 15, 15, 12].reverse(),
                    },
                }
            }
        },
    },
    {
        url: '/deepfake-finder/resultanalysis/row3/wordcloud',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: wordCloudData,
            }
        },
    },
]
