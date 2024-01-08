import request from '@/utils/request'

export default {
    //新增爬虫
    add(pojo) {
        return request({
            // url: '/deepfake-finder/monitorengine/crawler',
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler',
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

    //搜索
    search(page, size, searchMap) {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler/list/search',
            // url: '/deepfake-finder/monitorengine/crawler/list/search',
            method: 'post',
            data: {
                page,
                size,
                searchMap,
            },
        })
    },

    // 查询
    getById(id) {
        return request({
            // url: '/deepfake-finder/monitorengine/crawler',
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler',
            method: 'get',
            params: {
                id,
            },
        })
    },

    // 编辑
    update(pojo) {
        return request({
            // url: '/deepfake-finder/monitorengine/crawler/update',
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler/update',
            method: 'put',
            data: pojo,
        })
    },

    //删除
    deleteById(id) {
        return request({
            // url: '/deepfake-finder/monitorengine/crawler/delete',
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler/delete',
            method: 'delete',
            data: {
                id,
            },
        })
    },

    updateState(id, state) {
        return request({
            // url: '/deepfake-finder/monitorengine/crawler/state',
            url: 'http://127.0.0.1:5000/deepfake-finder/monitorengine/crawler/state',
            method: 'put',
            data: {
                id,
                state,
            },
        })
    },
}
