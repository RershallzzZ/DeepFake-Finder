import request from '@/utils/request'

export default {
    search(page, size, searchMap) {
        return request({
            // url: '/deepfake-finder/earlywarning/config/list/search',
            url: 'http://127.0.0.1:5000/deepfake-finder/earlywarning/config/list/search',
            method: 'post',
            data: {
                page,
                size,
                searchMap,
            },
        })
    },
    add(pojo) {
        return request({
            // url: '/deepfake-finder/earlywarning/config',
            url: 'http://127.0.0.1:5000/deepfake-finder/earlywarning/config',
            method: 'post',
            data: pojo,
        })
    },
    getWebsiteOption() {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler/website',
            method: 'get',
        })
    },
    // 查询
    getById(id) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/earlywarning/config',
            // url: '/deepfake-finder/earlywarning/config',
            method: 'get',
            params: {
                id,
            },
        })
    },

    // 编辑
    update(pojo) {
        return request({
            // url: '/deepfake-finder/earlywarning/config',
            url: 'http://127.0.0.1:5000/deepfake-finder/earlywarning/config',
            method: 'put',
            data: pojo,
        })
    },

    //删除
    deleteById(id) {
        return request({
            // url: '/deepfake-finder/earlywarning/config',
            url: 'http://127.0.0.1:5000/deepfake-finder/earlywarning/config',
            method: 'delete',
            data: {
                id,
            },
        })
    },
}
