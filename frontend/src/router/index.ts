import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/dashboard/index.vue'),
    meta: { title: '仪表盘', icon: 'Monitor' }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/alerts/index.vue'),
    meta: { title: '告警管理', icon: 'Bell' }
  },
  {
    path: '/rules',
    name: 'Rules',
    component: () => import('../views/rules/index.vue'),
    meta: { title: '规则管理', icon: 'Setting' }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('../views/notifications/index.vue'),
    meta: { title: '通知管理', icon: 'Message' }
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('../views/templates/index.vue'),
    meta: { title: '模板管理', icon: 'Document' }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('../views/analysis/index.vue'),
    meta: { title: '智能分析', icon: 'DataAnalysis' }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('../views/knowledge/index.vue'),
    meta: { title: '知识库', icon: 'Collection' }
  },
  {
    path: '/knowledge/query',
    name: 'KnowledgeQuery',
    component: () => import('../views/knowledge/query.vue'),
    meta: { title: '知识查询', icon: 'Search' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/index.vue'),
    meta: { title: '登录' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router