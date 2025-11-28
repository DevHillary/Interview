import { authAPI } from '@/services/api'

/**
 * Authentication state management module
 * Handles user authentication, JWT tokens, and user role management
 */

const state = {
  token: localStorage.getItem('token') || null,  // JWT access token
  user: JSON.parse(localStorage.getItem('user') || 'null'),  // Current user object
  loading: false,  // Loading state for async operations
  error: null,  // Error message for failed operations
}

const getters = {
  // Check if user is authenticated (has valid token)
  isAuthenticated: (state) => !!state.token,
  
  // Check if current user has manager role
  isManager: (state) => state.user?.role === 'manager',
  
  // Check if current user has agent role
  isAgent: (state) => state.user?.role === 'agent',
  
  // Get current user object
  currentUser: (state) => state.user,
}

const actions = {
  /**
   * Login action - authenticates user and stores JWT token
   * @param {Object} credentials - User login credentials (username, password)
   * @returns {Object} Success status and error message if failed
   */
  async login({ commit }, credentials) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await authAPI.login(credentials)
      const { access, user } = response.data
      
      // Store token and user data in localStorage for persistence
      localStorage.setItem('token', access)
      localStorage.setItem('user', JSON.stringify(user))
      
      // Update Vuex state
      commit('SET_TOKEN', access)
      commit('SET_USER', user)
      commit('SET_LOADING', false)
      
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed'
      commit('SET_ERROR', message)
      commit('SET_LOADING', false)
      return { success: false, error: message }
    }
  },

  async register({ commit }, userData) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      await authAPI.register(userData)
      commit('SET_LOADING', false)
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed'
      commit('SET_ERROR', message)
      commit('SET_LOADING', false)
      return { success: false, error: message }
    }
  },

  /**
   * Fetch current user profile from API
   * Updates the user state with latest information
   */
  async fetchCurrentUser({ commit }) {
    try {
      const response = await authAPI.getCurrentUser()
      commit('SET_USER', response.data)
      localStorage.setItem('user', JSON.stringify(response.data))
      return { success: true, user: response.data }
    } catch (error) {
      console.error('Failed to fetch current user:', error)
      return { success: false, error: error.response?.data?.detail || 'Failed to fetch user' }
    }
  },

  /**
   * Update user profile information
   * @param {Object} userData - Updated user data (email, first_name, last_name, phone)
   * @returns {Object} Success status and updated user data
   */
  async updateProfile({ commit }, userData) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // Use PATCH to update user profile
      const response = await authAPI.updateProfile(userData)
      commit('SET_USER', response.data)
      localStorage.setItem('user', JSON.stringify(response.data))
      commit('SET_LOADING', false)
      return { success: true, user: response.data }
    } catch (error) {
      const message = error.response?.data?.detail || error.response?.data || 'Failed to update profile'
      commit('SET_ERROR', message)
      commit('SET_LOADING', false)
      return { success: false, error: message }
    }
  },

  /**
   * Logout action - clears authentication data
   */
  logout({ commit }) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    commit('SET_TOKEN', null)
    commit('SET_USER', null)
  },
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
  },
  SET_USER(state, user) {
    state.user = user
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


