<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Leads</h1>
      <div class="actions">
        <button @click="exportToCSV" class="btn btn-success">Export to CSV</button>
        <button @click="showCreateModal = true" class="btn btn-primary">Create Lead</button>
      </div>
    </div>
    
    <!-- Search and Filters -->
    <div class="search-filters">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        type="text"
        placeholder="Search leads..."
        class="form-input search-input"
      />
      <select v-model="statusFilter" @change="handleFilter" class="form-select">
        <option value="">All Status</option>
        <option value="new">New</option>
        <option value="contacted">Contacted</option>
        <option value="qualified">Qualified</option>
        <option value="lost">Lost</option>
        <option value="converted">Converted</option>
      </select>
      <select v-model="priorityFilter" @change="handleFilter" class="form-select">
        <option value="">All Priority</option>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>
    
    <div v-if="loading" class="loading">Loading leads...</div>
    <div v-else-if="leads.length === 0" class="loading">No leads found</div>
    
    <table v-else class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Company</th>
          <th>Email</th>
          <th>Status</th>
          <th>Priority</th>
          <th>Owner</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lead in leads" :key="lead.id">
          <td>{{ lead.name }}</td>
          <td>{{ lead.company }}</td>
          <td>{{ lead.email }}</td>
          <td><span :class="`badge badge-${lead.status}`">{{ lead.status }}</span></td>
          <td><span :class="`badge badge-${lead.priority}`">{{ lead.priority }}</span></td>
          <td>{{ lead.owner?.username || 'N/A' }}</td>
          <td class="actions">
            <router-link :to="`/leads/${lead.id}`" class="btn btn-sm btn-primary">View</router-link>
            <button @click="editLead(lead)" class="btn btn-sm btn-secondary">Edit</button>
            <button v-if="isManager" @click="deleteLead(lead.id)" class="btn btn-sm btn-danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModals">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">{{ showEditModal ? 'Edit Lead' : 'Create Lead' }}</h2>
          <button @click="closeModals" class="modal-close">&times;</button>
        </div>
        
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label class="form-label">Name *</label>
            <input v-model="formData.name" type="text" class="form-input" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Company</label>
            <input v-model="formData.company" type="text" class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Email *</label>
            <input v-model="formData.email" type="email" class="form-input" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Phone</label>
            <input v-model="formData.phone" type="text" class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Status</label>
            <select v-model="formData.status" class="form-select">
              <option value="new">New</option>
              <option value="contacted">Contacted</option>
              <option value="qualified">Qualified</option>
              <option value="lost">Lost</option>
              <option value="converted">Converted</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Priority</label>
            <select v-model="formData.priority" class="form-select">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Source</label>
            <input v-model="formData.source" type="text" class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Estimated Value</label>
            <input v-model="formData.estimated_value" type="number" step="0.01" class="form-input" />
          </div>
          
          <div class="form-group">
            <label class="form-label">Description</label>
            <textarea v-model="formData.description" class="form-textarea"></textarea>
          </div>
          
          <div class="actions">
            <button type="submit" class="btn btn-primary">{{ showEditModal ? 'Update' : 'Create' }}</button>
            <button type="button" @click="closeModals" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Leads',
  setup() {
    const store = useStore()
    
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const searchQuery = ref('')
    const statusFilter = ref('')
    const priorityFilter = ref('')
    
    const formData = ref({
      name: '',
      company: '',
      email: '',
      phone: '',
      status: 'new',
      priority: 'medium',
      source: '',
      estimated_value: null,
      description: ''
    })
    
    const currentLeadId = ref(null)
    
    const leads = computed(() => store.state.leads.leads)
    const loading = computed(() => store.state.leads.loading)
    const isManager = computed(() => store.getters['auth/isManager'])
    
    const fetchLeads = () => {
      const params = {}
      if (searchQuery.value) params.search = searchQuery.value
      if (statusFilter.value) params.status = statusFilter.value
      if (priorityFilter.value) params.priority = priorityFilter.value
      store.dispatch('leads/fetchLeads', params)
    }
    
    const handleSearch = () => {
      fetchLeads()
    }
    
    const handleFilter = () => {
      fetchLeads()
    }
    
    const editLead = (lead) => {
      currentLeadId.value = lead.id
      formData.value = { ...lead }
      showEditModal.value = true
    }
    
    const handleSubmit = async () => {
      if (showEditModal.value) {
        const result = await store.dispatch('leads/updateLead', {
          id: currentLeadId.value,
          data: formData.value
        })
        if (result.success) {
          closeModals()
        }
      } else {
        const result = await store.dispatch('leads/createLead', formData.value)
        if (result.success) {
          closeModals()
        }
      }
    }
    
    const deleteLead = async (id) => {
      if (confirm('Are you sure you want to delete this lead?')) {
        await store.dispatch('leads/deleteLead', id)
      }
    }
    
    const closeModals = () => {
      showCreateModal.value = false
      showEditModal.value = false
      currentLeadId.value = null
      formData.value = {
        name: '',
        company: '',
        email: '',
        phone: '',
        status: 'new',
        priority: 'medium',
        source: '',
        estimated_value: null,
        description: ''
      }
    }
    
    const exportToCSV = () => {
      const token = localStorage.getItem('token')
      const params = new URLSearchParams()
      if (statusFilter.value) params.append('status', statusFilter.value)
      if (priorityFilter.value) params.append('priority', priorityFilter.value)
      
      const url = `http://localhost:8000/api/leads/export/csv/?${params.toString()}`
      
      // Create a temporary link and trigger download
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'leads_export.csv')
      link.style.display = 'none'
      
      // Add authorization header by using fetch
      fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'leads_export.csv'
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      })
      .catch(error => {
        console.error('Export failed:', error)
        alert('Failed to export leads')
      })
    }
    
    onMounted(() => {
      fetchLeads()
    })
    
    return {
      leads,
      loading,
      isManager,
      showCreateModal,
      showEditModal,
      searchQuery,
      statusFilter,
      priorityFilter,
      formData,
      handleSearch,
      handleFilter,
      editLead,
      handleSubmit,
      deleteLead,
      closeModals,
      exportToCSV
    }
  }
}
</script>


