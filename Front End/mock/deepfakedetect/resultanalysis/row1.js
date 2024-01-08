const lineChartData = {
    year: [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
    'deepfakeVideo|10': ['@integer(150, 200)'],
    'downloadVideo|10': ['@integer(200, 250)'],
}

const barChartData = {
    duration: ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上'],
    'deepfakeVideo|5': ['@integer(150, 200)'],
    'downloadVideo|5': ['@integer(200, 250)'],
}

export default [
    {
        url: '/deepfake-finder/resultanalysis/row1/linechart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: lineChartData,
            }
        },
    },
    {
        url: '/deepfake-finder/resultanalysis/row1/barchart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: barChartData,
            }
        },
    }
]
