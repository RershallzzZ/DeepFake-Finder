<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../mixins/resize'
import { getBarChartData } from '@/api/deepfakedetect/resultanalysis/row4'
const animationDuration = 6000

export default {
    mixins: [resize],
    props: {
        className: {
            type: String,
            default: 'chart',
        },
        width: {
            type: String,
            default: '100%',
        },
        height: {
            type: String,
            default: '320px',
        },
        searchMap: Object,
    },
    data() {
        return {
            chart: null,
            chartData: null,
        }
    },
    watch: {
        chartData: {
            deep: true,
            handler(newVal, oldVal) {
                this.$nextTick(() => {
                    this.chart.clear()
                    this.setOptions(newVal)
                })
            },
        },
    },
    created() {
        this.fetchData()
    },
    mounted() {
        this.$nextTick(() => {
            this.initChart()
        })
    },
    beforeDestroy() {
        if (!this.chart) {
            return
        }
        this.chart.dispose()
        this.chart = null
    },
    methods: {
        fetchData() {
            getBarChartData(this.searchMap).then(response => {
                this.chartData = response.data
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
            
        },
        setOptions({ author, count, website } = {}) {
            this.chart.setOption({
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                    },
                    formatter(params, ticket, callback) {
                        // console.log(params)
                        var res =
                            params[0].marker +
                            '视频作者<br/>' +
                            website[params[0].dataIndex] +
                            ': ' +
                            params[0].name +
                            '(' +
                            params[0].value +
                            ')'
                        return res
                    },
                },
                xAxis: [
                    {
                        type: 'value',
                        axisTick: {
                            show: false,
                        },
                        name: '视频作者出现次数',
                        nameLocation: 'center',
                        nameTextStyle: {
                            fontSize: 15,
                        },
                        nameGap: 35,
                    },
                ],
                yAxis: [
                    {
                        type: 'category',
                        data: author,
                        axisTick: {
                            alignWithLabel: true,
                        },
                        boundaryGap: true,
                        name: '视频作者',
                        nameTextStyle: {
                            fontSize: 15,
                        },
                        nameGap: 15,
                    },
                ],
                legend: {
                    data: ['出现次数'],
                },
                series: [
                    {
                        name: '出现次数',
                        type: 'bar',
                        stack: 'danger',
                        data: count,
                        animationDuration,
                    },
                ],
                grid: {
                    left: 20,
                    right: 20,
                    bottom: 30,
                    top: 40,
                    containLabel: true,
                },
                toolbox: {
                    right: '2%',
                    show: true,
                    showTilte: true,
                    feature: {
                        magicType: {
                            type: ['stack', 'tiled'],
                            show: true,
                        },
                        restore: {
                            show: true,
                        },
                        saveAsImage: {
                            show: true,
                        },
                    },
                },
            },true)
        },
    },
}
</script>
