import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    alerts: [],
    notifications: [],
    rules: [],
    templates: []
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setAlerts(state, alerts) {
      state.alerts = alerts
    },
    setNotifications(state, notifications) {
      state.notifications = notifications
    },
    setRules(state, rules) {
      state.rules = rules
    },
    setTemplates(state, templates) {
      state.templates = templates
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(credentials)
        })
        if (response.ok) {
          const data = await response.json()
          commit('setUser', data.user)
          localStorage.setItem('token', data.access_token)
          return true
        }
        return false
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },
    async fetchAlerts({ commit }) {
      try {
        const response = await fetch('/api/v1/alerts')
        const data = await response.json()
        commit('setAlerts', data)
      } catch (error) {
        console.error('Failed to fetch alerts:', error)
      }
    },
    async fetchNotifications({ commit }) {
      try {
        const response = await fetch('/api/v1/notifications')
        const data = await response.json()
        commit('setNotifications', data)
      } catch (error) {
        console.error('Failed to fetch notifications:', error)
      }
    },
    async fetchRules({ commit }) {
      try {
        const response = await fetch('/api/v1/rules')
        const data = await response.json()
        commit('setRules', data)
      } catch (error) {
        console.error('Failed to fetch rules:', error)
      }
    },
    async fetchTemplates({ commit }) {
      try {
        const response = await fetch('/api/v1/templates')
        const data = await response.json()
        commit('setTemplates', data)
      } catch (error) {
        console.error('Failed to fetch templates:', error)
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    allAlerts: state => state.alerts,
    allNotifications: state => state.notifications,
    allRules: state => state.rules,
    allTemplates: state => state.templates
  }
})