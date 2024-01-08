<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import { getBarChartData } from '@/api/deepfakedetect'
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
    },
    data() {
        return {
            chart: null,
            chartData: {
                politics: null,
                entertainment: null,
                tech: null,
                others: null,
            },
            websites: [],
        }
    },
    watch: {
        chartData: {
            deep: true,
            handler(newVal, oldVal) {
                this.$nextTick(() => {
                    console.log('watch', newVal, oldVal)
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
            getBarChartData().then(response => {
                this.chartData = response.data.data
                this.websites = response.data.websites
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
        },
        setOptions({ politics, entertainment, tech, others } = {}) {
            const websites = this.websites
            this.chart.setOption({
                title: {
                    text: '各网站换脸视频类别分布',
                    textStyle: {
                        fontSize: 15,
                    },
                    y: 'bottom',
                    left: 'center',
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                    },
                },
                grid: {
                    top: 10,
                    left: '2%',
                    right: '2%',
                    bottom: '3%',
                    containLabel: true,
                },
                xAxis: [
                    {
                        type: 'category',
                        data: websites,
                        axisTick: {
                            alignWithLabel: true,
                        },
                        boundaryGap: true,
                    },
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisTick: {
                            show: false,
                        },
                    },
                ],
                legend: {
                    data: ['政治', '娱乐', '科技', '其他'],
                    x: 'left', //可设定图例在左、右、居中
                    y: 'top', //可设定图例在上、下、居中
                    padding: [0, 0, 0, 0],
                    // orient: 'vertical',
                },
                series: [
                    {
                        name: '政治',
                        type: 'bar',
                        tiled: 'danger',
                        data: politics,
                        animationDuration,
                    },
                    {
                        name: '娱乐',
                        type: 'bar',
                        tiled: 'danger',
                        data: entertainment,
                        animationDuration,
                    },
                    {
                        name: '科技',
                        type: 'bar',
                        tiled: 'danger',
                        data: tech,
                        animationDuration,
                    },
                    {
                        name: '其他',
                        type: 'bar',
                        tiled: 'danger',
                        data: others,
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
                    top: '4%',
                    right: '3%',
                    show: true,
                    showTilte: true,
                    itemSize: 12,
                    feature: {
                        magicType: {
                            type: ['line', 'bar', 'stack', 'tiled'],
                        },
                        restore: {
                            show: true,
                        },
                        saveAsImage: {
                            show: true,
                        },
                    },
                },
            })
        },
    },
}
</script>
