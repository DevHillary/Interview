import { contactAPI } from '@/services/api'

const state = {
  contacts: [],
  currentContact: null,
  loading: false,
  error: null,
}

const getters = {
  allContacts: (state) => state.contacts,
  currentContact: (state) => state.currentContact,
}

const actions = {
  async fetchContacts({ commit }, params = {}) {
    commit('SET_LOADING', true)
    try {
      const response = await contactAPI.getAll(params)
      commit('SET_CONTACTS', response.data.results || response.data)
      commit('SET_LOADING', false)
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch contacts')
      commit('SET_LOADING', false)
    }
  },

  async createContact({ commit }, contactData) {
    commit('SET_LOADING', true)
    try {
      const response = await contactAPI.create(contactData)
      commit('ADD_CONTACT', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create contact')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async updateContact({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await contactAPI.update(id, data)
      commit('UPDATE_CONTACT', response.data)
      commit('SET_LOADING', false)
      return { success: true, data: response.data }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update contact')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },

  async deleteContact({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await contactAPI.delete(id)
      commit('REMOVE_CONTACT', id)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete contact')
      commit('SET_LOADING', false)
      return { success: false, error: error.response?.data }
    }
  },
}

const mutations = {
  SET_CONTACTS(state, contacts) {
    state.contacts = contacts
  },
  SET_CURRENT_CONTACT(state, contact) {
    state.currentContact = contact
  },
  ADD_CONTACT(state, contact) {
    state.contacts.unshift(contact)
  },
  UPDATE_CONTACT(state, updatedContact) {
    const index = state.contacts.findIndex((c) => c.id === updatedContact.id)
    if (index !== -1) {
      state.contacts.splice(index, 1, updatedContact)
    }
  },
  REMOVE_CONTACT(state, id) {
    state.contacts = state.contacts.filter((c) => c.id !== id)
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



