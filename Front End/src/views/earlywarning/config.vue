<template>
    <div class="app-container">
        <el-form :inline="true" ref="searchForm" :model="searchMap" class="demo-form-inline" style="margin-top:1%; ">
            <el-form-item>
                <el-button type="primary" icon="el-icon-circle-plus" @click="handleAdd">新增监控用户</el-button>
            </el-form-item>
            <el-form-item prop="keyword">
                <el-input
                    v-model="searchMap.keyword"
                    @keyup.enter.native="fetchData"
                    placeholder="输入用户名"
                ></el-input>
            </el-form-item>
            <el-form-item prop="analyzed">
                <el-select v-model="searchMap.analyzed" placeholder="请选择预警阈值" style="width: 180px">
                    <el-option
                        v-for="item in analyzedOption"
                        :key="item.type"
                        :label="item.name"
                        :value="item.type"
                    ></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" icon="el-icon-search" @click="fetchData">搜索</el-button>
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
            border
            height="300"
            style="width: 100%;margin-bottom:1%"
            :default-sort="{ prop: 'analyzed', order: 'descending' }"
            v-loading="listLoading"
        >
            <el-table-column type="index" label="序号" align="center" width="50px"></el-table-column>

            <el-table-column prop="analyzed" label="预警阈值" sortable width="120" align="center">
                <template slot-scope="scope">
                    <el-tooltip effect="dark" :content="tooltipContent(scope.row.analyzed)" placement="top-start">
                        <el-tag :type="scope.row.analyzed | analyzedTagFilter">
                            {{ scope.row.analyzed | analyzedFilter }}
                        </el-tag>
                    </el-tooltip>
                </template>
            </el-table-column>

            <el-table-column prop="username" label="用户名" width="150" align="center"></el-table-column>
            <el-table-column prop="email" label="邮箱地址" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="'mailto:' + row.email" target="_blank">{{ row.email }}</el-link>
                </template>
            </el-table-column>
            <el-table-column prop="url" label="监控网站" align="center">
                <template slot-scope="{ row }">
                    <el-link type="primary" :href="row.url" target="_blank">{{ row.url }}</el-link>
                </template>
            </el-table-column>
            <el-table-column prop="create_time" label="创建日期" width="200" align="center"></el-table-column>

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
        <el-dialog title="编辑" :visible.sync="dialogFormVisible" width="500px">
            <el-form
                :model="pojo"
                ref="pojoForm"
                :rules="rules"
                label-position="right"
                label-width="120px"
                style="width: 400px"
            >
                <el-form-item label="用户邮箱" prop="email">
                    <el-input v-model="pojo.email"></el-input>
                </el-form-item>
                <el-form-item label="监控网站地址" prop="url">
                    <el-select v-model="pojo.url" placeholder="请选择监控网站地址" style="width: 250px;">
                        <el-option
                            v-for="item in websiteOptions"
                            :key="item.url"
                            :label="item.url"
                            :value="item.name"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="pojo.username"></el-input>
                </el-form-item>
                <el-form-item label="创建日期" prop="create_time">
                    <el-date-picker
                        format="yyyy 年 MM 月 dd 日"
                        v-model="pojo.create_time"
                        type="date"
                        placeholder="创建日期"
                        value-format="yyyy-MM-dd"
                    ></el-date-picker>
                </el-form-item>
                <el-form-item label="预警阈值" prop="analyzed">
                    <el-radio-group v-model="pojo.analyzed" size="medium">
                        <el-radio-button :label="4">高疑似</el-radio-button>
                        <el-radio-button :label="3">中疑似</el-radio-button>
                        <el-radio-button :label="2">低疑似</el-radio-button>
                    </el-radio-group>
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
import configApi from '@/api/deepfakedetect/earlywarning/config'
const analyzedOption = [{ type: 2, name: '低疑似' }, { type: 3, name: '中疑似' }, { type: 4, name: '高疑似' }]
const initPojo = {
    id: null,
    url: '',
    username: '',
    email: '',
    analyzed: '',
    create_time: '',
}
export default {
    name: 'EarlyWarningConfig',
    data() {
        return {
            list: [],
            total: 0,
            currentPage: 1,
            listLoading: false,
            pageSize: 10,
            searchMap: {
                keyword: '',
                analyzed: null,
            },
            analyzedOption,
            websiteOptions: [],
            dialogFormVisible: false,
            pojo: initPojo,
            rules: {
                //校验规则
                url: [
                    {
                        required: true,
                        message: '监控网站地址不能为空',
                        trigger: 'blur',
                    },
                ],
                email: [{ required: true, message: '邮箱地址不能为空', trigger: 'blur' }],
                analyzed: [
                    {
                        required: true,
                        message: '预警阈值不能为空',
                        trigger: 'change',
                    },
                ],
            },
        }
    },
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

    components: {},

    methods: {
        fetchData() {
            this.listLoading = true
            configApi.search(this.currentPage, this.pageSize, this.searchMap).then(response => {
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
        handleAdd() {
            configApi.getWebsiteOption().then(response => {
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
        addData(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    //提交表单

                    configApi.add(this.pojo).then(response => {
                        this.$message({
                            type: 'success',
                            message: '新增记录成功!',
                        })
                        this.fetchData()
                        this.dialogFormVisible = false
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '新增记录失败!',
                    })
                    return false
                }
            })
        },
        handleEdit(id) {
            this.handleAdd()
            configApi.getById(id).then(response => {
                console.log('handle edit', response)
                this.pojo = response.data
            })
        },

        //提交修改数据
        updateData(formName) {
            this.$refs[formName].validate(valid => {
                if (valid) {
                    configApi.update(this.pojo).then(response => {
                        this.$message({
                            type: 'success',
                            message: '更新记录成功!',
                        })
                        this.fetchData()
                        this.dialogFormVisible = false
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: '更新记录失败!',
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
                    configApi.deleteById(id).then(response => {
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
        handleDownload() {
            import('@/vendor/Export2Excel').then(excel => {
                const tHeader = ['预警阈值', '用户名', '邮箱地址', '监控网站', '创建日期']
                const filterVal = ['analyzed', 'username', 'email', 'url', 'create_time']
                const data = this.formatJson(filterVal)
                excel.export_json_to_excel({
                    header: tHeader,
                    data,
                    filename: '预警配置导出表',
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
        tooltipContent(type) {
            const analyzedObj = analyzedOption.find(obj => obj.type === type)
            return analyzedObj ? '当出现' + analyzedObj.name + '等级以上的视频时，给用户发送预警邮件' : null
        },
    },
}
</script>

<style>
body .el-table th.gutter {
    display: table-cell !important;
}
</style>
