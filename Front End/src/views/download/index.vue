<template>
    <div class="app-container">
        <el-form :inline="true" :model="searchMap" ref="searchForm">
            <el-form-item prop="title">
                <el-input
                    v-model="searchMap.title"
                    placeholder="请输入关键词"
                    @keyup.native.enter="fetchData"
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
                    <!-- <el-option label="Youtube" value="youtube"></el-option> -->
                    <!-- <el-option label="bilibili" value="bilibili"></el-option> -->
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button icon="el-icon-search" type="primary" @click="fetchData">查询</el-button>
                <el-button
                    type="primary"
                    @click="resetForm('searchForm')"
                    class="filter-item"
                    icon="el-icon-s-operation"
                >
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
            <el-table-column prop="crawl_time" sortable label="采集时间" align="center" width="160px"></el-table-column>
            <el-table-column prop="upload_time" sortable label="视频发布时间" align="center" width="130"></el-table-column>
            <el-table-column prop="title" label="视频名称" align="center"></el-table-column>
            <el-table-column prop="url" label="视频地址" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="row.url" target="_blank">{{ row.url }}</el-link>
                </template>
            </el-table-column>

            <el-table-column prop="duration" label="视频时长" align="center" width="80"></el-table-column>
            <el-table-column prop="category" label="视频类型" align="center" width="80"></el-table-column>
            <el-table-column prop="download" label="下载情况" align="center" width="100">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.download | tagIsDownloadFilter">
                        {{ scope.row.download | isDownloadFilter }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" align="center" width="220px">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="handleScreenshot(scope.row.id)">
                        快照
                    </el-button>
                    <el-button
                        :disabled="!scope.row.download"
                        size="mini"
                        type="primary"
                        @click="handleVideo(scope.row)"
                    >
                        播放
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
        <el-dialog
            :title="'爬取视频地址：' + currentVideoSource"
            :center="true"
            :visible.sync="dialogVisible"
            :before-close="handleVideoClose"
        >
            <video id="videoElement" controls ref="dialogVideo"></video>
        </el-dialog>
        <el-dialog width="1000px" title="网页快照" :center="true" :visible.sync="dialogScreenshotVisible">
            <viewer :images="images" class="images">
                <img :src="src" class="image" v-for="(src, src_index) in images" :key="src_index" />
            </viewer>
        </el-dialog>
    </div>
</template>

<script>
import downloadApi from '@/api/deepfakedetect/download'
import flvjs from 'flv.js'
const isDownloadOption = [{ type: 0, name: '未下载' }, { type: 1, name: '已下载' }]
export default {
    name: 'Download',
    data() {
        return {
            list: [],
            images: [],
            websiteOptions: [],
            total: 0,
            currentPage: 1,
            pageSize: 10,
            searchMap: {
                title: '',
                website: 'youtube',
            },
            listLoading: false,
            dialogVisible: false,
            dialogScreenshotVisible: false,
            currentVideoSource: '',
            flvPlayer: {},
        }
    },
    created() {
        this.fetchData()
    },
    filters: {
        isDownloadFilter(type) {
            //过滤器中无法使用this

            const isDownloadObj = isDownloadOption.find(obj => obj.type == type)
            return isDownloadObj ? isDownloadObj.name : null
        },
        tagIsDownloadFilter(tagType) {
            const tagTypeMap = [
                {
                    type: 0,
                    name: 'info',
                },
                {
                    type: 1,
                    name: 'success',
                },
            ]
            const tagTypeObj = tagTypeMap.find(obj => obj.type == tagType)
            return tagTypeObj ? tagTypeObj.name : null
        },
    },
    methods: {
        fetchData() {
            this.listLoading = true
            downloadApi.getWebsite().then(response => {
                this.websiteOptions = response.data.websiteList
            })
            downloadApi.search(this.currentPage, this.pageSize, this.searchMap).then(response => {
                this.list = response.data.list
                this.total = response.data.total
                setTimeout(() => {
                    this.listLoading = false
                }, 1 * 1000)
            })
            console.log(this.list)
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
        resetForm(formName) {
            this.$refs[formName].resetFields()
            // this.fetchData()
        },
        handleDownload() {
            import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['采集时间', '视频名称', '视频地址', '视频发布时间', '视频时长', '视频类型', '下载状况']
                const filterVal = ['crawl_time', 'title', 'url', 'upload_time', 'duration', 'category', 'download']
                const data = this.formatJson(filterVal)
                excel.export_json_to_excel({
                    header: tHeader,
                    data,
                    filename: '视频采集导出表',
                })
            })
        },
        formatJson(filterVal) {
            return this.list.map(v =>
                filterVal.map(j => {
                    if (j === 'download') {
                        const isDownloadObj = isDownloadOption.find(obj => obj.type === v[j])
                        return isDownloadObj ? isDownloadObj.name : null
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
                    downloadApi.deleteById(id, this.searchMap.website).then(response => {
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
        handleVideo(row) {
            this.currentVideoSource = row.url
            if (row.download) {
                this.dialogVisible = true
                downloadApi.getVideoPath(row.id, this.searchMap.website).then(response => {
                    console.log(response)
                    const split = response.data.path.includes('/') ? '/' : '\\'
                    const temp = response.data.path.split(split)
                    const videoType = temp[temp.length - 1].split('.')[1]
                    this.$nextTick(() => {
                        if (flvjs.isSupported()) {
                            console.log(videoType)
                            var videoElement = document.getElementById('videoElement')
                            this.flvPlayer = flvjs.createPlayer({
                                type: videoType,
                                url: 'http://127.0.0.1:5000/' + response.data.path,
                            })
                            this.flvPlayer.attachMediaElement(videoElement)
                            this.flvPlayer.load()
                            // flvPlayer.play()
                        }
                    })
                })
            }
        },
        handleVideoClose(done) {
            this.$nextTick(() => {
                this.flvPlayer.destroy()
                done()
            })
        },
        handleScreenshot(id) {
            this.dialogScreenshotVisible = true
            downloadApi.getScreenshot(id, this.searchMap.website).then(response => {
                var images = []
                images.push('http://127.0.0.1:5000/' + response.data.path)
                this.images = images
            })
        },
    },
}
</script>
<style scoped>
video {
    height: 400px;
    width: 100%;
}

.images {
    display: flex;
    margin: 0 auto;
    width: 100%;
    align-items: center;
    justify-content: center;
}
.image {
    width: 80%;
    height: 400px;
    border-radius: 3px;
    border: 6px solid white;
    padding: 1px;
    /* margin: 10px; */
    cursor: pointer;
    box-shadow: 1px 1px 5px #333333;
}
</style>
