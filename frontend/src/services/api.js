/**
 * API Service Module
 * Central configuration for all API calls to the Django backend
 */

import axios from 'axios'

// API base URL - defaults to localhost for development
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request Interceptor
 * Automatically adds JWT token to all outgoing requests
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response Interceptor
 * Handles authentication errors globally
 * Redirects to login page if token is invalid or expired
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear stored authentication data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Redirect to login page
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

/**
 * Authentication API endpoints
 */
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login/', credentials),
  register: (userData) => api.post('/api/auth/register/', userData),
  getCurrentUser: () => api.get('/api/auth/me/'),
  updateProfile: (userData) => api.patch('/api/auth/me/', userData),
  refreshToken: (refresh) => api.post('/api/auth/token/refresh/', { refresh }),
}

/**
 * Lead management API endpoints
 */
export const leadAPI = {
  getAll: (params) => api.get('/api/leads/', { params }),
  getOne: (id) => api.get(`/api/leads/${id}/`),
  create: (data) => api.post('/api/leads/', data),
  update: (id, data) => api.patch(`/api/leads/${id}/`, data),
  delete: (id) => api.delete(`/api/leads/${id}/`),
  getMyLeads: () => api.get('/api/leads/my_leads/'),
  getAuditLog: (id) => api.get(`/api/leads/${id}/audit_log/`),
}

/**
 * Contact management API endpoints
 */
export const contactAPI = {
  getAll: (params) => api.get('/api/contacts/', { params }),
  getOne: (id) => api.get(`/api/contacts/${id}/`),
  create: (data) => api.post('/api/contacts/', data),
  update: (id, data) => api.patch(`/api/contacts/${id}/`, data),
  delete: (id) => api.delete(`/api/contacts/${id}/`),
  getCorrespondences: (id) => api.get(`/api/contacts/${id}/correspondences/`),
}

/**
 * Note management API endpoints
 */
export const noteAPI = {
  getAll: (params) => api.get('/api/notes/', { params }),
  create: (data) => api.post('/api/notes/', data),
  update: (id, data) => api.patch(`/api/notes/${id}/`, data),
  delete: (id) => api.delete(`/api/notes/${id}/`),
}

/**
 * Reminder management API endpoints
 */
export const reminderAPI = {
  getAll: (params) => api.get('/api/reminders/', { params }),
  getOne: (id) => api.get(`/api/reminders/${id}/`),
  create: (data) => api.post('/api/reminders/', data),
  update: (id, data) => api.patch(`/api/reminders/${id}/`, data),
  delete: (id) => api.delete(`/api/reminders/${id}/`),
  getMyReminders: () => api.get('/api/reminders/my_reminders/'),
  getOverdue: () => api.get('/api/reminders/overdue/'),
}

/**
 * Correspondence tracking API endpoints
 */
export const correspondenceAPI = {
  getAll: (params) => api.get('/api/correspondences/', { params }),
  create: (data) => api.post('/api/correspondences/', data),
  update: (id, data) => api.patch(`/api/correspondences/${id}/`, data),
  delete: (id) => api.delete(`/api/correspondences/${id}/`),
}

export default api


