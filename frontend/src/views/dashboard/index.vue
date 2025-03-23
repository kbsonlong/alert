<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="overview-card">
          <template #header>
            <div class="card-header">
              <span>告警概览</span>
            </div>
          </template>
          <div class="overview-content">
            <div class="overview-item">
              <div class="item-label">今日告警</div>
              <div class="item-value">{{ stats.today }}</div>
            </div>
            <div class="overview-item">
              <div class="item-label">待处理</div>
              <div class="item-value warning">{{ stats.pending }}</div>
            </div>
            <div class="overview-item">
              <div class="item-label">已处理</div>
              <div class="item-value success">{{ stats.handled }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="severity-card">
          <template #header>
            <div class="card-header">
              <span>告警级别分布</span>
            </div>
          </template>
          <div ref="severityChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="source-card">
          <template #header>
            <div class="card-header">
              <span>告警来源分布</span>
            </div>
          </template>
          <div ref="sourceChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card class="trend-card">
          <template #header>
            <div class="card-header">
              <span>告警趋势</span>
              <el-radio-group v-model="trendTimeRange" size="small">
                <el-radio-button label="week">最近一周</el-radio-button>
                <el-radio-button label="month">最近一月</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="trendChart" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="latest-card">
          <template #header>
            <div class="card-header">
              <span>最新告警</span>
              <el-link type="primary" :underline="false" @click="viewMore">查看更多</el-link>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="alert in latestAlerts"
              :key="alert.id"
              :type="getSeverityType(alert.severity)"
              :timestamp="alert.created_at"
            >
              {{ alert.title }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const severityChart = ref()
const sourceChart = ref()
const trendChart = ref()
const trendTimeRange = ref('week')

const stats = reactive({
  today: 0,
  pending: 0,
  handled: 0
})

const latestAlerts = ref([])

const initCharts = () => {
  // 初始化告警级别分布图表
  const severityOption = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: '50%',
        data: [
          { value: 10, name: '紧急' },
          { value: 20, name: '重要' },
          { value: 30, name: '次要' },
          { value: 40, name: '提示' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  // 初始化告警来源分布图表
  const sourceOption = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: '50%',
        data: [
          { value: 25, name: '系统监控' },
          { value: 20, name: '应用监控' },
          { value: 15, name: '网络监控' },
          { value: 40, name: '其他' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  // 初始化告警趋势图表
  const trendOption = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['紧急', '重要', '次要', '提示']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '紧急',
        type: 'line',
        data: [10, 8, 12, 6, 9, 7, 11]
      },
      {
        name: '重要',
        type: 'line',
        data: [20, 18, 22, 16, 19, 17, 21]
      },
      {
        name: '次要',
        type: 'line',
        data: [30, 28, 32, 26, 29, 27, 31]
      },
      {
        name: '提示',
        type: 'line',
        data: [40, 38, 42, 36, 39, 37, 41]
      }
    ]
  }
  
  const severityChartInstance = echarts.init(severityChart.value)
  const sourceChartInstance = echarts.init(sourceChart.value)
  const trendChartInstance = echarts.init(trendChart.value)
  
  severityChartInstance.setOption(severityOption)
  sourceChartInstance.setOption(sourceOption)
  trendChartInstance.setOption(trendOption)
  
  window.addEventListener('resize', () => {
    severityChartInstance.resize()
    sourceChartInstance.resize()
    trendChartInstance.resize()
  })
}

const getSeverityType = (severity: string) => {
  const types = {
    urgent: 'danger',
    important: 'warning',
    minor: 'info',
    hint: 'success'
  }
  return types[severity] || 'info'
}

const viewMore = () => {
  router.push('/alerts')
}

const fetchDashboardData = async () => {
  try {
    // TODO: 实现仪表盘数据获取API调用
    // const response = await fetch('/api/v1/dashboard/stats')
    // const data = await response.json()
    // stats.today = data.today
    // stats.pending = data.pending
    // stats.handled = data.handled
    // latestAlerts.value = data.latest_alerts
    
    // 模拟数据
    stats.today = 58
    stats.pending = 15
    stats.handled = 43
    latestAlerts.value = [
      { id: 1, title: '服务器CPU使用率超过90%', severity: 'urgent', created_at: '2024-01-20 10:30:00' },
      { id: 2, title: '数据库连接数接近上限', severity: 'important', created_at: '2024-01-20 09:45:00' },
      { id: 3, title: '应用响应时间异常', severity: 'minor', created_at: '2024-01-20 09:15:00' },
      { id: 4, title: '磁盘使用空间超过80%', severity: 'hint', created_at: '2024-01-20 08:30:00' }
    ]
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

onMounted(() => {
  fetchDashboardData()
  initCharts()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.overview-content {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.overview-item {
  text-align: center;
}

.item-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.item-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.item-value.warning {
  color: #E6A23C;
}

.item-value.success {
  color: #67C23A;
}

.chart-container {
  height: 300px;
}
</style>