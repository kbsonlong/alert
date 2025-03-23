<template>
  <div class="analysis-container">
    <h2>智能分析</h2>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>告警趋势分析</span>
              <el-select v-model="timeRange" size="small">
                <el-option label="最近7天" value="7" />
                <el-option label="最近30天" value="30" />
                <el-option label="最近90天" value="90" />
              </el-select>
            </div>
          </template>
          <!-- 趋势图表 -->
          <div class="chart-container">
            <!-- 这里将使用ECharts等图表库展示数据 -->
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>告警类型分布</span>
            </div>
          </template>
          <!-- 饼图 -->
          <div class="chart-container">
            <!-- 这里将使用ECharts等图表库展示数据 -->
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>告警智能分析报告</span>
            </div>
          </template>
          <div class="analysis-report">
            <!-- 分析报告内容 -->
            <el-empty description="暂无分析数据" v-if="!hasAnalysisData" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const timeRange = ref('7')
const hasAnalysisData = ref(false)

// TODO: 实现数据获取和图表展示逻辑
</script>

<style scoped>
.analysis-container {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
}

.mt-20 {
  margin-top: 20px;
}

.analysis-report {
  min-height: 200px;
}
</style>