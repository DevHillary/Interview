<template>
  <div class="container">
    <h1 class="page-title">Dashboard</h1>
    
    <div v-if="loading" class="loading">Loading dashboard...</div>
    
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else>
      <!-- Stats Grid -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon" style="background: #3498db;">📊</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.total_leads }}</h3>
            <p class="stat-label">Total Leads</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon" style="background: #e74c3c;">🆕</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.new_leads }}</h3>
            <p class="stat-label">New Leads</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon" style="background: #f39c12;">📞</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.contacted_leads }}</h3>
            <p class="stat-label">Contacted</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon" style="background: #27ae60;">✅</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.converted_leads }}</h3>
            <p class="stat-label">Converted</p>
          </div>
        </div>
        
        <div class="stat-card stat-card-large">
          <div class="stat-icon" style="background: #9b59b6;">💰</div>
          <div class="stat-content">
            <h3 class="stat-number">KES {{ formatCurrency(stats.total_value) }}</h3>
            <p class="stat-label">Total Pipeline Value</p>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon" style="background: #1abc9c;">👥</div>
          <div class="stat-content">
            <h3 class="stat-number">{{ stats.total_contacts }}</h3>
            <p class="stat-label">Total Contacts</p>
          </div>
        </div>
      </div>
      
      <!-- Charts Row -->
      <div class="charts-row">
        <!-- Status Distribution -->
        <div class="chart-card">
          <h2 class="card-title">Leads by Status</h2>
          <div class="chart-content">
            <div v-for="(count, status) in stats.status_distribution" :key="status" class="status-bar-item">
              <div class="status-bar-label">
                <span :class="`badge badge-${status}`">{{ status }}</span>
                <span class="count">{{ count }}</span>
              </div>
              <div class="bar-container">
                <div 
                  class="bar" 
                  :class="`bar-${status}`"
                  :style="{width: (count / stats.total_leads * 100) + '%'}"
                ></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Priority Distribution -->
        <div class="chart-card">
          <h2 class="card-title">Leads by Priority</h2>
          <div class="chart-content">
            <div v-for="(count, priority) in stats.priority_distribution" :key="priority" class="status-bar-item">
              <div class="status-bar-label">
                <span :class="`badge badge-${priority}`">{{ priority }}</span>
                <span class="count">{{ count }}</span>
              </div>
              <div class="bar-container">
                <div 
                  class="bar" 
                  :class="`bar-${priority}`"
                  :style="{width: (count / stats.total_leads * 100) + '%'}"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Activity and Reminders Row -->
      <div class="activity-row">
        <!-- Recent Activity -->
        <div class="activity-card">
          <h2 class="card-title">Recent Activity</h2>
          <div class="activity-list">
            <div v-for="activity in stats.recent_activity" :key="activity.id" class="activity-item">
              <div class="activity-icon">
                <span v-if="activity.action === 'Create'">➕</span>
                <span v-else-if="activity.action === 'Update'">✏️</span>
                <span v-else>🗑️</span>
              </div>
              <div class="activity-content">
                <p class="activity-text">
                  <strong>{{ activity.user }}</strong> {{ activity.action.toLowerCase() }}d 
                  {{ activity.model }} <em>{{ activity.object }}</em>
                </p>
                <p class="activity-time">{{ formatTimeAgo(activity.timestamp) }}</p>
              </div>
            </div>
            <div v-if="stats.recent_activity.length === 0" class="empty-state">
              No recent activity
            </div>
          </div>
        </div>
        
        <!-- Upcoming Reminders -->
        <div class="reminders-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 class="card-title">Upcoming Reminders</h2>
            <span v-if="stats.overdue_reminders_count > 0" class="overdue-badge">
              {{ stats.overdue_reminders_count }} Overdue
            </span>
          </div>
          <div class="reminders-list">
            <div v-for="reminder in stats.upcoming_reminders" :key="reminder.id" class="reminder-item">
              <div class="reminder-icon">⏰</div>
              <div class="reminder-content">
                <p class="reminder-title">{{ reminder.title }}</p>
                <p class="reminder-lead">{{ reminder.lead }}</p>
                <p class="reminder-date">{{ formatDate(reminder.date) }}</p>
              </div>
            </div>
            <div v-if="stats.upcoming_reminders.length === 0" class="empty-state">
              No upcoming reminders
            </div>
          </div>
          <router-link to="/reminders" class="view-all-link">View all reminders →</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Dashboard',
  setup() {
    // Initialize dashboard statistics state
    const stats = ref({
      total_leads: 0,
      new_leads: 0,
      contacted_leads: 0,
      qualified_leads: 0,
      converted_leads: 0,
      lost_leads: 0,
      total_value: 0,
      total_contacts: 0,
      total_notes: 0,
      status_distribution: {},
      priority_distribution: {},
      recent_activity: [],
      upcoming_reminders: [],
      overdue_reminders_count: 0
    })
    
    // UI state management
    const loading = ref(true)
    const error = ref(null)
    
    /**
     * Fetch dashboard statistics from the API
     * Retrieves aggregated data for leads, contacts, and activity
     */
    const fetchDashboardStats = async () => {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get('http://localhost:8000/api/dashboard/stats/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        stats.value = response.data
        loading.value = false
      } catch (err) {
        error.value = 'Failed to load dashboard statistics'
        loading.value = false
        console.error('Dashboard error:', err)
      }
    }
    
    /**
     * Format numbers as Kenyan currency (KES)
     * @param {number} value - The numeric value to format
     * @returns {string} Formatted currency string without decimals
     */
    const formatCurrency = (value) => {
      return new Intl.NumberFormat('en-KE', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value)
    }
    
    /**
     * Format date in Kenyan locale
     * @param {string} date - ISO date string
     * @returns {string} Formatted date string (e.g., "Nov 28, 02:30 PM")
     */
    const formatDate = (date) => {
      return new Date(date).toLocaleString('en-KE', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    /**
     * Calculate relative time from now (e.g., "5 minutes ago")
     * @param {string} date - ISO date string
     * @returns {string} Human-readable relative time
     */
    const formatTimeAgo = (date) => {
      const seconds = Math.floor((new Date() - new Date(date)) / 1000)
      
      if (seconds < 60) return 'just now'
      if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`
      if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`
      return `${Math.floor(seconds / 86400)} days ago`
    }
    
    // Load dashboard data when component mounts
    onMounted(() => {
      fetchDashboardStats()
    })
    
    return {
      stats,
      loading,
      error,
      formatCurrency,
      formatDate,
      formatTimeAgo
    }
  }
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.stat-card-large {
  grid-column: span 2;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.stat-label {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
  font-weight: 500;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.chart-content {
  margin-top: 1.5rem;
}

.status-bar-item {
  margin-bottom: 1.25rem;
}

.status-bar-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.count {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.bar-container {
  background: #ecf0f1;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 5px;
  transition: width 0.6s ease;
}

.bar-new { background: linear-gradient(90deg, #3498db, #2980b9); }
.bar-contacted { background: linear-gradient(90deg, #f39c12, #e67e22); }
.bar-qualified { background: linear-gradient(90deg, #1abc9c, #16a085); }
.bar-converted { background: linear-gradient(90deg, #27ae60, #229954); }
.bar-lost { background: linear-gradient(90deg, #e74c3c, #c0392b); }
.bar-low { background: linear-gradient(90deg, #95a5a6, #7f8c8d); }
.bar-medium { background: linear-gradient(90deg, #f39c12, #e67e22); }
.bar-high { background: linear-gradient(90deg, #e74c3c, #c0392b); }

.activity-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.activity-card, .reminders-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.activity-list, .reminders-list {
  margin-top: 1rem;
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #ecf0f1;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #f8f9fa;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
  font-size: 0.95rem;
}

.activity-time {
  margin: 0;
  color: #95a5a6;
  font-size: 0.85rem;
}

.reminder-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-left: 3px solid #3498db;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 0.75rem;
  transition: all 0.2s;
}

.reminder-item:hover {
  background: #ecf0f1;
  border-left-color: #2980b9;
}

.reminder-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.reminder-content {
  flex: 1;
}

.reminder-title {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #2c3e50;
}

.reminder-lead {
  margin: 0 0 0.25rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.reminder-date {
  margin: 0;
  color: #3498db;
  font-size: 0.85rem;
  font-weight: 500;
}

.overdue-badge {
  background: #e74c3c;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.view-all-link {
  display: block;
  text-align: center;
  margin-top: 1rem;
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.view-all-link:hover {
  background: #ecf0f1;
  color: #2980b9;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #95a5a6;
  font-style: italic;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card-large {
    grid-column: span 1;
  }
  
  .charts-row, .activity-row {
    grid-template-columns: 1fr;
  }
}
</style>

