<template>
    <div class="app-container">
        <el-form :inline="true" :model="searchMap" ref="searchForm">
            <el-form-item prop="analyzed">
                <el-select v-model="searchMap.analyzed" placeholder="请选择疑似程度" style="width: 160px">
                    <el-option
                        v-for="option in analyzedOption"
                        :key="option.type"
                        :label="option.name"
                        :value="option.type"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="title">
                <el-input
                    v-model="searchMap.title"
                    @keyup.enter.native="fetchData"
                    placeholder="请输入关键词"
                    style="width: 200px"
                ></el-input>
            </el-form-item>
            <el-form-item prop="website">
                <el-select v-model="searchMap.website" placeholder="视频网站名" style="width: 180px">
                    <el-option
                        v-for="item in websiteOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button icon="el-icon-search" type="primary" @click="fetchData">查询</el-button>
                <el-button type="primary" @click="$refs.searchForm.resetFields()" icon="el-icon-s-operation">
                    重置
                </el-button>
                <el-button type="primary" icon="el-icon-download" @click="handleDownload">
                    导出
                </el-button>
            </el-form-item>
        </el-form>
        <el-table
            
            :data="list"
            height="500"
            style="width: 100%;margin-bottom:1%"
            border
            v-loading="listLoading"
        >
            <el-table-column type="index" label="序号" align="center" width="50px"></el-table-column>
            <el-table-column sortable prop="analyzed" label="疑似度" align="center" width="100">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.analyzed | analyzedTagFilter">
                        {{ scope.row.analyzed | analyzedFilter }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="crawl_time" sortable label="采集时间" align="center" width="200px"></el-table-column>
            <el-table-column
                prop="upload_time"
                sortable
                label="视频发布时间"
                align="center"
                width="130"
            ></el-table-column>
            <el-table-column prop="title" label="视频标题" align="center"></el-table-column>
            <el-table-column prop="url" label="视频地址" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="row.url" target="_blank">{{ row.url }}</el-link>
                </template>
            </el-table-column>

            <el-table-column prop="duration" label="视频时长" align="center" width="80"></el-table-column>
            <el-table-column prop="category" label="视频类型" align="center" width="80"></el-table-column>

            <el-table-column label="操作" align="center" width="220px">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="handleScreenshot(scope.row.id)">
                        快照
                    </el-button>
                    <el-button size="mini" type="primary" @click="handleDialog(scope.row)">
                        查看
                    </el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.row.id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="[10, 20, 30, 40]"
            :page-size.sync="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
        ></el-pagination>
        <el-dialog width="1000px" title="网页快照" :center="true" :visible.sync="dialogScreenshotVisible">
            <viewer :images="screenshot" class="screenshot_wrapper">
                <img :src="src" class="screenshot" v-for="(src, src_index) in screenshot" :key="src_index" />
            </viewer>
        </el-dialog>

        <el-dialog width="1000px" title="检测结果" :center="true" :visible.sync="dialogVisible">
            <template v-if="isShowFastDetectResult">
                <h1 style="text-align:center;">
                    快速检测结果:
                    <span :class="[resultStyle[fastDetectAnalyzed - 1]]">
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
                    <el-button class="detect_button" type="primary" @click="dialogAllImageVisible = true">
                        查看全部关键帧
                    </el-button>
                </div>
                <el-dialog title="全部关键帧检测结果" :center="true" :visible.sync="dialogAllImageVisible" width="80%">
                    <div class="carousel_wrapper">
                        <carousel :scrollPerPage="true" :perPageCustom="[[480, 2], [768, 3]]">
                            <slide v-for="(src, src_index) in imagesAll" :key="src_index">
                                <img :src="src" style="width: 500px ;max-width: 100%;" />
                            </slide>
                        </carousel>
                    </div>
                </el-dialog>
            </template>
            <template v-if="isShowDeepDetectResult">
                <h1 style="text-align:center;">
                    深度检测结果:
                    <span :class="[resultStyle[deepDetectAnalyzed - 1]]">
                        {{ deepDetectAnalyzed | analyzedFilter }}
                    </span>
                </h1>
                <div class="video_wrapper">
                    <video :src="resultVideo" controls ref="Video">
                        您的浏览器不支持播放该视频！
                    </video>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import detectResultApi from '@/api/deepfakedetect/detectresult'
import { Carousel, Slide } from 'vue-carousel'
const analyzedOption = [
    { type: 1, name: '无疑似' },
    { type: 2, name: '低疑似' },
    { type: 3, name: '中疑似' },
    { type: 4, name: '高疑似' },
]
export default {
    name: 'Detectresult',
    data() {
        return {
            images: [],
            imagesAll: [],
            screenshot: [],
            websiteOptions: [],
            list: [],
            total: 0,
            currentPage: 1,
            pageSize: 10,
            searchMap: {
                title: '',
                analyzed: null,
                website: 'youtube',
            },
            websiteOptions: [],
            listLoading: false,
            dialogVisible: false,
            analyzedOption,
            dialogScreenshotVisible: false,
            isShowFastDetectResult: false,
            isShowDeepDetectResult: false,
            fastDetectAnalyzed: 0,
            deepDetectAnalyzed: 0,
            resultVideo: '',
            dialogAllImageVisible: false,
            resultStyle: ['none', 'low', 'middle', 'high'],
        }
    },
    components: { Carousel, Slide },
    created() {
        this.fetchData()
    },
    filters: {
        analyzedFilter(type) {
            //过滤器中无法使用this

            const analyzedObj = analyzedOption.find(obj => obj.type === type)
            return analyzedObj ? analyzedObj.name : null
        },
        analyzedTagFilter(tagType) {
            const tagTypeMap = [
                {
                    type: 1,
                    name: 'success',
                },
                {
                    type: 2,
                    name: '',
                },
                {
                    type: 3,
                    name: 'warning',
                },
                {
                    type: 4,
                    name: 'danger',
                },
            ]
            const tagTypeObj = tagTypeMap.find(obj => obj.type === tagType)
            return tagTypeObj ? tagTypeObj.name : null
        },
    },
    methods: {
        fetchData() {
            this.listLoading = true
            detectResultApi.getWebsite().then(response => {
                this.websiteOptions = response.data.websiteList
            })
            detectResultApi.search(this.currentPage, this.pageSize, this.searchMap).then(response => {
                this.list = response.data.list
                this.total = response.data.total
                setTimeout(() => {
                    this.listLoading = false
                }, 1 * 1000)
            })
        },
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`)
            this.pageSize = val
            this.fetchData()
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`)
            this.currentPage = val
            this.fetchData()
        },
        handleDownload() {
            import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['疑似度', '采集时间', '视频名称', '视频地址', '视频发布时间', '视频时长', '视频类型']
                const filterVal = ['analyzed', 'crawl_time', 'title', 'url', 'upload_time', 'duration', 'category']
                const data = this.formatJson(filterVal)
                excel.export_json_to_excel({
                    header: tHeader,
                    data,
                    filename: '检测结果导出表',
                })
            })
        },
        formatJson(filterVal) {
            return this.list.map(v =>
                filterVal.map(j => {
                    if (j === 'analyzed') {
                        const analyzedObj = analyzedOption.find(obj => obj.type === v[j])
                        return analyzedObj ? analyzedObj.name : null
                    } else {
                        return v[j]
                    }
                })
            )
        },
        handleDelete(id) {
            console.log('删除', id)
            this.$confirm('确认删除这条记录吗？', '提示', {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
            })
                .then(() => {
                    console.log('确认')
                    detectResultApi.deleteById(id, this.searchMap.website).then(response => {
                        this.$message({
                            type: response.flag ? 'success' : 'error',
                            message: response.message,
                        })
                        if (response.flag) {
                            this.fetchData()
                        }
                    })
                })
                .catch(() => {
                    //不用理会 该回调函数会自动关闭弹窗
                    console.log('取消')
                })
        },
        handleDialog(row) {
            this.isShowFastDetectResult = false
            this.isShowDeepDetectResult = false
            detectResultApi.getDetectResult(row.id, this.searchMap.website).then(response => {
                if (response.data.image && response.data.image_6) {
                    const list = response.data.image_6
                    console.log('images', list)
                    var images = []
                    for (var i = 0; i < list.length; i = i + 3) {
                        var temp = []
                        for (var j = i; j < i + 3; j++) {
                            temp.push('http://127.0.0.1:5000/' + list[j])
                        }
                        images.push(temp)
                    }
                    this.images = images
                    this.imagesAll = response.data.image
                    for (var i = 0; i < this.imagesAll.length; i++) {
                        this.imagesAll[i] = 'http://127.0.0.1:5000/' + this.imagesAll[i]
                    }
                    this.isShowFastDetectResult = true
                    this.fastDetectAnalyzed = response.data.fastAnalyzed
                }
                if (response.data.resultVideo) {
                    this.resultVideo = 'http://127.0.0.1:5000/' + response.data.resultVideo
                    this.isShowDeepDetectResult = true
                    this.deepDetectAnalyzed = response.data.deepAnalyzed
                }
            })
            this.dialogVisible = true
        },
        handleScreenshot(id) {
            this.dialogScreenshotVisible = true
            detectResultApi.getScreenshot(id, this.searchMap.website).then(response => {
                var screenshot = []
                screenshot.push('http://127.0.0.1:5000/' + response.data.path)
                this.screenshot = screenshot
            })
        },
    },
}
</script>

<style scoped>
.button_wrapper {
    display: flex;
    /* margin: 0 auto; */
    /* width: 100%; */
    align-items: center;
    justify-content: center;
}
.detect_button {
    margin-top: 25px;
    margin-bottom: 20px;
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
.screenshot_wrapper {
    display: flex;
    margin: 0 auto;
    width: 100%;
    align-items: center;
    justify-content: center;
}
.screenshot {
    width: 80%;
    height: 400px;
    border-radius: 3px;
    border: 6px solid white;
    padding: 1px;
    /* margin: 10px; */
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
    color: #409eff;
}
.middle {
    color: #e6a23c;
}
.high {
    color: #f56c6c;
}
</style>
