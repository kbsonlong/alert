<template>
  <el-container class="app-wrapper">
    <el-aside width="200px" class="sidebar-container">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical"
        :router="true"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard">
          <el-icon><Monitor /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/alerts">
          <el-icon><Bell /></el-icon>
          <span>告警管理</span>
        </el-menu-item>
        <el-menu-item index="/rules">
          <el-icon><Setting /></el-icon>
          <span>规则管理</span>
        </el-menu-item>
        <el-menu-item index="/notifications">
          <el-icon><Message /></el-icon>
          <span>通知管理</span>
        </el-menu-item>
        <el-menu-item index="/templates">
          <el-icon><Document /></el-icon>
          <span>模板管理</span>
        </el-menu-item>
        <el-menu-item index="/analysis">
          <el-icon><DataAnalysis /></el-icon>
          <span>智能分析</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header height="50px" class="app-header">
        <div class="header-left">
          <h2>运维告警管理系统</h2>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-dropdown">
              <el-avatar size="small" />
              <span class="username">管理员</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { Monitor, Bell, Setting, Message, Document, DataAnalysis } from '@element-plus/icons-vue'
</script>

<style scoped>
.app-wrapper {
  height: 100vh;
}

.sidebar-container {
  background-color: #304156;
  height: 100%;
}

.el-menu-vertical {
  border-right: none;
}

.app-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  font-size: 14px;
}
</style>