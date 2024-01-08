<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
import resize from './mixins/resize'

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
            default: '500px',
        },
    },
    data() {
        return {
            chart: null,
        }
    },
    mounted() {
        this.initChart()
    },
    beforeDestroy() {
        if (!this.chart) {
            return
        }
        this.chart.dispose()
        this.chart = null
    },
    methods: {
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
            const xData = (function() {
                const data = []
                for (let i = 15; i < 27; i++) {
                    data.push('2020-05-'+i )
                }
                return data
            })()
            this.chart.setOption({
                title: {
                    text: '每日监控趋势',
                    x: 'center',
                    textStyle: {
                        fontSize: '22',
                    },
                },
                tooltip: {
                    trigger: 'axis',
                },
                grid: {
                    left: 20,
                    right: 20,
                    bottom: 60,
                    top: 80,
                    containLabel: true,
                },
                legend: {
                    x:'center',
                    top:'10%',
                    data: ['换脸视频数量', '作者数量', '检测视频数量'],
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        axisLabel: {
                            interval: 0,
                        },
                        data: xData,
                    },
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            interval: 0,
                        },
                        name: '数量/个',
                        nameTextStyle: {
                            fontSize: 15,
                        },
                        nameGap: 23,
                    },
                ],
                dataZoom: [
                    {
                        show: true,
                        height: 30,
                        xAxisIndex: [0],
                        bottom: 20,
                        handleIcon:
                            'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
                        handleSize: '110%',
                    },
                    {
                        type: 'inside',
                        show: true,
                        height: 15,
                        start: 1,
                        end: 35,
                    },
                ],
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
                series: [
                    {
                        name: '换脸视频数量',
                        type: 'bar',
                        tiled: 'total',
                        barMaxWidth: 35,
                        barGap: '10%',
                        itemStyle: {
                            normal: {
                                // color: 'rgba(255,144,128,1)',
                                label: {
                                    show: true,
                                    textStyle: {
                                        // color: '#fff',
                                    },
                                    position: 'insideTop',
                                    formatter(p) {
                                        return p.value > 0 ? p.value : ''
                                    },
                                },
                            },
                        },
                        data: [47, 19, 25, 26, 17, 14, 15, 32, 52, 33, 24, 40],
                    },

                    {
                        name: '作者数量',
                        type: 'bar',
                        tiled: 'total',
                        barMaxWidth: 35,
                        itemStyle: {
                            normal: {
                                // color: 'rgba(0,191,183,1)',
                                barBorderRadius: 0,
                                label: {
                                    show: true,
                                    position: 'top',
                                    formatter(p) {
                                        return p.value > 0 ? p.value : ''
                                    },
                                },
                            },
                        },
                        data: [12, 17, 5, 12, 8, 8, 7, 13, 10, 9, 3, 10],
                    },
                    {
                        name: '检测视频数量',
                        type: 'line',
                        stack: 'total',
                        symbolSize: 10,
                        symbol: 'circle',
                        itemStyle: {
                            normal: {
                                // color: 'rgba(252,230,48,1)',
                                barBorderRadius: 0,
                                label: {
                                    show: true,
                                    position: 'top',
                                    formatter(p) {
                                        return p.value > 0 ? p.value : ''
                                    },
                                },
                            },
                        },
                        data: [56, 46, 40, 30, 51, 40, 30, 37, 75, 45, 54, 60],
                    },
                ],
            })
        },
    },
}
</script>
