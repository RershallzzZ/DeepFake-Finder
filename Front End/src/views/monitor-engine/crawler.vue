<template>
    <div class="app-container">
        <!-- 条件查询 -->
        <el-form :inline="true" ref="searchForm" :model="searchMap" class="demo-form-inline" style="margin-top:1%; ">
            <el-form-item>
                <el-button type="primary" icon="el-icon-circle-plus" @click="handleAdd">新增爬虫</el-button>
            </el-form-item>
            <el-form-item prop="keyword">
                <el-input
                    v-model="searchMap.keyword"
                    @keyup.enter.native="fetchData"
                    placeholder="筛选关键词"
                ></el-input>
            </el-form-item>
            <el-form-item prop="state">
                <el-select v-model="searchMap.state" placeholder="请选择爬虫状态" style="width: 180px">
                    <el-option
                        v-for="item in stateOption"
                        :key="item.type"
                        :label="item.name"
                        :value="item.type"
                    ></el-option>
                </el-select>
            </el-form-item>

            <el-form-item>
                <el-button type="primary" icon="el-icon-search" @click="fetchData">
                    搜索
                </el-button>
                <el-button type="primary" @click="$refs.searchForm.resetFields()" icon="el-icon-s-operation">
                    重置
                </el-button>
                <el-button type="primary" icon="el-icon-download" @click="handleDownload">
                    导出
                </el-button>
            </el-form-item>
        </el-form>

        <!-- 爬虫列表数据 -->
        <el-table
            :data="list"
            border
            height="300"
            :default-sort="{ prop: 'state', order: 'descending' }"
            style="width: 100%;margin-bottom:1%"
            v-loading="listLoading"
        >
            <el-table-column type="index" label="序号" align="center" width="50px"></el-table-column>
            <el-table-column prop="state" label="爬虫状态" width="120" align="center" sortable>
                <template slot-scope="scope">
                    <el-tag :type="scope.row.state | spiderStateTagFilter">
                        {{ scope.row.state | spiderStateFilter }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="url" label="监控网站" width="250" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="row.url" target="_blank">{{ row.url }}</el-link>
                </template>
            </el-table-column>
            <el-table-column prop="keyword" label="爬虫关键词" align="center"></el-table-column>
            <el-table-column prop="time" label="是否按时间爬取" align="center" width="120">
                <template slot-scope="scope">
                    <el-tooltip effect="dark" content="表示爬虫是否优先爬取最新上传的视频" placement="top-start">
                        <span>{{ scope.row.time | timeFilter }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="len" label="爬取长度" align="center" width="150">
                <template slot-scope="scope">
                    <el-tooltip effect="dark" :content="tooltipLen(scope.row.len)" placement="top-start">
                        <span>{{ scope.row.len | lenFilter }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="stateControl" label="爬虫控制" align="center" width="250">
                <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="begin(scope.row.id)">开启</el-button>
                    <el-button size="mini" type="warning" @click="pause(scope.row.id)">暂停</el-button>
                    <el-button size="mini" type="danger" @click="stop(scope.row.id)">关闭</el-button>
                </template>
            </el-table-column>
            <el-table-column prop="action" label="操作" width="170" align="center">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="handleEdit(scope.row.id)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="[10, 20, 30]"
            :page-size.sync="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
        ></el-pagination>

        <!-- 弹窗 -->
        <el-dialog title="编辑" :visible.sync="dialogFormVisible" width="450px">
            <el-form :model="pojo" ref="pojoForm" :rules="rules" style="width: 400px">
                <el-form-item label="监控网站地址" prop="url" label-width="120px">
                    <el-select v-model="pojo.url" placeholder="请选择监控网站地址" style="width: 250px;">
                        <el-option
                            v-for="item in websiteOptions"
                            :key="item.url"
                            :label="item.url"
                            :value="item.name"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="爬虫关键词" prop="keyword" label-width="120px">
                    <el-input v-model="pojo.keyword"></el-input>
                </el-form-item>
                <el-form-item label="爬取长度" prop="len" label-width="120px">
                    <el-select v-model="pojo.len" placeholder="爬取长度">
                        <el-option label="长(>30 min)" :value="1"></el-option>
                        <el-option label="中(10~30 min)" :value="2"></el-option>
                        <el-option label="短(<10 min)" :value="3"></el-option>
                        <el-option label="无限制" :value="0"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="是否按照视频发布时间进行爬取" prop="time">
                    <el-switch v-model="pojo.time"></el-switch>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="pojo.id === null ? addData('pojoForm') : updateData('pojoForm')">
                    确 定
                </el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import crawlerApi from '@/api/deepfakedetect/monitorengine/crawler'

const stateOption = [{ type: -1, name: '关闭' }, { type: 0, name: '暂停' }, { type: 1, name: '开启' }]
const timeOptions = [{ src: true, dst: '是' }, { src: false, dst: '否' }]
const lenOptions = [{ type: 0, name: '无' }, { type: 1, name: '长' }, { type: 2, name: '中' }, { type: 3, name: '短' }]
const initPojo = {
    id: null,
    url: '',
    keyword: '',
    time: false,
    len: 0,
}
export default {
    name: 'CrawlerConfiguration',
    data() {
        return {
            list: [],
            timeOptions,
            stateOption,
            lenOptions,
            websiteOptions: [],
            listLoading: false,
            dialogFormVisible: false, //控制对话框
            total: 0,
            currentPage: 1,
            pageSize: 10,
            searchMap: {
                keyword: '',
                state: null,
            },
            pojo: initPojo,
            rules: {
                //校验规则
                url: [{ required: true, message: '监控网站地址不能为空', trigger: 'blur' }],
            },
        }
    },

    created() {
        this.fetchData()
    },

    components: {},

    filters: {
        timeFilter(time) {
            const timeObj = timeOptions.find(obj => obj.src == time)
            return timeObj ? timeObj.dst : null
        },
        spiderStateFilter(state) {
            const stateObj = stateOption.find(obj => obj.type === state)
            return stateObj ? stateObj.name : null
        },
        spiderStateTagFilter(state) {
            const StateMap = [
                {
                    type: 1,
                    name: 'success',
                },
                {
                    type: -1,
                    name: 'danger',
                },
                {
                    type: 0,
                    name: 'warning',
                },
            ]
            const stateObj = StateMap.find(obj => obj.type === state)
            return stateObj ? stateObj.name : null
        },
        lenFilter(len) {
            const lenObj = lenOptions.find(obj => obj.type == len)
            return lenObj ? lenObj.name : null
        },
    },

    methods: {
        fetchData() {
            this.listLoading = true
            crawlerApi.search(this.currentPage, this.pageSize, this.searchMap).then(response => {
                console.log(response.data.list)
                this.list = response.data.list
                this.total = response.data.total
                setTimeout(() => {
                    this.listLoading = false
                }, 1 * 1000)
            })
        },
        tooltipLen(len) {
            if (len == 1) {
                return '长(>30 min)'
            } else if (len == 2) {
                return '中(10~30 min)'
            } else if (len == 3) {
                return '短(<10 min))'
            } else if (len == 0) {
                return '无限制'
            }
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
        //弹出新增窗口
        handleAdd() {
            crawlerApi.getWebsiteOption().then(response => {
                this.websiteOptions = response.data
            })
            this.dialogFormVisible = true
            //this.$nextTick(）是一个异步事件，当渲染结束后，它的回调函数才会被执行
            //弹出窗口打开后需加载DOM，就需要花费一点时间，应当等待加载完DOM后再进行调用resetFields方法重置表单和清除样式
            this.$nextTick(() => {
                this.$refs['pojoForm'].resetFields()
            })
            this.pojo = initPojo
        },

        //提交新增数据
        addData(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    //提交表单
                    crawlerApi.add(this.pojo).then(response => {
                        this.$message({
                            type: 'success',
                            message: '新增爬虫记录成功!',
                        })
                        console.log('this pojo', this.pojo)
                        this.fetchData()
                        this.dialogFormVisible = false
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '新增爬虫记录失败!',
                    })
                    return false
                }
            })
        },

        //打开编辑窗口
        handleEdit(id) {
            this.handleAdd()
            crawlerApi.getById(id).then(response => {
                console.log('handle edit', response)
                this.pojo = response.data
            })
        },

        //提交修改数据
        updateData(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    crawlerApi.update(this.pojo).then(response => {
                        this.$message({
                            type: 'success',
                            message: '更新爬虫记录成功!',
                        })
                        this.fetchData()
                        this.dialogFormVisible = false
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '更新爬虫记录失败!',
                    })
                    return false
                }
            })
        },

        //删除爬虫
        handleDelete(id) {
            console.log('删除', id)
            this.$confirm('确认删除这条记录吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
                .then(() => {
                    //确认
                    crawlerApi.deleteById(id).then(response => {
                        this.$message({
                            type: response.code === 20000 ? 'success' : 'error',
                            message: response.data,
                        })
                        //删除成功，刷新列表数据
                        this.fetchData()
                    })
                })
                .catch(() => {
                    //取消,不用理会
                })
        },

        //开启爬虫
        begin(id) {
            crawlerApi.updateState(id, 1).then(response => {
                console.log('开启爬虫', id)
                this.$message({
                    type: response.code === 20000 ? 'success' : 'error',
                    message: response.data,
                })
                this.fetchData()
            })
        },

        //暂停爬虫
        pause(id) {
            crawlerApi.updateState(id, 0).then(response => {
                console.log('暂停爬虫', id)
                this.$message({
                    type: response.code === 20000 ? 'success' : 'error',
                    message: response.data,
                })
                this.fetchData()
            })
        },

        //关闭爬虫
        stop(id) {
            crawlerApi.updateState(id, -1).then(response => {
                console.log('关闭爬虫', id)
                this.$message({
                    type: response.code === 20000 ? 'success' : 'error',
                    message: response.data,
                })
                this.fetchData()
            })
        },
        handleDownload() {
            import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['爬虫状态', '监控网站', '爬虫关键词', '是否按时间爬取', '爬取长度']
                const filterVal = ['state', 'url', 'keyword', 'time', 'len']
                const data = this.formatJson(filterVal)
                excel.export_json_to_excel({
                    header: tHeader,
                    data,
                    filename: '爬虫配置导出表',
                })
            })
        },
        formatJson(filterVal) {
            return this.list.map(v =>
                filterVal.map(j => {
                    if (j === 'state') {
                        const stateObj = stateOption.find(obj => obj.type === v[j])
                        return stateObj ? stateObj.name : null
                    } else if (j === 'time') {
                        const timeObj = timeOptions.find(obj => obj.src == v[j])
                        return timeObj ? timeObj.dst : null
                    } else {
                        return v[j]
                    }
                })
            )
        },
    },
}
</script>

<style>
body .el-table th.gutter {
    display: table-cell !important;
}
</style>
