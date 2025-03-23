<template>
  <div class="knowledge-query">
    <el-form :model="queryForm" label-width="100px">
      <el-form-item label="查询内容" required>
        <el-input
          v-model="queryForm.query"
          type="textarea"
          :rows="4"
          placeholder="请输入要查询的内容"
        />
      </el-form-item>
      <el-form-item label="匹配数量">
        <el-input-number
          v-model="queryForm.top_k"
          :min="1"
          :max="10"
          :step="1"
        />
      </el-form-item>
      <el-form-item label="相似度阈值">
        <el-slider
          v-model="queryForm.threshold"
          :min="0"
          :max="1"
          :step="0.1"
          :format-tooltip="(val) => (val * 100).toFixed(0) + '%'"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleQuery" :loading="loading">
          查询
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="queryResult" class="query-result">
      <el-card class="result-card">
        <template #header>
          <div class="card-header">
            <span>查询结果</span>
            <el-tag type="info" size="small">
              耗时: {{ queryResult.metadata?.total_duration?.toFixed(2) }}ms
            </el-tag>
          </div>
        </template>
        <div class="result-content">
          <pre>{{ queryResult.content }}</pre>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { KnowledgeQuery, KnowledgeSearchResult } from '@/types/knowledge'

const queryForm = ref<KnowledgeQuery>({
  query: '',
  top_k: 3,
  threshold: 0.7
})

const loading = ref(false)
const queryResult = ref<KnowledgeSearchResult | null>(null)

const handleQuery = async () => {
  if (!queryForm.value.query.trim()) {
    ElMessage.warning('请输入查询内容')
    return
  }

  loading.value = true
  try {
    const response = await fetch('/api/knowledge/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(queryForm.value)
    })

    if (!response.ok) {
      throw new Error('查询失败')
    }

    queryResult.value = await response.json()
  } catch (error) {
    ElMessage.error('查询失败：' + (error instanceof Error ? error.message : '未知错误'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.knowledge-query {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.query-result {
  margin-top: 20px;
}

.result-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-content {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>