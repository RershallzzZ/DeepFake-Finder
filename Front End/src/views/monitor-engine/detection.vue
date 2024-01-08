<template>
    <div class="app-container">
        <el-row style="" :gutter="20">
            <!-- 选择检测方式、开始检测 -->
            <el-col :xs="24" :sm="24" :lg="8">
                <span>请选择检测方式:</span>
                <el-select v-model="detectType" placeholder="默认为快速检测" style="margin-left:1%;width:30%">
                    <el-option
                        v-for="option in detectionTypeOptions"
                        :key="option.type"
                        :label="option.name"
                        :value="option.type"
                    ></el-option>
                </el-select>
                <el-button type="primary" icon="el-icon-aim" @click="manualDetect" style="margin-left:5%">
                    开始检测
                </el-button>
            </el-col>
            <!-- 条件查询 -->
            <el-col :xs="24" :sm="24" :lg="11">
                <el-input
                    v-model="searchMap.title"
                    placeholder="请输入关键词"
                    style="width:40%"
                    @keyup.native.enter="fetchData"
                ></el-input>
                <el-select v-model="searchMap.website" placeholder="视频网站名" style="width:30%;margin-left:3%">
                    <el-option
                        v-for="item in websiteOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                    ></el-option>
                </el-select>
                <el-button type="primary" icon="el-icon-search" @click="fetchData" style="margin-left:5%">
                    搜索
                </el-button>
            </el-col>
            <!-- 自动检测 -->
            <el-col :xs="24" :sm="24" :lg="5" style="margin-top:10px">
                <span>是否开启自动检测</span>
                <el-switch v-model="autoDetectSwitch" @change="autoDetect"></el-switch>
            </el-col>
        </el-row>

        <!-- 需检测视频数据 -->
        <el-table
            :data="list"
            ref="multipleTable"
            height="500"
            border
            style="width: 100%;margin-bottom:1%;margin-top:1.5%"
            
            @selection-change="handleSelectionChange"
            v-loading="listLoading"
        >
            <el-table-column type="selection" width="50" align="center" :selectable="checkSelectable"></el-table-column>
            <el-table-column prop="state" label="是否已检测" align="center" sortable width="120">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.state | stateTagFilter">{{ scope.row.state | stateFilter }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="analyzed" label="疑似程度" sortable width="120" align="center">
                <template slot-scope="scope">
                    <el-tag :type="scope.row.analyzed | analyzedTagFilter" effect="dark">
                        {{ scope.row.analyzed | analyzedFilter }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="crawl_time" sortable label="采集时间" align="center" width="160px"></el-table-column>
            <el-table-column prop="title" label="视频名称" align="center"></el-table-column>
            <el-table-column prop="url" label="视频地址" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="row.url" target="_blank">{{ row.url }}</el-link>
                </template>
            </el-table-column>
            <el-table-column prop="upload_time" label="视频发布时间" align="center" width="130"></el-table-column>
            <el-table-column prop="duration" label="视频时长" align="center" width="80"></el-table-column>
            <el-table-column prop="category" label="视频类型" align="center" width="80"></el-table-column>
        </el-table>

        <!-- 分页功能 -->
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[10, 20, 30]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
        ></el-pagination>
    </div>
</template>

<script>
import detectionApi from '@/api/deepfakedetect/monitorengine/detection'

// 检测类型
const detectionTypeOptions = [{ type: 1, name: '快速检测' }, { type: 2, name: '深度检测' }]

//状态类型
const stateOptions = [{ type: -1, name: '待检测' }, { type: 0, name: '检测中' }, { type: 1, name: '已检测' }]

//状态对应标签
const stateTagOptions = [{ state: -1, tag: 'danger' }, { state: 0, tag: 'warning' }, { state: 1, tag: 'success' }]

//疑似程度类型
const analyzedOptions = [
    { type: '0', name: '未知' },
    { type: '1', name: '无' },
    { type: '2', name: '低' },
    { type: '3', name: '中' },
    { type: '4', name: '高' },
]

//疑似程度对应标签
const analyzedTagOptions = [
    { analyzed: '0', tag: 'info' },
    { analyzed: '1', tag: 'success' },
    { analyzed: '2', tag: '' },
    { analyzed: '3', tag: 'warning' },
    { analyzed: '4', tag: 'danger' },
]

export default {
    name: 'DetectionConfiguration',
    data() {
        return {
            list: [],
            total: 0,
            listLoading: false,
            currentPage: 1, //当前页码
            pageSize: 10, //每页显示10条数据
            stateOptions,
            detectionTypeOptions,
            stateTagOptions,
            analyzedOptions,
            dialogFormVisible: false, //控制对话框
            searchMap: {
                title: '',
                website: 'youtube',
            },
            websiteOptions: [],
            detectType: 1,
            autoDetectSwitch: false,
            multipleSelection: [],
        }
    },

    created() {
        this.fetchData()
    },

    components: {},

    filters: {
        stateFilter(state) {
            const stateObj = stateOptions.find(obj => obj.type == state)
            return stateObj ? stateObj.name : null
        },
        stateTagFilter(state) {
            const tagObj = stateTagOptions.find(obj => obj.state == state)
            return tagObj ? tagObj.tag : null
        },
        analyzedFilter(analyzed) {
            const analyzedObj = analyzedOptions.find(obj => obj.type == analyzed)
            return analyzedObj ? analyzedObj.name : null
        },
        analyzedTagFilter(analyzed) {
            const tagObj = analyzedTagOptions.find(obj => obj.analyzed == analyzed)
            return tagObj ? tagObj.tag : null
        },
    },

    methods: {
        fetchData() {
            this.listLoading = true
            detectionApi.getWebsite().then(response => {
                this.websiteOptions = response.data.websiteList
            })
            detectionApi.search(this.currentPage, this.pageSize, this.searchMap).then(response => {
                console.log('fetch data', this.searchMap, response.data.list)
                this.total = response.data.total
                this.list = response.data.list
                setTimeout(() => {
                    this.listLoading = false
                }, 1 * 1000)
            })
        },
        checkSelectable(row) {
            return row.state != 0
        },

        //当每页显示条数改变后，被触发，val是最新的每页显示条数
        handleSizeChange(val) {
            this.pageSize = val
            this.fetchData()
        },

        //当页码改变后，被触发，val是最新的页码
        handleCurrentChange(val) {
            this.currentPage = val
            this.fetchData()
        },

        handleSelectionChange(val) {
            this.multipleSelection = val
            console.log(this.multipleSelection)
        },

        //开始手动检测
        manualDetect() {
            if (!this.multipleSelection.length) {
                this.$message({
                    showClose: true,
                    message: '请选择视频再开始检测',
                    type: 'error',
                })
            } else {
                this.$message({
                    showClose: true,
                    message: '开始检测视频',
                    type: 'success',
                })
                const id = []
                for (let i = 0; i < this.multipleSelection.length; i++) {
                    this.multipleSelection[i].state = 0
                    id.push(this.multipleSelection[i].id)
                }
                detectionApi.detectManual(id, this.detectType, this.searchMap.website, JSON.stringify(id)).then(response => {
                    this.$message({
                        showClose: true,
                        message: response.message,
                        type: 'success',
                    })
                })
                this.$refs.multipleTable.clearSelection()
            }
        },

        //开启自动检测
        autoDetect(callback) {
            console.log('自动检测开关', callback)
            if (callback) {
                detectionApi.detectAutoBegin().then(response => {
                    this.$message({
                        showClose: true,
                        message: response.data,
                        type: 'success',
                    })
                })
                for(let i=0;i<this.list.length;i++) {
                    this.list[i].state = 0
                }
            } else {
                detectionApi.detectAutoStop().then(response => {
                    this.$message({
                        showClose: true,
                        message: response.data,
                        type: 'error',
                    })
                })
            }
        },
    },
}
</script>

<style>
.el-table th,
.el-table td {
    text-align: center;
}
</style>
