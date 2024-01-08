const pieChartData = {
    'high|1300-1500': 1,
    'medium|1300-1500': 1,
    'low|1500-1700': 1,
    'none|1800-2000': 1,
}

const raddarChartData = {
    'youtube|4': ['@integer(500,1000)'],
    'bilibili|4': ['@integer(500,1000)'],
    'aiqiyi|4': ['@integer(500,1000)'],
}

const barChartData = {
    'politics|3': ['@integer(500,1000)'],
    'entertainment|3': ['@integer(500,1000)'],
    'tech|3': ['@integer(500,1000)'],
    'others|3': ['@integer(500,1000)'],
}

export default [
    {
        url: '/deepfake-finder/resultanalysis/row2/piechart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: pieChartData,
            }
        },
    },
    {
        url: '/deepfake-finder/resultanalysis/row2/barchart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: barChartData,
            }
        },
    },
    {
        url: '/deepfake-finder/resultanalysis/row2/raddarchart',
        type: 'post',
        response: _ => {
            return {
                code: 20000,
                data: raddarChartData,
            }
        },
    },
]
