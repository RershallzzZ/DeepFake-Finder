<template>
    <div class="dashboard-editor-container">
        <panel-group />

        <el-row class="chart-container">
            <mix-chart />
        </el-row>

        <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
            <line-chart />
        </el-row>

        <el-row :gutter="32">
            <el-col :xs="24" :sm="24" :lg="8">
                <div class="chart-wrapper">
                    <pie-chart />
                </div>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
                <div class="chart-wrapper">
                    <bar-chart />
                </div>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
                <div class="chart-wrapper">
                    <raddar-chart />
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
import RaddarChart from './components/RaddarChart'
import PieChart from './components/PieChart'
import BarChart from './components/BarChart'
import MixChart from './components/MixChart'

export default {
    name: 'DashboardAdmin',
    components: {
        PanelGroup,
        LineChart,
        RaddarChart,
        PieChart,
        BarChart,
        MixChart
    },
    data() {
        return {}
    },

    methods: {},
}
</script>

<style lang="scss" scoped>
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
.chart-container{
  background:#fff;
  padding:16px 16px 0;
  margin-bottom:32px;
}
</style>
