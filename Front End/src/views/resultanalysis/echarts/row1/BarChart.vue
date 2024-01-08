<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../mixins/resize'
import { getBarChartData } from '@/api/deepfakedetect/resultanalysis/row1'


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
        autoResize: {
            type: Boolean,
            default: true,
        },
        searchMap: Object,
    },
    data() {
        return {
            chart: null,
            chartData: null
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
        setOptions({ duration, deepfakeVideo, downloadVideo } = {}) {
            
            this.chart.setOption({
                grid: {
                    left: 20,
                    right: 20,
                    bottom: 30,
                    top: 40,
                    containLabel: true,
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                    },
                    padding: [5, 10],
                },
                xAxis: {
                    data: duration,
                    boundaryGap: true,
                    axisTick: {
                        show: true,
                    },
                    name: '视频时长',
                    nameLocation: 'center',
                    nameTextStyle: {
                        fontSize: 15,
                    },
                    nameGap: 23,
                },
                yAxis: {
                    axisTick: {
                        show: true,
                    },
                    name: '视频数量/个',
                    nameTextStyle: {
                        fontSize: 15,
                    },
                    nameGap: 23,
                },
                legend: {
                    data: ['爬取视频数量', '换脸视频数量'],
                },
                series: [
                    {
                        name: '换脸视频数量',
                        itemStyle: {
                            normal: {
                                color: '#FF005A',
                                lineStyle: {
                                    color: '#FF005A',
                                    width: 2,
                                },
                            },
                        },
                        smooth: true,
                        type: 'bar',
                        data: deepfakeVideo,
                        animationDuration: 2800,
                        animationEasing: 'cubicInOut',
                    },
                    {
                        name: '爬取视频数量',
                        smooth: true,
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                color: '#3888fa',
                                lineStyle: {
                                    color: '#3888fa',
                                    width: 2,
                                },
                                areaStyle: {
                                    color: '#f3f8ff',
                                },
                            },
                        },
                        data: downloadVideo,
                        animationDuration: 2800,
                        animationEasing: 'quadraticOut',
                    },
                ],
                toolbox: {
                    right: '2%',
                    show: true,
                    showTilte: true,
                    feature: {
                        magicType: {
                            type: ['line', 'bar', 'stack', 'tiled'],
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
