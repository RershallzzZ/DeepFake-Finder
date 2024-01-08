<template>
    <div class="dashboard-editor-container">
        <el-form ref="searchForm" :model="searchMap">
            <el-row class="filter">
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item label="请输入视频标题" prop="title" label-width="130px">
                        <el-input v-model="searchMap.title" placeholder="视频标题" style="width: 180px;"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item label="请输入作者" prop="promulgator" label-width="130px">
                        <el-input v-model="searchMap.promulgator" placeholder="作者名" style="width: 160px;"></el-input>
                    </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item prop="year" label="请选择视频年份" label-width="130px">
                        <el-date-picker
                            format="yyyy 年"
                            v-model="searchMap.year"
                            type="year"
                            style="width: 160px;"
                            placeholder="视频年份"
                            value-format="yyyy"
                        ></el-date-picker>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item prop="monitorDate" label="请选择监控日期" label-width="130px">
                        <el-date-picker
                            format="yyyy-MM-dd"
                            v-model="searchMap.monitorDate"
                            type="date"
                            style="width: 160px;"
                            placeholder="监控日期"
                            value-format="yyyy-MM-dd"
                        ></el-date-picker>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row class="filter" style="margin-bottom: 32px;">
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item label="请选择视频网站" prop="website" label-width="130px">
                        <el-select v-model="searchMap.website" multiple placeholder="视频网站名" style="width: 180px;">
                            <el-option
                                v-for="item in websiteOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item label="请选择时长" prop="duration" label-width="130px">
                        <el-select v-model="searchMap.duration" multiple placeholder="请选择时长" style="width: 150px;">
                            <el-option
                                v-for="item in durationOptions"
                                :key="item"
                                :label="item"
                                :value="item"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item prop="category" label="请选择视频类别" label-width="130px">
                        <el-select v-model="searchMap.category" multiple placeholder="视频类别" style="width: 160px;">
                            <el-option label="政治" value="政治"></el-option>
                            <el-option label="娱乐" value="娱乐"></el-option>
                            <el-option label="科技" value="科技"></el-option>
                            <el-option label="其他" value="其他"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="6">
                    <el-form-item label-width="40px">
                        <el-button icon="el-icon-search" type="primary" @click="analyse">统计</el-button>
                        <el-button type="primary" @click="$refs.searchForm.resetFields()" icon="el-icon-s-operation">
                            重置
                        </el-button>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
        <el-main v-loading="loading">
            <el-row :gutter="32">
                <el-col :xs="24" :sm="24" :lg="12">
                    <div class="chart-wrapper">
                        <Row1LineChart ref="row1_line_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="12">
                    <div class="chart-wrapper">
                        <Row1BarChart ref="row1_bar_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="32">
                <el-col :xs="24" :sm="24" :lg="8">
                    <div class="chart-wrapper">
                        <Row2PieChart ref="row2_pie_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="8">
                    <div class="chart-wrapper">
                        <Row2BarChart ref="row2_bar_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="8">
                    <div class="chart-wrapper">
                        <Row2RaddarChart ref="row2_raddar_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="32">
                <el-col :xs="24" :sm="24" :lg="12">
                    <el-tag>换脸视频标题词云</el-tag>
                    <div class="chart-wrapper" style="padding-bottom: 16px;">
                        <Row3WordCloud ref="row3_word_cloud" :searchMap="searchMap" />
                    </div>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="12">
                    <el-tag>换脸视频标题TOP10</el-tag>
                    <div class="chart-wrapper" style="padding-bottom: 16px;">
                        <Row3BarChart ref="row3_bar_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="32">
                <el-col :xs="24" :sm="24" :lg="12">
                    <el-tag>换脸视频作者词云</el-tag>
                    <div class="chart-wrapper" style="padding-bottom: 16px;">
                        <Row4WordCloud ref="row4_word_cloud" :searchMap="searchMap" />
                    </div>
                </el-col>
                <el-col :xs="24" :sm="24" :lg="12">
                    <el-tag>换脸视频作者TOP10</el-tag>
                    <div class="chart-wrapper" style="padding-bottom: 16px;">
                        <Row4BarChart ref="row4_bar_chart" :searchMap="searchMap" />
                    </div>
                </el-col>
            </el-row>
        </el-main>
    </div>
</template>

<script>
import axios from 'axios'
import Row1LineChart from './echarts/row1/LineChart'
import Row1BarChart from './echarts/row1/BarChart'
import Row2RaddarChart from './echarts/row2/RaddarChart'
import Row2PieChart from './echarts/row2/PieChart'
import Row2BarChart from './echarts/row2/BarChart'
import Row3WordCloud from './echarts/row3/WordCloud'
import Row3BarChart from './echarts/row3/BarChart'
import Row4WordCloud from './echarts/row4/WordCloud'
import Row4BarChart from './echarts/row4/BarChart'
import websitesApi from '@/api/deepfakedetect/resultanalysis/websites'
export default {
    name: 'ResultAnalysis',
    data() {
        return {
            test: '',
            loading: false,
            websiteOptions: [],
            searchMap: {
                title: '',
                promulgator: '',
                year: '',
                monitorDate: '',
                category: '',
                website: [],
                duration: [],
            },
            durationOptions: ['3分钟以下', '3-10分钟', '10-30分钟', '30-60分钟', '60分钟以上'],
        }
    },
    created() {
        this.fetchWebsites()
        //延时器
    },
    components: {
        Row1LineChart,
        Row1BarChart,
        Row2RaddarChart,
        Row2PieChart,
        Row2BarChart,
        Row3WordCloud,
        Row3BarChart,
        Row4WordCloud,
        Row4BarChart,
    },
    methods: {
        fetchWebsites() {
            this.loading = true
            websitesApi.getWebsite().then(response => {
                this.websiteOptions = response.data.websiteList
                setTimeout(() => {
                    this.loading = false
                }, 1000)
            })
        },

        analyse() {
            this.loading = true
            this.$refs.row1_line_chart.fetchData()
            this.$refs.row1_bar_chart.fetchData()
            this.$refs.row2_bar_chart.fetchData()
            this.$refs.row2_pie_chart.fetchData()
            this.$refs.row2_raddar_chart.fetchData()
            this.$refs.row3_bar_chart.fetchData()
            this.$refs.row3_word_cloud.fetchData()
            this.$refs.row4_word_cloud.fetchData()
            this.$refs.row4_bar_chart.fetchData()
            setTimeout(() => {
                this.loading = false
            }, 1000)
        },
    },
}
</script>

<style lang="scss" scoped>
.filter {
    background: #fff;
    padding: 16px 16px 0;
    // justify-content: space-between;
    // margin-bottom:32px;
}

.dashboard-editor-container {
    padding: 32px;
    background-color: rgb(240, 242, 245);
    position: relative;

    .chart-wrapper {
        background: #fff;
        padding: 16px 16px 0;
        margin-bottom: 32px;
    }
}

@media (max-width: 1024px) {
    .chart-wrapper {
        padding: 8px;
    }
}
</style>
