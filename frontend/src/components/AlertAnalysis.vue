<template>
  <div>
    <el-button
      type="primary"
      size="small"
      :loading="loading"
      @click="handleAnalyze"
    >
      智能分析
    </el-button>

    <el-dialog
      title="告警分析结果"
      v-model="dialogVisible"
      width="50%"
    >
      <div v-if="analysisRecord">
        <div v-if="analysisRecord.status === 'completed'">
          <div v-if="analysisRecord.error_message" class="error-message">
            分析失败: {{ analysisRecord.error_message }}
          </div>
          <div v-else class="analysis-result">
            {{ analysisRecord.analysis_result }}
          </div>
        </div>
        <div v-else class="processing">
          <el-icon class="is-loading"><Loading /></el-icon>
          正在分析中...
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps<{
  alertId: number
}>()

const loading = ref(false)
const dialogVisible = ref(false)
const analysisRecord = ref(null)
let pollingTimer: number | null = null

const handleAnalyze = async () => {
  try {
    loading.value = true
    // 创建分析记录
    const response = await axios.post(`/api/analysis-records/analyze/${props.alertId}`)
    analysisRecord.value = response.data
    dialogVisible.value = true

    // 如果状态是processing，开始轮询
    if (response.data.status === 'processing') {
      startPolling()
    }
  } catch (error) {
    ElMessage.error('启动分析失败')
  } finally {
    loading.value = false
  }
}

const startPolling = () => {
  pollingTimer = window.setInterval(async () => {
    try {
      const response = await axios.get(`/api/analysis-records/${props.alertId}`)
      analysisRecord.value = response.data
      
      // 如果分析完成，停止轮询
      if (response.data.status === 'completed') {
        stopPolling()
      }
    } catch (error) {
      console.error('轮询分析状态失败:', error)
      stopPolling()
    }
  }, 3000) // 每3秒轮询一次
}

const stopPolling = () => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
    pollingTimer = null
  }
}

// 组件卸载时清理轮询定时器
onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.error-message {
  color: #f56c6c;
  margin: 10px 0;
}

.analysis-result {
  white-space: pre-wrap;
  line-height: 1.5;
  margin: 10px 0;
}

.processing {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
}
</style>