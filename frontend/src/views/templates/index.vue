<template>
  <div class="templates-container">
    <div class="header">
      <h2>通知模板管理</h2>
      <el-button type="primary" @click="showCreateDialog">新建模板</el-button>
    </div>

    <el-table :data="templates" border style="width: 100%">
      <el-table-column prop="name" label="模板名称" />
      <el-table-column prop="type" label="模板类型" />
      <el-table-column prop="language" label="语言" width="100" />
      <el-table-column label="操作" width="250">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button size="small" type="success" @click="showTestDialog(row)">测试</el-button>
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
      <el-form :model="templateForm" label-width="100px">
        <el-form-item label="模板名称" required>
          <el-input v-model="templateForm.name" />
        </el-form-item>
        <el-form-item label="模板类型" required>
          <el-select v-model="templateForm.type" style="width: 100%">
            <el-option label="邮件" value="email" />
            <el-option label="短信" value="sms" />
            <el-option label="WebHook" value="webhook" />
          </el-select>
        </el-form-item>
        <el-form-item label="语言">
          <el-select v-model="templateForm.language" style="width: 100%">
            <el-option label="中文" value="zh-CN" />
            <el-option label="英文" value="en-US" />
          </el-select>
        </el-form-item>
        <el-form-item label="模板内容" required>
          <el-input
            v-model="templateForm.content"
            type="textarea"
            :rows="6"
            placeholder="支持使用 {{变量名}} 作为占位符"
          />
        </el-form-item>
        <el-form-item label="变量列表">
          <el-tag
            v-for="variable in templateForm.variables?.variables || []"
            :key="variable"
            closable
            @close="removeVariable(variable)"
            style="margin-right: 10px; margin-bottom: 10px"
          >
            {{ variable }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="inputRef"
            v-model="inputValue"
            class="input-new-tag"
            size="small"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button v-else class="button-new-tag" size="small" @click="showInput">
            + 添加变量
          </el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 模板测试对话框 -->
    <el-dialog
      title="模板测试"
      v-model="testDialogVisible"
      width="50%"
    >
      <el-form :model="testForm" label-width="100px">
        <el-form-item
          v-for="variable in currentTemplate?.variables?.variables || []"
          :key="variable"
          :label="variable"
        >
          <el-input v-model="testForm[variable]" />
        </el-form-item>
      </el-form>
      <div v-if="testResult" class="test-result">
        <el-alert
          title="渲染结果"
          type="info"
          :closable="false"
        >
          <div style="white-space: pre-wrap;">{{ testResult }}</div>
        </el-alert>
      </div>
      <template #footer>
        <el-button @click="testDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleTest">测试</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { NotificationTemplate } from '@/types/notification'

const templates = ref<NotificationTemplate[]>([])
const dialogVisible = ref(false)
const testDialogVisible = ref(false)
const dialogTitle = ref('')
const templateForm = ref<Partial<NotificationTemplate>>({})
const currentTemplate = ref<NotificationTemplate | null>(null)
const testForm = ref<Record<string, string>>({})
const testResult = ref('')

// 变量输入相关
const inputVisible = ref(false)
const inputValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

const fetchTemplates = async () => {
  try {
    const response = await fetch('/api/notification-templates')
    const data = await response.json()
    templates.value = data
  } catch (error) {
    ElMessage.error('获取模板列表失败')
  }
}

const showCreateDialog = () => {
  dialogTitle.value = '新建模板'
  templateForm.value = {
    language: 'zh-CN',
    variables: { variables: [] }
  }
  dialogVisible.value = true
}

const showEditDialog = (template: NotificationTemplate) => {
  dialogTitle.value = '编辑模板'
  templateForm.value = { ...template }
  dialogVisible.value = true
}

const showTestDialog = (template: NotificationTemplate) => {
  currentTemplate.value = template
  testForm.value = {}
  testResult.value = ''
  testDialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    const url = templateForm.value.id
      ? `/api/notification-templates/${templateForm.value.id}`
      : '/api/notification-templates'
    const method = templateForm.value.id ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(templateForm.value)
    })
    
    if (response.ok) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      fetchTemplates()
    } else {
      throw new Error('保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleDelete = async (template: NotificationTemplate) => {
  try {
    await ElMessageBox.confirm('确定要删除该模板吗？')
    
    const response = await fetch(`/api/notification-templates/${template.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      fetchTemplates()
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleTest = async () => {
  if (!currentTemplate.value) return
  
  try {
    const response = await fetch(`/api/notification-templates/${currentTemplate.value.id}/test`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(testForm.value)
    })
    
    if (response.ok) {
      const data = await response.json()
      testResult.value = data.rendered_content
    } else {
      throw new Error('测试失败')
    }
  } catch (error) {
    ElMessage.error('测试失败')
  }
}

// 变量管理相关方法
const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    if (!templateForm.value.variables) {
      templateForm.value.variables = { variables: [] }
    }
    templateForm.value.variables.variables.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const removeVariable = (variable: string) => {
  if (templateForm.value.variables?.variables) {
    const index = templateForm.value.variables.variables.indexOf(variable)
    if (index !== -1) {
      templateForm.value.variables.variables.splice(index, 1)
    }
  }
}

onMounted(() => {
  fetchTemplates()
})
</script>

<style scoped>
.templates-container {
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

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.test-result {
  margin-top: 20px;
}
</style>