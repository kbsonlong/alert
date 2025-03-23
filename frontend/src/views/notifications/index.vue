<template>
  <div class="notifications-container">
    <div class="header">
      <h2>通知渠道管理</h2>
      <el-button type="primary" @click="showCreateDialog">新建渠道</el-button>
    </div>

    <el-table :data="channels" border style="width: 100%">
      <el-table-column prop="name" label="渠道名称" />
      <el-table-column prop="type" label="渠道类型" />
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
      <el-form :model="channelForm" label-width="100px">
        <el-form-item label="渠道名称" required>
          <el-input v-model="channelForm.name" />
        </el-form-item>
        <el-form-item label="渠道类型" required>
          <el-select v-model="channelForm.type" style="width: 100%">
            <el-option label="邮件" value="email" />
            <el-option label="短信" value="sms" />
            <el-option label="WebHook" value="webhook" />
          </el-select>
        </el-form-item>
        <el-form-item label="配置信息" required>
          <el-input
            v-model="channelForm.config"
            type="textarea"
            :rows="4"
            placeholder="请输入JSON格式的配置信息"
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
import type { NotificationChannel } from '@/types/notification'

const channels = ref<NotificationChannel[]>([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const channelForm = ref<Partial<NotificationChannel>>({})

const fetchChannels = async () => {
  try {
    const response = await fetch('/api/notifications/channels')
    const data = await response.json()
    channels.value = data
  } catch (error) {
    ElMessage.error('获取通知渠道列表失败')
  }
}

const showCreateDialog = () => {
  dialogTitle.value = '新建渠道'
  channelForm.value = {
    enabled: true,
    config: '{}'
  }
  dialogVisible.value = true
}

const showEditDialog = (channel: NotificationChannel) => {
  dialogTitle.value = '编辑渠道'
  channelForm.value = {
    ...channel,
    config: typeof channel.config === 'string' ? channel.config : JSON.stringify(channel.config, null, 2)
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    // 验证配置信息是否为有效的JSON
    if (channelForm.value.config) {
      try {
        JSON.parse(channelForm.value.config as string)
      } catch (e) {
        ElMessage.error('配置信息必须是有效的JSON格式')
        return
      }
    }

    const url = channelForm.value.id
      ? `/api/notifications/channels/${channelForm.value.id}`
      : '/api/notifications/channels'
    const method = channelForm.value.id ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...channelForm.value,
        config: channelForm.value.config ? JSON.parse(channelForm.value.config as string) : {}
      })
    })
    
    if (response.ok) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      fetchChannels()
    } else {
      throw new Error('保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleStatusChange = async (channel: NotificationChannel) => {
  try {
    const response = await fetch(`/api/notifications/channels/${channel.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ enabled: channel.enabled })
    })
    
    if (!response.ok) {
      throw new Error('更新状态失败')
    }
  } catch (error) {
    channel.enabled = !channel.enabled
    ElMessage.error('更新状态失败')
  }
}

const handleDelete = async (channel: NotificationChannel) => {
  try {
    await ElMessageBox.confirm('确定要删除该通知渠道吗？')
    
    const response = await fetch(`/api/notifications/channels/${channel.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      fetchChannels()
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchChannels()
})
</script>

<style scoped>
.notifications-container {
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