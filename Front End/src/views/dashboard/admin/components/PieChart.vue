<template>
    <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import { getPieChartData } from '@/api/deepfakedetect'
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
                premium: null,
                high: null,
                medium: null,
                low: null,
                bad: null,
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
            getPieChartData().then(response => {
                this.chartData = response.data
            })
        },
        initChart() {
            this.chart = echarts.init(this.$el, 'macarons')
        },
        setOptions({ high, medium, low, none } = {}) {
            this.chart.setOption({
                title: {
                    text: '已检测视频疑似换脸程度分布',
                    textStyle: {
                        fontSize: 15,
                    },
                    bottom: '8%',
                    left: 'center',
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)',
                },
                legend: {
                    left: 'center',
                    bottom: '0',
                    data: ['高', '中', '低', '无'],
                },
                series: [
                    {
                        name: '视频疑似换脸程度',
                        type: 'pie',
                        roseType: 'radius',
                        radius: [15, '65%'],
                        center: ['50%', '38%'],
                        data: [
                            {
                                value: high,
                                name: '高',
                                itemStyle: {
                                    color: '#f4516c',
                                },
                            },
                            {
                                value: medium,
                                name: '中',
                                itemStyle: {
                                    color: '#fda500',
                                },
                            },
                            {
                                value: low,
                                name: '低',
                                itemStyle: {
                                    color: '#36a3f7',
                                },
                            },
                            {
                                value: none,
                                name: '无',
                                itemStyle: {
                                    color: '#34bfa3',
                                },
                            },
                        ],
                        animationEasing: 'cubicInOut',
                        animationDuration: 2600,
                    },
                ],
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
            })
        },
    },
}
</script>
<style scoped>
.test {
    color: rgb(82, 212, 30);
}
</style>
