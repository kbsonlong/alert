<template>
  <div class="rules-container">
    <div class="header">
      <h2>告警规则管理</h2>
      <el-button type="primary" @click="showCreateDialog">新建规则</el-button>
    </div>

    <el-table :data="rules" border style="width: 100%">
      <el-table-column prop="name" label="规则名称" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="severity" label="告警级别">
        <template #default="{ row }">
          <el-tag :type="getSeverityType(row.severity)">{{ row.severity }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="enabled" label="状态">
        <template #default="{ row }">
          <el-switch v-model="row.enabled" @change="handleStatusChange(row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="ruleForm" label-width="100px">
        <el-form-item label="规则名称" required>
          <el-input v-model="ruleForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="ruleForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="告警级别" required>
          <el-select v-model="ruleForm.severity">
            <el-option label="严重" value="critical" />
            <el-option label="警告" value="warning" />
            <el-option label="提示" value="info" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发条件" required>
          <el-input
            v-model="ruleForm.conditions"
            type="textarea"
            :rows="4"
            placeholder="请输入JSON格式的触发条件"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { AlertRule } from '@/types/alert'

const rules = ref<AlertRule[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const ruleForm = ref<Partial<AlertRule>>({})

const fetchRules = async () => {
  try {
    const response = await fetch('/api/alert-rules')
    const data = await response.json()
    rules.value = data
  } catch (error) {
    ElMessage.error('获取规则列表失败')
  }
}

const showCreateDialog = () => {
  dialogTitle.value = '新建规则'
  ruleForm.value = {
    enabled: true
  }
  dialogVisible.value = true
}

const showEditDialog = (rule: AlertRule) => {
  dialogTitle.value = '编辑规则'
  ruleForm.value = { ...rule }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    const url = ruleForm.value.id ? `/api/alert-rules/${ruleForm.value.id}` : '/api/alert-rules'
    const method = ruleForm.value.id ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(ruleForm.value)
    })
    
    if (response.ok) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      fetchRules()
    } else {
      throw new Error('保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleStatusChange = async (rule: AlertRule) => {
  try {
    const response = await fetch(`/api/alert-rules/${rule.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ enabled: rule.enabled })
    })
    
    if (!response.ok) {
      throw new Error('更新状态失败')
    }
  } catch (error) {
    rule.enabled = !rule.enabled
    ElMessage.error('更新状态失败')
  }
}

const handleDelete = async (rule: AlertRule) => {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？')
    
    const response = await fetch(`/api/alert-rules/${rule.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      fetchRules()
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getSeverityType = (severity: string) => {
  const types = {
    critical: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return types[severity as keyof typeof types] || 'info'
}

onMounted(() => {
  fetchRules()
})
</script>

<style scoped>
.rules-container {
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
</style>