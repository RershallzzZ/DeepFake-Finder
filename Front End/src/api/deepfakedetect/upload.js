import request from '@/utils/request'

export default {
    detectVideo(video,detectMode) {
        return request({
            url: 'http://127.0.0.1:5000/upload/detect',
            method: 'post',
            data:{
                video,
                detectMode
            }
        })
    },
}
