<template>
  <div class="container">
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="lead">
      <div class="page-header">
        <h1 class="page-title">{{ lead.name }} - {{ lead.company }}</h1>
        <router-link to="/leads" class="btn btn-secondary">Back to Leads</router-link>
      </div>
      
      <!-- Lead Details -->
      <div class="card">
        <h2 class="card-title">Lead Information</h2>
        <div class="card-content">
          <p><strong>Email:</strong> {{ lead.email }}</p>
          <p><strong>Phone:</strong> {{ lead.phone || 'N/A' }}</p>
          <p><strong>Status:</strong> <span :class="`badge badge-${lead.status}`">{{ lead.status }}</span></p>
          <p><strong>Priority:</strong> <span :class="`badge badge-${lead.priority}`">{{ lead.priority }}</span></p>
          <p><strong>Source:</strong> {{ lead.source || 'N/A' }}</p>
          <p><strong>Owner:</strong> {{ lead.owner?.username || 'N/A' }}</p>
          <p><strong>Estimated Value:</strong> ${{ lead.estimated_value || '0.00' }}</p>
          <p><strong>Description:</strong> {{ lead.description || 'N/A' }}</p>
        </div>
      </div>
      
      <!-- Contacts -->
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h2 class="card-title" style="margin: 0;">Contacts</h2>
          <button @click="showContactModal = true" class="btn btn-sm btn-primary">Add Contact</button>
        </div>
        
        <div v-if="lead.contacts && lead.contacts.length > 0">
          <div v-for="contact in lead.contacts" :key="contact.id" class="card" style="background: #f8f9fa;">
            <h3>{{ contact.name }} {{ contact.is_primary ? '(Primary)' : '' }}</h3>
            <p><strong>Email:</strong> {{ contact.email }}</p>
            <p><strong>Phone:</strong> {{ contact.phone || 'N/A' }}</p>
            <p><strong>Position:</strong> {{ contact.position || 'N/A' }}</p>
            <p><strong>Notes:</strong> {{ contact.notes || 'N/A' }}</p>
            <button @click="viewCorrespondences(contact.id)" class="btn btn-sm btn-secondary">
              View Correspondence
            </button>
          </div>
        </div>
        <p v-else>No contacts found</p>
      </div>
      
      <!-- Notes -->
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h2 class="card-title" style="margin: 0;">Notes</h2>
          <button @click="showNoteModal = true" class="btn btn-sm btn-primary">Add Note</button>
        </div>
        
        <div v-if="lead.notes && lead.notes.length > 0">
          <div v-for="note in lead.notes" :key="note.id" class="card" style="background: #f8f9fa;">
            <p><strong>{{ note.author?.username }}</strong> - {{ formatDate(note.created_at) }}</p>
            <p>{{ note.content }}</p>
          </div>
        </div>
        <p v-else>No notes found</p>
      </div>
      
      <!-- Reminders -->
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h2 class="card-title" style="margin: 0;">Reminders</h2>
          <button @click="showReminderModal = true" class="btn btn-sm btn-primary">Add Reminder</button>
        </div>
        
        <div v-if="lead.reminders && lead.reminders.length > 0">
          <div v-for="reminder in lead.reminders" :key="reminder.id" class="card" style="background: #f8f9fa;">
            <h3>{{ reminder.title }}</h3>
            <p><strong>Date:</strong> {{ formatDate(reminder.reminder_date) }}</p>
            <p><strong>Status:</strong> <span :class="`badge badge-${reminder.status}`">{{ reminder.status }}</span></p>
            <p>{{ reminder.description }}</p>
          </div>
        </div>
        <p v-else>No reminders found</p>
      </div>
      
      <!-- Contact Modal -->
      <div v-if="showContactModal" class="modal-overlay" @click.self="showContactModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Add Contact</h2>
            <button @click="showContactModal = false" class="modal-close">&times;</button>
          </div>
          
          <form @submit.prevent="addContact">
            <div class="form-group">
              <label class="form-label">Name *</label>
              <input v-model="contactForm.name" type="text" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Email *</label>
              <input v-model="contactForm.email" type="email" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Phone</label>
              <input v-model="contactForm.phone" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Position</label>
              <input v-model="contactForm.position" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label style="display: flex; align-items: center; gap: 0.5rem;">
                <input v-model="contactForm.is_primary" type="checkbox" />
                <span>Primary Contact</span>
              </label>
            </div>
            <div class="actions">
              <button type="submit" class="btn btn-primary">Add</button>
              <button type="button" @click="showContactModal = false" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Note Modal -->
      <div v-if="showNoteModal" class="modal-overlay" @click.self="showNoteModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Add Note</h2>
            <button @click="showNoteModal = false" class="modal-close">&times;</button>
          </div>
          
          <form @submit.prevent="addNote">
            <div class="form-group">
              <label class="form-label">Content *</label>
              <textarea v-model="noteForm.content" class="form-textarea" required></textarea>
            </div>
            <div class="actions">
              <button type="submit" class="btn btn-primary">Add</button>
              <button type="button" @click="showNoteModal = false" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Reminder Modal -->
      <div v-if="showReminderModal" class="modal-overlay" @click.self="showReminderModal = false">
        <div class="modal">
          <div class="modal-header">
            <h2 class="modal-title">Add Reminder</h2>
            <button @click="showReminderModal = false" class="modal-close">&times;</button>
          </div>
          
          <form @submit.prevent="addReminder">
            <div class="form-group">
              <label class="form-label">Title *</label>
              <input v-model="reminderForm.title" type="text" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Date & Time *</label>
              <input v-model="reminderForm.reminder_date" type="datetime-local" class="form-input" required />
            </div>
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea v-model="reminderForm.description" class="form-textarea"></textarea>
            </div>
            <div class="actions">
              <button type="submit" class="btn btn-primary">Add</button>
              <button type="button" @click="showReminderModal = false" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import { noteAPI, contactAPI, reminderAPI } from '@/services/api'

