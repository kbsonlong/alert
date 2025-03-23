<template>
  <div class="notification-groups-container">
    <div class="header">
      <h2>通知组管理</h2>
      <el-button type="primary" @click="showCreateDialog">新建通知组</el-button>
    </div>

    <el-table :data="groups" border style="width: 100%">
      <el-table-column prop="name" label="组名称" />
      <el-table-column label="成员数量" width="120">
        <template #default="{ row }">
          {{ row.members?.members?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column label="通知渠道" width="200">
        <template #default="{ row }">
          <el-tag
            v-for="channelId in row.channels?.channels"
            :key="channelId"
            size="small"
            style="margin-right: 5px"
          >
            {{ getChannelName(channelId) }}
          </el-tag>
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
      <el-form :model="groupForm" label-width="100px">
        <el-form-item label="组名称" required>
          <el-input v-model="groupForm.name" />
        </el-form-item>
        <el-form-item label="组成员" required>
          <el-table :data="groupForm.members?.members || []" border style="width: 100%">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="phone" label="手机号" />
            <el-table-column label="操作" width="100">
              <template #default="{ $index }">
                <el-button
                  type="danger"
                  size="small"
                  @click="removeMember($index)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 10px">
            <el-button type="primary" @click="showMemberDialog">添加成员</el-button>
          </div>
        </el-form-item>
        <el-form-item label="通知渠道" required>
          <el-select
            v-model="groupForm.channels.channels"
            multiple
            style="width: 100%"
          >
            <el-option
              v-for="channel in channels"
              :key="channel.id"
              :label="channel.name"
              :value="channel.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加成员对话框 -->
    <el-dialog
      title="添加成员"
      v-model="memberDialogVisible"
      width="40%"
    >
      <el-form :model="memberForm" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="memberForm.name" />
        </el-form-item>
        <el-form-item label="邮箱" required>
          <el-input v-model="memberForm.email" type="email" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="memberForm.phone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="memberDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddMember">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { NotificationGroup, NotificationChannel } from '@/types/notification'

const groups = ref<NotificationGroup[]>([])
const channels = ref<NotificationChannel[]>([])
const dialogVisible = ref(false)
const memberDialogVisible = ref(false)
const dialogTitle = ref('')
const groupForm = ref<Partial<NotificationGroup>>({
  members: { members: [] },
  channels: { channels: [] }
})
const memberForm = ref({
  name: '',
  email: '',
  phone: ''
})

const fetchGroups = async () => {
  try {
    const response = await fetch('/api/notification-groups')
    const data = await response.json()
    groups.value = data
  } catch (error) {
    ElMessage.error('获取通知组列表失败')
  }
}

const fetchChannels = async () => {
  try {
    const response = await fetch('/api/notification-channels')
    const data = await response.json()
    channels.value = data
  } catch (error) {
    ElMessage.error('获取通知渠道列表失败')
  }
}

const showCreateDialog = () => {
  dialogTitle.value = '新建通知组'
  groupForm.value = {
    members: { members: [] },
    channels: { channels: [] }
  }
  dialogVisible.value = true
}

const showEditDialog = (group: NotificationGroup) => {
  dialogTitle.value = '编辑通知组'
  groupForm.value = { ...group }
  dialogVisible.value = true
}

const showMemberDialog = () => {
  memberForm.value = {
    name: '',
    email: '',
    phone: ''
  }
  memberDialogVisible.value = true
}

const handleAddMember = () => {
  if (!memberForm.value.name || !memberForm.value.email) {
    ElMessage.warning('请填写必填项')
    return
  }

  if (!groupForm.value.members) {
    groupForm.value.members = { members: [] }
  }

  groupForm.value.members.members.push({
    name: memberForm.value.name,
    email: memberForm.value.email,
    phone: memberForm.value.phone
  })

  memberDialogVisible.value = false
}

const removeMember = (index: number) => {
  if (groupForm.value.members?.members) {
    groupForm.value.members.members.splice(index, 1)
  }
}

const handleSubmit = async () => {
  try {
    const url = groupForm.value.id
      ? `/api/notification-groups/${groupForm.value.id}`
      : '/api/notification-groups'
    const method = groupForm.value.id ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(groupForm.value)
    })
    
    if (response.ok) {
      ElMessage.success('保存成功')
      dialogVisible.value = false
      fetchGroups()
    } else {
      throw new Error('保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleDelete = async (group: NotificationGroup) => {
  try {
    await ElMessageBox.confirm('确定要删除该通知组吗？')
    
    const response = await fetch(`/api/notification-groups/${group.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('删除成功')
      fetchGroups()
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const getChannelName = (channelId: number) => {
  const channel = channels.value.find(c => c.id === channelId)
  return channel?.name || '未知渠道'
}

onMounted(() => {
  fetchGroups()
  fetchChannels()
})
</script>

<style scoped>
.notification-groups-container {
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