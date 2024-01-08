import request from '@/utils/request'

export default {
    getWebsite() {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/website',
            method: 'get',
        })
    },
    //page当前页码，size每页查询条数，serachMap条件查询的条件值
    search(page, size, searchMap) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/detectresult/search',
            method: 'post',
            data: {
                page,
                size,
                searchMap,
            },
        })
    },
    deleteById(id, website) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/detectresult/delete',
            method: 'delete',
            data: {
                id,
                website,
            },
        })
    },
    getScreenshot(id, website) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/detectresult/screenshot',
            method: 'get',
            params: {
                id,
                website,
            },
        })
    },
    getDetectResult(id, website) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/detectresult/result',
            method: 'get',
            params: {
                id,
                website,
            },
        })
    },
}
