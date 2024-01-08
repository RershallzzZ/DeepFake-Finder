import request from '@/utils/request'

export function getProfile() {
    return request({
        url:'http://127.0.0.1:5000/deepfake-finder/profile',
        // url:'/deepfake-finder/profile',
        method:'get'
    })
}

export function getLineChartData() {
    return request({
        url:'http://127.0.0.1:5000/deepfake-finder/dashboard/linechart',
        method:'get',
    })
}
export function getPieChartData() {
    return request({
        url:'http://127.0.0.1:5000/deepfake-finder/dashboard/piechart',
        method:'get',
    })
}
export function getBarChartData() {
    return request({
        url:'http://127.0.0.1:5000/deepfake-finder/dashboard/barchart',
        method:'get',
    })
}
export function getRaddarChartData() {
    return request({
        url:'http://127.0.0.1:5000/deepfake-finder/dashboard/raddarchart',
        method:'get',
    })
}