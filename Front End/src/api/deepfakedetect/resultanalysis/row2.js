import request from '@/utils/request'

export function getPieChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row2/piechart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}

export function getBarChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row2/barchart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}

export function getRaddarChartData(searchMap) {
    return request({
        url: 'http://127.0.0.1:5000/deepfake-finder/resultanalysis/row2/raddarchart',
        method: 'post',
        data: {
            searchMap,
        }
    })
}