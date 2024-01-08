<template>
    <div>
        <div :class="className" :style="{ height: height, width: width }" id="linechart" />
        <!-- <button @click="changeData">动态变化</button> -->
    </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import { getLineChartData } from '@/api/deepfakedetect'

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
            default: '350px',
        },
        autoResize: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            chart: null,
            chartData: {
                year: null,
                deepfakeVideo: null,
                downloadVideo: null,
            },
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
            getLineChartData().then(response => {
                this.chartData = response.data
            })
        },
        initChart() {
            this.chart = echarts.init(document.getElementById('linechart'), 'macarons')
        },
        setOptions({ year, deepfakeVideo, downloadVideo } = {}) {
            this.chart.setOption({
                xAxis: {
                    data: year,
                    boundaryGap: false,
                    axisTick: {
                        show: true,
                    },
                    
                    name: '视频年份',
                    nameLocation: 'center',
                    nameTextStyle: {
                        fontSize: 15,
                    },
                    nameGap: 23,
                },
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
                yAxis: {
                    axisTick: {
                        show: true,
                    },
                    splitLine: {
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
                        type: 'line',
                        data: deepfakeVideo,
                        animationDuration: 2800,
                        animationEasing: 'cubicInOut',
                    },
                    {
                        name: '爬取视频数量',
                        smooth: true,
                        type: 'line',
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
            })
        },
        changeData() {
            // this.chartData = {
            //   year: [2000, 2001, 2002,2003,2004,2005,2006],
            //   deepfakeVideo: [100, 120, 161, 134, 105, 160, 165],
            //   downloadVideo: [120, 82, 91, 154, 162, 140, 145]
            // };
            // this.chartData.year.push(2007);
            // this.chartData.deepfakeVideo.push(200);
            // this.chartData.downloadVideo.push(130);
            this.setOptions({
                year: [2000, 2001, 2002, 2003, 2004, 2005, 2006],
                deepfakeVideo: [100, 120, 161, 134, 105, 160, 165],
                downloadVideo: [120, 82, 91, 154, 162, 140, 145],
            })
        },
    },
}
</script>
