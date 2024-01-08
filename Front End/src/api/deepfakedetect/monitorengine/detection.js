import request from '@/utils/request'

export default{
    getWebsite() {
        return request({
            url: 'http://127.0.0.1:5000/deepfake-finder/website',
            method: 'get',
        })
    },
    //搜索
    search(page, size, searchMap){
        return request({
            url:'http://127.0.0.1:5000/deepfake-finder/monitorengine/detection/list/search',
            method:'post',
            data:{
                page,
                size,
                searchMap
            }
        })
    },

    //开始手动检测
    detectManual(id, detectType, website, videoList){
        return request({
            url:`http://127.0.0.1:5000/deepfake-finder/monitorengine/detection/manual/${videoList}`,
            method:'post',
            data:{
                id,
                detectType,
                website
            }
        })
    },

    //开始自动检测
    detectAutoBegin(){
        return request({
            url:'/deepfake-finder/monitorengine/detection/auto/begin',
            method:'post'
        })
    },

    //停止自动检测
    detectAutoStop(){
        return request({
            url:'/deepfake-finder/monitorengine/detection/auto/stop',
            method:'post'
        })
    }
}