<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
import resize from '../mixins/resize'
require('echarts-wordcloud')
require('echarts/theme/macarons') // echarts theme
import { getWordCloudData } from '@/api/deepfakedetect/resultanalysis/row3'
import { debounce } from '@/utils'

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
            getWordCloudData(this.searchMap).then(response => {
                this.chartData = response.data
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
        },
        setOptions(chartData = {}) {
            
            this.chart.setOption(
                {
                    tooltip: {
                        show: true,
                    },
                    toolbox: {
                        right: '2%',
                        y: 'top',
                        padding: [0, 0, 0, 0],
                        feature: {
                            saveAsImage: {},
                        },
                    },
                    series: [
                        {
                            name: '标题分析', //数据提示窗标题
                            type: 'wordCloud',
                            gridSize: 1,
                            width: '100%',
                            height: '85%',
                            sizeRange: [15, 60], //画布范围，如果设置太大会出现少词（溢出屏幕）
                            rotationRange: [-45, 90], //数据翻转范围
                            shape: 'diamond',
                            textPadding: 0,
                            drawOutOfBound:false,
                            autoSize: {
                                enable: true,
                                minSize: 6,
                            },
                            textStyle: {
                                normal: {
                                    color: function() {
                                        return (
                                            'rgb(' +
                                            [
                                                Math.round(Math.random() * 160),
                                                Math.round(Math.random() * 160),
                                                Math.round(Math.random() * 160),
                                            ].join(',') +
                                            ')'
                                        )
                                    },
                                },
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowColor: '#333',
                                },
                            },
                            data: chartData,
                        },
                    ],
                },
                true
            )
        },
    },
}
</script>
