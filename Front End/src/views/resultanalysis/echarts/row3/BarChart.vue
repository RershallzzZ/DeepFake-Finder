<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../mixins/resize'
import { getBarChartData } from '@/api/deepfakedetect/resultanalysis/row3'
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
            websites: [],
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
                this.chartData = response.data.data
                this.websites = response.data.websites
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
        },
        setOptions({ titleTop10, titleNum } = {}) {
            const websites = this.websites
            var series = []
            for (var i = 0; i < this.websites.length; i++) {
                series.push({
                    type: 'bar',
                    stack: 'danger',
                    animationDuration,
                    name: this.websites[i],
                    data: titleNum[i],
                })
            }
            this.chart.setOption(
                {
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
                            type: 'value',
                            axisTick: {
                                show: false,
                            },
                            name: '视频标题出现次数',
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
                            data: titleTop10,
                            axisTick: {
                                alignWithLabel: true,
                            },
                            boundaryGap: true,
                            name: '视频标题',
                            nameTextStyle: {
                                fontSize: 15,
                            },
                            nameGap: 15,
                        },
                    ],
                    legend: {
                        data: websites,
                    },
                    series: series,
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
                },
                true
            )
        },
    },
}
</script>
