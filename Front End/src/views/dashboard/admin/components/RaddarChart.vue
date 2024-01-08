<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import { getRaddarChartData } from '@/api/deepfakedetect'
const animationDuration = 3000

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
            chartData: {},
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
            getRaddarChartData().then(response => {
                this.chartData = response.data.data
                this.websites = response.data.websites
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
        },
        setOptions(chartData = {}) {
            var data = []
            for (var i = 0; i < this.websites.length; i++) {
                data.push({ value: chartData[i], name: this.websites[i] })
            }
            var maxSet = []
            for (let i = 0; i < 4; i++) {
                var temp = []
                for (let j = 0; j < this.websites.length; j++) {
                    temp.push(this.chartData[j][i])
                }
                maxSet.push(Math.max(...temp))
            }
            this.chart.setOption({
                title: {
                    text: '各网站已检测视频疑似程度分布',
                    textStyle: {
                        fontSize: 15,
                    },
                    bottom: '8%',
                    left: 'center',
                },
                toolbox: {
                    right: '5%',
                    show: true,
                    showTilte: true,
                    feature: {
                        saveAsImage: {
                            show: true,
                        },
                    },
                },
                tooltip: {},
                radar: {
                    radius: '66%',
                    center: ['50%', '42%'],
                    splitNumber: 8,
                    splitArea: {
                        areaStyle: {
                            color: 'rgba(127,95,132,.3)',
                            opacity: 1,
                            shadowBlur: 45,
                            shadowColor: 'rgba(0,0,0,.5)',
                            shadowOffsetX: 0,
                            shadowOffsetY: 15,
                        },
                    },
                    indicator: [
                        { name: '高疑似', color: '#f4516c', max: maxSet[0] * 1.2 },
                        { name: '中疑似', color: '#fda500', max: maxSet[1] * 1.2 },
                        { name: '低疑似', color: '#36a3f7', max: maxSet[2] * 1.2 },
                        { name: '无疑似', color: '#34bfa3', max: maxSet[3] * 1.2 },
                    ],
                },
                legend: {
                    left: 'center',
                    bottom: '0',
                    data: this.websites,
                },
                series: [
                    {
                        type: 'radar',
                        symbolSize: 0,
                        areaStyle: {
                            normal: {
                                shadowBlur: 13,
                                shadowColor: 'rgba(0,0,0,.2)',
                                shadowOffsetX: 0,
                                shadowOffsetY: 10,
                                opacity: 1,
                            },
                        },
                        data: data,
                        animationDuration,
                    },
                ],
            })
        },
    },
}
</script>
