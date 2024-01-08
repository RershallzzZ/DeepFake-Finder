import request from '@/utils/request'

export function getLineChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row1/linechart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}

export function getBarChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row1/barchart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}
