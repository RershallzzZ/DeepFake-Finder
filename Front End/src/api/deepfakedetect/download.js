import request from '@/utils/request'

export default {
    //page当前页码，size每页查询条数，serachMap条件查询的条件值
    getWebsite() {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/website',
            method: 'get',
        })
    },
    search(page, size, searchMap) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/download/search',
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
            url: 'http://127.0.0.1:5000/deepfake-finder/download/delete',
            method: 'delete',
            data: {
                id,
                website,
            },
        })
    },
    getVideoPath(id, website) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/download/video',
            method: 'get',
            params: {
                id,
                website,
            },
        })
    },

    getScreenshot(id, website) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/download/screenshot',
            method: 'get',
            params: {
                id,
                website,
            },
        })
    },
}
