<template>
  <div class="knowledge-container">
    <div class="header">
      <h2>知识库管理</h2>
      <el-button type="primary" @click="showCreateDialog">新建知识库</el-button>
    </div>

    <el-table :data="knowledgeBases" border style="width: 100%">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip />
      <el-table-column prop="source_type" label="来源类型" width="120" />
      <el-table-column prop="tags" label="标签">
        <template #default="{ row }">
          <el-tag
            v-for="tag in row.tags"
            :key="tag"
            style="margin-right: 5px"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180" />
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
      <el-form :model="knowledgeForm" label-width="100px">
        <el-form-item label="名称" required>
          <el-input v-model="knowledgeForm.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="knowledgeForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="来源类型" required>
          <el-select v-model="knowledgeForm.source_type">
            <el-option label="文档" value="document" />
            <el-option label="API" value="api" />
            <el-option label="数据库" value="database" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input
            v-model="knowledgeForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入知识库内容"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-tag
            v-for="tag in knowledgeForm.tags"
            :key="tag"
            closable
            @close="handleRemoveTag(tag)"
            style="margin-right: 5px"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputTagVisible"
            ref="tagInputRef"
            v-model="inputTagValue"
            class="input-new-tag"
            size="small"
            @keyup.enter="handleAddTag"
            @blur="handleAddTag"
          />
          <el-button v-else size="small" @click="showTagInput">
            + 新标签
          </el-button>
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
import type { KnowledgeBase } from '@/types/knowledge'

const knowledgeBases = ref<KnowledgeBase[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const knowledgeForm = ref<Partial<KnowledgeBase>>({})
const inputTagVisible = ref(false)
const inputTagValue = ref('')
const tagInputRef = ref<HTMLInputElement>()

const fetchKnowledgeBases = async () => {
  try {
    const response = await fetch('/api/knowledge')
    const data = await response.json()
    knowledgeBases.value = data
  } catch (error) {
    ElMessage.error('获取知识库列表失败')
  }
}

const showCreateDialog = () => {
  dialogTitle.value = '新建知识库'
  knowledgeForm.value = {
    tags: []
  }
  dialogVisible.value = true
}

const showEditDialog = (knowledge: KnowledgeBase) => {
  dialogTitle.value = '编辑知识库'
  knowledgeForm.value = { ...knowledge }
  dialogVisible.value = true
}

const handleDelete = async (knowledge: KnowledgeBase) => {
  try {
    await ElMessageBox.confirm('确认删除该知识库吗？', '提示', {
      type: 'warning'
    })
    await fetch(`/api/knowledge/${knowledge.id}`, {
      method: 'DELETE'
    })
    ElMessage.success('删除成功')
    await fetchKnowledgeBases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  try {
    const method = knowledgeForm.value.id ? 'PUT' : 'POST'
    const url = knowledgeForm.value.id
      ? `/api/knowledge/${knowledgeForm.value.id}`
      : '/api/knowledge'

    await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(knowledgeForm.value)
    })

    ElMessage.success(knowledgeForm.value.id ? '更新成功' : '创建成功')
    dialogVisible.value = false
    await fetchKnowledgeBases()
  } catch (error) {
    ElMessage.error(knowledgeForm.value.id ? '更新失败' : '创建失败')
  }
}

const handleRemoveTag = (tag: string) => {
  if (knowledgeForm.value.tags) {
    knowledgeForm.value.tags = knowledgeForm.value.tags.filter(t => t !== tag)
  }
}

const showTagInput = () => {
  inputTagVisible.value = true
  nextTick(() => {
    tagInputRef.value?.focus()
  })
}

const handleAddTag = () => {
  if (inputTagValue.value) {
    if (!knowledgeForm.value.tags) {
      knowledgeForm.value.tags = []
    }
    knowledgeForm.value.tags.push(inputTagValue.value)
  }
  inputTagVisible.value = false
  inputTagValue.value = ''
}

onMounted(() => {
  fetchKnowledgeBases()
})
</script>

<style scoped>
.knowledge-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>