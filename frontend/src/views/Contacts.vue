<template>
  <div class="container">
    <div class="page-header">
      <h1 class="page-title">Contacts</h1>
    </div>
    
    <div v-if="loading" class="loading">Loading contacts...</div>
    <div v-else-if="contacts.length === 0" class="loading">No contacts found</div>
    
    <div v-else>
      <div v-for="contact in contacts" :key="contact.id" class="card">
        <h2 class="card-title">{{ contact.name }} {{ contact.is_primary ? '(Primary)' : '' }}</h2>
        <div class="card-content">
          <p><strong>Email:</strong> {{ contact.email }}</p>
          <p><strong>Phone:</strong> {{ contact.phone || 'N/A' }}</p>
          <p><strong>Position:</strong> {{ contact.position || 'N/A' }}</p>
          <p><strong>Lead:</strong> {{ contact.lead }}</p>
          
          <div style="margin-top: 1rem;">
            <button @click="viewCorrespondences(contact.id)" class="btn btn-sm btn-primary">
              View Correspondence
            </button>
            <button @click="addCorrespondence(contact.id)" class="btn btn-sm btn-success">
              Log Correspondence
            </button>
          </div>
          
          <!-- Correspondences -->
          <div v-if="selectedContactId === contact.id && correspondences.length > 0" style="margin-top: 1rem;">
            <h3>Correspondence History</h3>
            <div v-for="corr in correspondences" :key="corr.id" class="card" style="background: #f8f9fa;">
              <p><strong>{{ corr.type }}</strong> - {{ formatDate(corr.date) }}</p>
              <p><strong>Subject:</strong> {{ corr.subject }}</p>
              <p>{{ corr.description }}</p>
              <p><em>Logged by: {{ corr.logged_by?.username }}</em></p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Correspondence Modal -->
    <div v-if="showCorrModal" class="modal-overlay" @click.self="showCorrModal = false">
      <div class="modal">
        <div class="modal-header">
          <h2 class="modal-title">Log Correspondence</h2>
          <button @click="showCorrModal = false" class="modal-close">&times;</button>
        </div>
        
        <form @submit.prevent="submitCorrespondence">
          <div class="form-group">
            <label class="form-label">Type *</label>
            <select v-model="corrForm.type" class="form-select" required>
              <option value="email">Email</option>
              <option value="phone">Phone Call</option>
              <option value="meeting">Meeting</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div class="form-group">
            <label class="form-label">Subject *</label>
            <input v-model="corrForm.subject" type="text" class="form-input" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Date & Time *</label>
            <input v-model="corrForm.date" type="datetime-local" class="form-input" required />
          </div>
          
          <div class="form-group">
            <label class="form-label">Description *</label>
            <textarea v-model="corrForm.description" class="form-textarea" required></textarea>
          </div>
          
          <div class="actions">
            <button type="submit" class="btn btn-primary">Log</button>
            <button type="button" @click="showCorrModal = false" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { correspondenceAPI, contactAPI } from '@/services/api'

export default {
  name: 'Contacts',
  setup() {
    const store = useStore()
    
    const selectedContactId = ref(null)
    const correspondences = ref([])
    const showCorrModal = ref(false)
    const currentContactId = ref(null)
    
    const corrForm = ref({
      type: 'email',
      subject: '',
      date: '',
      description: ''
    })
    
    const contacts = computed(() => store.state.contacts.contacts)
    const loading = computed(() => store.state.contacts.loading)
    
    const formatDate = (date) => {
      return new Date(date).toLocaleString()
    }
    
    const viewCorrespondences = async (contactId) => {
      if (selectedContactId.value === contactId) {
        selectedContactId.value = null
        correspondences.value = []
      } else {
        try {
          const response = await contactAPI.getCorrespondences(contactId)
          correspondences.value = response.data
          selectedContactId.value = contactId
        } catch (error) {
          console.error('Failed to fetch correspondences:', error)
        }
      }
    }
    
    const addCorrespondence = (contactId) => {
      currentContactId.value = contactId
      corrForm.value.date = new Date().toISOString().slice(0, 16)
      showCorrModal.value = true
    }
    
    const submitCorrespondence = async () => {
      try {
        await correspondenceAPI.create({
          ...corrForm.value,
          contact: currentContactId.value
        })
        showCorrModal.value = false
        corrForm.value = {
          type: 'email',
          subject: '',
          date: '',
          description: ''
        }
        
        // Refresh correspondences if viewing
        if (selectedContactId.value === currentContactId.value) {
          viewCorrespondences(currentContactId.value)
        }
      } catch (error) {
        console.error('Failed to log correspondence:', error)
      }
    }
    
    onMounted(() => {
      store.dispatch('contacts/fetchContacts')
    })
    
    return {
      contacts,
      loading,
      selectedContactId,
      correspondences,
      showCorrModal,
      corrForm,
      formatDate,
      viewCorrespondences,
      addCorrespondence,
      submitCorrespondence
    }
  }
}
</script>



