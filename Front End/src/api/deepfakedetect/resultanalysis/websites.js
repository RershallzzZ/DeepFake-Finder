import request from '@/utils/request'

export default {
    getWebsite() {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/website',
            method: 'get',
        })
    },
}
