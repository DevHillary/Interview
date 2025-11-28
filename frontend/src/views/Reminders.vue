<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Reminders</h1>
    </div>
    
    <!-- Filter -->
    <div class="search-filters">
      <select v-model="statusFilter" @change="handleFilter" class="form-select">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="sent">Sent</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>
    
    <div v-if="loading" class="loading">Loading reminders...</div>
    <div v-else-if="reminders.length === 0" class="loading">No reminders found</div>
    
    <div v-else>
      <div v-for="reminder in reminders" :key="reminder.id" class="card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
          <div>
            <h2 class="card-title">{{ reminder.title }}</h2>
            <div class="card-content">
              <p><strong>Date:</strong> {{ formatDate(reminder.reminder_date) }}</p>
              <p><strong>Lead:</strong> Lead #{{ reminder.lead }}</p>
              <p><strong>Status:</strong> <span :class="`badge badge-${reminder.status}`">{{ reminder.status }}</span></p>
              <p v-if="reminder.is_overdue" class="error">⚠️ Overdue</p>
              <p>{{ reminder.description }}</p>
            </div>
          </div>
          <div class="actions">
            <button 
              v-if="reminder.status === 'pending'"
              @click="updateStatus(reminder.id, 'sent')" 
              class="btn btn-sm btn-success"
            >
              Mark as Sent
            </button>
            <button 
              v-if="reminder.status === 'pending'"
              @click="updateStatus(reminder.id, 'cancelled')" 
              class="btn btn-sm btn-danger"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Reminders',
  setup() {
    const store = useStore()
    
    const statusFilter = ref('')
    
    const reminders = computed(() => store.state.reminders.reminders)
    const loading = computed(() => store.state.reminders.loading)
    
    const formatDate = (date) => {
      return new Date(date).toLocaleString()
    }
    
    const handleFilter = () => {
      const params = {}
      if (statusFilter.value) params.status = statusFilter.value
      store.dispatch('reminders/fetchReminders', params)
    }
    
    const updateStatus = async (id, status) => {
      await store.dispatch('reminders/updateReminder', {
        id,
        data: { status }
      })
      handleFilter()
    }
    
    onMounted(() => {
      store.dispatch('reminders/fetchReminders')
    })
    
    return {
      reminders,
      loading,
      statusFilter,
      formatDate,
      handleFilter,
      updateStatus
    }
  }
}
</script>



