import { reminderAPI } from '@/services/api'

const state = {
  reminders: [],
  loading: false,
  error: null,
}

const getters = {
  allReminders: (state) => state.reminders,
  pendingReminders: (state) => state.reminders.filter(r => r.status === 'pending'),
}

const actions = {
  async fetchReminders({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await reminderAPI.getAll(params)
      commit('SET_REMINDERS', response.data.results || response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch reminders')
      commit('SET_LOADING', false)
    }
  },

  async createReminder({ commit }, reminderData) {
    commit('SET_LOADING', true)
    try {
      const response = await reminderAPI.create(reminderData)
      commit('ADD_REMINDER', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create reminder')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async updateReminder({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await reminderAPI.update(id, data)
      commit('UPDATE_REMINDER', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update reminder')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async deleteReminder({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await reminderAPI.delete(id)
      commit('REMOVE_REMINDER', id)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete reminder')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },
}

const mutations = {
  SET_REMINDERS(state, reminders) {
    state.reminders = reminders
  },
  ADD_REMINDER(state, reminder) {
    state.reminders.unshift(reminder)
  },
  UPDATE_REMINDER(state, updatedReminder) {
    const index = state.reminders.findIndex((r) => r.id === updatedReminder.id)
    if (index !== -1) {
      state.reminders.splice(index, 1, updatedReminder)
    }
  },
  REMOVE_REMINDER(state, id) {
    state.reminders = state.reminders.filter((r) => r.id !== id)
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}



