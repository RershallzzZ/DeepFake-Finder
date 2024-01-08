import request from '@/utils/request'


export function getBarChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row3/barchart',
        // url: '/deepfake-finder/resultanalysis/row3/barchart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}

export function getWordCloudData(searchMap) {
    return request({
        // url: '/deepfake-finder/resultanalysis/row3/wordcloud',
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row3/wordcloud',
        method: 'post',
        data: {
            searchMap,
        }
    })
}
