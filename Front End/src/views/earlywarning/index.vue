<template>
    <div class="app-container">
        <div>
            <el-row :gutter="20">
                <el-col :span="24" :xs="24">
                    <el-card>
                        <el-tabs v-model="activeTab">
                            <mix-chart />
                            <el-tab-pane label="系统预警消息" name="timeline">
                                <timeline />
                            </el-tab-pane>
                        </el-tabs>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
import Timeline from './components/Timeline'
import MixChart from './components/MixChart'

export default {
    name: 'EarlyWarningShow',
    components: { Timeline, MixChart },
    data() {
        return {
            activeTab: 'timeline',
        }
    },

    methods: {},
}
</script>