export default {
  name: 'LeadDetail',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    
    const showContactModal = ref(false)
    const showNoteModal = ref(false)
    const showReminderModal = ref(false)
    
    const contactForm = ref({ name: '', email: '', phone: '', position: '', is_primary: false })
    const noteForm = ref({ content: '' })
    const reminderForm = ref({ title: '', reminder_date: '', description: '' })
    
    const lead = computed(() => store.state.leads.currentLead)
    const loading = computed(() => store.state.leads.loading)
    
    const formatDate = (date) => {
      return new Date(date).toLocaleString()
    }
    
    const addContact = async () => {
      const result = await store.dispatch('contacts/createContact', {
        ...contactForm.value,
        lead: route.params.id
      })
      if (result.success) {
        showContactModal.value = false
        contactForm.value = { name: '', email: '', phone: '', position: '', is_primary: false }
        store.dispatch('leads/fetchLead', route.params.id)
      }
    }
    
    const addNote = async () => {
      try {
        await noteAPI.create({
          ...noteForm.value,
          lead: route.params.id
        })
        showNoteModal.value = false
        noteForm.value = { content: '' }
        store.dispatch('leads/fetchLead', route.params.id)
      } catch (error) {
        console.error('Failed to add note:', error)
      }
    }
    
    const addReminder = async () => {
      const result = await store.dispatch('reminders/createReminder', {
        ...reminderForm.value,
        lead: route.params.id
      })
      if (result.success) {
        showReminderModal.value = false
        reminderForm.value = { title: '', reminder_date: '', description: '' }
        store.dispatch('leads/fetchLead', route.params.id)
      }
    }
    
    const viewCorrespondences = (contactId) => {
      router.push(`/contacts?contact=${contactId}`)
    }
    
    onMounted(() => {
      store.dispatch('leads/fetchLead', route.params.id)
    })
    
    return {
      lead,
      loading,
      showContactModal,
      showNoteModal,
      showReminderModal,
      contactForm,
      noteForm,
      reminderForm,
      formatDate,
      addContact,
      addNote,
      addReminder,
      viewCorrespondences
    }
  }
}
</script>



