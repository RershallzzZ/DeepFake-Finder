<template>
    <div class="app-container">
        <!-- <el-button type="primary" round @click="test"></el-button> -->
        <h1 style="text-align:center;">上传视频检测</h1>
        <div class="upload_wrapper">
            <ele-upload-video
                class="upload"
                :fileSize="20"
                @error="handleUploadError"
                :responseFn="handleResponse"
                action="http://127.0.0.1:5000/upload"
                v-model="video.url"
            />
        </div>
        <div class="button_wrapper">
            <el-button
                type="primary"
                :disabled="loadingDeep"
                :loading="loadingFast"
                round
                v-if="video.url"
                @click="handleFastDetect"
            >
                快速检测
            </el-button>
            <el-button
                type="primary"
                :disabled="loadingFast"
                :loading="loadingDeep"
                round
                v-if="video.url"
                @click="handleDeepDetect"
            >
                深度检测
            </el-button>
        </div>

        <template v-if="isShowFastDetectResult && video.url">
            <h1 style="text-align:center;">
                快速检测结果:
                <span :class="[resultStyle[fastDetectAnalyzed-1]]">
                    {{ fastDetectAnalyzed | analyzedFilter }}
                </span>
            </h1>
            <div class="image_wrapper">
                <el-row :gutter="32" v-for="(item, item_index) in images" :key="item_index">
                    <viewer :images="images" class="images">
                        <el-col :xs="24" :sm="24" :lg="8" v-for="(src, src_index) in item" :key="src_index">
                            <img :src="src" class="image" />
                        </el-col>
                    </viewer>
                </el-row>
            </div>
            <div class="button_wrapper">
                <el-button type="primary" @click="dialogVisible = true">
                    查看全部关键帧
                </el-button>
            </div>
            <el-dialog title="全部关键帧检测结果" :center="true" :visible.sync="dialogVisible" width="80%">
                <div class="carousel_wrapper">
                    <carousel :scrollPerPage="true" :perPageCustom="[[480, 2], [768, 3]]">
                        <slide v-for="(src, src_index) in imagesAll" :key="src_index">
                            <img :src="src" style="width: 500px ;max-width: 100%;" />
                        </slide>
                    </carousel>
                </div>
            </el-dialog>
        </template>
        <template v-if="isShowDeepDetectResult && video.url">
            <h1 style="text-align:center;">
                深度检测结果:
                <span :class="[resultStyle[deepDetectAnalyzed-1]]">
                    {{ deepDetectAnalyzed | analyzedFilter }}
                </span>
            </h1>
            <div class="video_wrapper">
                <video :src="resultVideo" controls ref="Video">
                    您的浏览器不支持播放该视频！
                </video>
            </div>
        </template>
    </div>
</template>

<script>
import EleUploadVideo from 'vue-ele-upload-video'
import uploadApi from '@/api/deepfakedetect/upload'
import { Carousel, Slide } from 'vue-carousel'
const analyzedOption = [
    { type: 1, name: '无疑似' },
    { type: 2, name: '低疑似' },
    { type: 3, name: '中疑似' },
    { type: 4, name: '高疑似' },
]
export default {
    name: 'UploadVideo',
    data() {
        return {
            // 上传时需要携带后台请求的token
            token: 'xxxx',
            video: {
                url: null,
                path: '',
                filename: '',
            },
            dialogVisible: false,
            images: [],
            imagesAll: [],
            isShowFastDetectResult: false,
            isShowDeepDetectResult: false,
            fastDetectAnalyzed: 0,
            deepDetectAnalyzed: 0,
            resultVideo: '',
            loadingFast: false,
            loadingDeep: false,
            resultStyle: ['none', 'low', 'middle', 'high'],
        }
    },
    filters: {
        analyzedFilter(type) {
            //过滤器中无法使用this
            const analyzedObj = analyzedOption.find(obj => obj.type == type)
            return analyzedObj ? analyzedObj.name : null
        },
    },
    methods: {
        handleUploadError(error) {
            console.log('error', error)
            this.loading = false
        },
        handleResponse(response) {
            this.isShowFastDetectResult = false
            this.isShowDeepDetectResult = false
            this.video.path = response.data.path
            const split = this.video.path.includes('/') ? '/' : '\\'
            const temp = this.video.path.split(split)
            this.video.filename = temp[temp.length - 1]
            return 'http://127.0.0.1:5000/' + this.video.path
        },
        handleFastDetect() {
            this.loadingFast = true
            uploadApi.detectVideo(this.video, 1).then(response => {
                const list = response.data.result.image_6
                var images = []
                for (var i = 0; i < list.length; i = i + 3) {
                    var temp = []
                    for (var j = i; j < i + 3; j++) {
                        temp.push('http://127.0.0.1:5000/' + list[j])
                    }
                    images.push(temp)
                }
                this.images = images
                this.imagesAll = response.data.result.image
                for (var i = 0; i < this.imagesAll.length; i++) {
                    this.imagesAll[i] = 'http://127.0.0.1:5000/' + this.imagesAll[i]
                }

                this.isShowFastDetectResult = true
                this.loadingFast = false
                this.fastDetectAnalyzed = response.data.result.fastAnalyzed
            })
        },
        handleDeepDetect() {
            this.loadingDeep = true
            uploadApi.detectVideo(this.video, 2).then(response => {
                this.resultVideo = 'http://127.0.0.1:5000/' + response.data.result.resultVideo
                this.isShowDeepDetectResult = true
                this.loadingDeep = false
                this.deepDetectAnalyzed = response.data.result.deepAnalyzed
            })
        },
        test() {
            console.log(this.video)
        },
    },
    components: {
        EleUploadVideo,
        Carousel,
        Slide,
    },
}
</script>

<style scoped>
.upload_wrapper {
    display: flex;
    /* margin: 0 auto; */
    /* width: 100%; */
    align-items: center;
    justify-content: center;
}
.upload {
    margin-top: 10px;
}
.button_wrapper {
    display: flex;
    /* margin: 0 auto; */
    /* width: 100%; */
    align-items: center;
    justify-content: center;
}
.el-button {
    margin-top: 25px;
    margin-bottom: 20px;
}
.image_wrapper {
    /* display: flex; */
    /* margin: 0 auto; */
    /* width: 100%; */
    align-items: center;
    justify-content: center;
}
.images {
    display: flex;
    margin: 0 auto;
    width: 1000px;
    justify-content: space-between;
}
.image {
    width: 265px;
    height: 180px;
    border-radius: 3px;
    border: 6px solid white;
    padding: 1px;
    margin: 10px;
    cursor: pointer;
    box-shadow: 1px 1px 5px #333333;
}
.video_wrapper {
    display: flex;
    margin: 20px;
    /* margin: 0 auto; */
    /* width: 100%; */
    align-items: center;
    justify-content: center;
}
video {
    height: 400px;
    /* width: 40%; */
}
.carousel_wrapper {
    /* margin: 0 auto; */
    /* width: 60%;*/
    /* position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%; */
}
.VueCarousel-slide {
    /* position: relative; */
    background: #333333;
    font-family: Arial;
    font-size: 24px;

    text-align: center;
    min-height: 100px;
    align-items: center;
    justify-content: center;
}
.none {
    color: #67c23a;
}
.low {
    color: #409EFF;
}
.middle{
    color: #E6A23C;
}
.high{
    color: #F56C6C;
}
</style>
