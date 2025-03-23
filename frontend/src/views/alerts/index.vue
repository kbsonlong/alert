<template>
  <div class="alerts-container">
    <div class="header">
      <h2>告警记录管理</h2>
      <el-button-group>
        <el-button type="primary" @click="handleRefresh">刷新</el-button>
        <el-button type="success" @click="handleBatchAnalyze" :disabled="!selectedAlerts.length">批量分析</el-button>
      </el-button-group>
    </div>

    <el-table :data="alerts" border style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column prop="description" label="告警标题" show-overflow-tooltip />
      <el-table-column prop="severity" label="级别" width="100">
        <template #default="{ row }">
          <el-tag :type="getSeverityType(row.severity)">{{ row.severity }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="source" label="来源" width="120" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="showDetailDialog(row)">详情</el-button>
            <el-button size="small" type="primary" @click="showAnalysisDialog(row)">分析</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 告警详情对话框 -->
    <el-dialog
      title="告警详情"
      v-model="detailDialogVisible"
      width="60%"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="标题">{{ currentAlert.description }}</el-descriptions-item>
        <el-descriptions-item label="级别">{{ currentAlert.severity }}</el-descriptions-item>
        <el-descriptions-item label="来源">{{ currentAlert.source }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-select v-model="currentAlert.status" style="width: 100%">
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已处理" value="resolved" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-descriptions-item>
        <el-descriptions-item label="内容" :span="2">
          <div style="white-space: pre-wrap;">{{ currentAlert.content }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="处理记录" :span="2">
          <el-input
            v-model="currentAlert.handling_notes"
            type="textarea"
            :rows="4"
            placeholder="请输入处理记录"
          />
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateAlert">保存</el-button>
      </template>
    </el-dialog>

    <!-- AI分析结果对话框 -->
    <el-dialog
      title="AI分析结果"
      v-model="analysisDialogVisible"
      width="60%"
    >
      <div v-if="currentAnalysis">
        <el-alert
          title="分析结果"
          type="info"
          :closable="false"
          style="margin-bottom: 20px;"
        >
          <div style="white-space: pre-wrap;">{{ currentAnalysis.analysis_result }}</div>
        </el-alert>

        <el-alert
          title="处理建议"
          type="success"
          :closable="false"
          style="margin-bottom: 20px;"
        >
          <ul>
            <li v-for="(suggestion, index) in currentAnalysis.suggestions.suggestions" :key="index">
              {{ suggestion }}
            </li>
          </ul>
        </el-alert>

        <el-alert
          v-if="currentAnalysis.similar_alerts.similar.length"
          title="相似告警"
          type="warning"
          :closable="false"
        >
          <ul>
            <li v-for="(alert, index) in currentAnalysis.similar_alerts.similar" :key="index">
              {{ alert }}
            </li>
          </ul>
        </el-alert>
      </div>
      <div v-else class="analysis-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在分析中，请稍候...</span>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import type { AlertRecord, AnalysisRecord } from '@/types/alert'

const alerts = ref<AlertRecord[]>([])
const selectedAlerts = ref<AlertRecord[]>([])
const detailDialogVisible = ref(false)
const analysisDialogVisible = ref(false)
const currentAlert = ref<Partial<AlertRecord>>({})
const currentAnalysis = ref<AnalysisRecord | null>(null)

const fetchAlerts = async () => {
  try {
    const response = await fetch('/api/alert-records')
    const data = await response.json()
    alerts.value = data
  } catch (error) {
    ElMessage.error('获取告警列表失败')
  }
}

const handleRefresh = () => {
  fetchAlerts()
}

const handleSelectionChange = (selection: AlertRecord[]) => {
  selectedAlerts.value = selection
}

const showDetailDialog = (alert: AlertRecord) => {
  currentAlert.value = { ...alert }
  detailDialogVisible.value = true
}

const handleUpdateAlert = async () => {
  try {
    const response = await fetch(`/api/alert-records/${currentAlert.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        status: currentAlert.value.status,
        handling_notes: currentAlert.value.handling_notes
      })
    })
    
    if (response.ok) {
      ElMessage.success('更新成功')
      detailDialogVisible.value = false
      fetchAlerts()
    } else {
      throw new Error('更新失败')
    }
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const showAnalysisDialog = async (alert: AlertRecord) => {
  currentAnalysis.value = null
  analysisDialogVisible.value = true
  
  try {
    const response = await fetch(`/api/analysis-records/analyze/${alert.id}`, {
      method: 'POST'
    })
    
    if (response.ok) {
      const data = await response.json()
      currentAnalysis.value = data.analysis
    } else {
      throw new Error('分析失败')
    }
  } catch (error) {
    ElMessage.error('分析失败')
    analysisDialogVisible.value = false
  }
}

const handleBatchAnalyze = async () => {
  ElMessage.info('批量分析功能开发中')
}

const getSeverityType = (severity: string) => {
  const types = {
    critical: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return types[severity as keyof typeof types] || 'info'
}

const getStatusType = (status: string) => {
  const types = {
    pending: 'warning',
    processing: 'info',
    resolved: 'success',
    closed: ''
  }
  return types[status as keyof typeof types] || ''
}

onMounted(() => {
  fetchAlerts()
})
</script>

<style scoped>
.alerts-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.analysis-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.analysis-loading .el-icon {
  margin-right: 10px;
  font-size: 20px;
}
</style>