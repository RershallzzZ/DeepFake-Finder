const barChartData = {
    'author|10': ['@cname()'],
    "count|10": ["@integer(500,1000)"],
    'website|10':[{
        "websitename|1":['Youtube','bilibili','爱奇艺']
    }]
}
const wordCloudData = {
    "list|100":[{
        'name': '@cname()',
        'value': "@integer(300,1000)"
    }]
}

export default [

    {
        url: '/deepfake-finder/resultanalysis/row4/barchart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: barChartData,
            }
        },
    },
    {
        url: '/deepfake-finder/resultanalysis/row4/wordcloud',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: wordCloudData,
            }
        },
    },

]
