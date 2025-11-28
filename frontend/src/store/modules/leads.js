import { leadAPI } from '@/services/api'

const state = {
  leads: [],
  currentLead: null,
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
  },
}

const getters = {
  allLeads: (state) => state.leads,
  currentLead: (state) => state.currentLead,
  isLoading: (state) => state.loading,
}

const actions = {
  async fetchLeads({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await leadAPI.getAll(params)
      commit('SET_LEADS', response.data.results || response.data)
      if (response.data.count) {
        commit('SET_PAGINATION', {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
        })
      }
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch leads')
      commit('SET_LOADING', false)
    }
  },

  async fetchLead({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await leadAPI.getOne(id)
      commit('SET_CURRENT_LEAD', response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch lead')
      commit('SET_LOADING', false)
    }
  },

  async createLead({ commit }, leadData) {
    commit('SET_LOADING', true)
    try {
      const response = await leadAPI.create(leadData)
      commit('ADD_LEAD', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create lead')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async updateLead({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await leadAPI.update(id, data)
      commit('UPDATE_LEAD', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update lead')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async deleteLead({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await leadAPI.delete(id)
      commit('REMOVE_LEAD', id)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete lead')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },
}

const mutations = {
  SET_LEADS(state, leads) {
    state.leads = leads
  },
  SET_CURRENT_LEAD(state, lead) {
    state.currentLead = lead
  },
  ADD_LEAD(state, lead) {
    state.leads.unshift(lead)
  },
  UPDATE_LEAD(state, updatedLead) {
    const index = state.leads.findIndex((l) => l.id === updatedLead.id)
    if (index !== -1) {
      state.leads.splice(index, 1, updatedLead)
    }
    if (state.currentLead?.id === updatedLead.id) {
      state.currentLead = updatedLead
    }
  },
  REMOVE_LEAD(state, id) {
    state.leads = state.leads.filter((l) => l.id !== id)
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_PAGINATION(state, pagination) {
    state.pagination = pagination
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}



