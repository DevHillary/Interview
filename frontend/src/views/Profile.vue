<template>
  <div class="container">
    <div class="page-header">
      <h1>My Profile</h1>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>

    <!-- Error message -->
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <!-- Success message -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- Profile content -->
    <div v-if="!loading && user" class="profile-content">
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">
            <span class="avatar-text">{{ userInitials }}</span>
          </div>
          <div class="profile-info">
            <h2>{{ fullName || user.username }}</h2>
            <p class="profile-role">{{ roleDisplay }}</p>
            <p class="profile-email">{{ user.email }}</p>
          </div>
        </div>

        <div class="profile-actions">
          <button 
            @click="toggleEditMode" 
            class="btn"
            :class="{ 'btn-secondary': editMode }"
          >
            {{ editMode ? 'Cancel' : 'Edit Profile' }}
          </button>
        </div>
      </div>

      <!-- View mode -->
      <div v-if="!editMode" class="profile-details">
        <div class="detail-section">
          <h3>Personal Information</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <label>Username</label>
              <p>{{ user.username }}</p>
            </div>
            <div class="detail-item">
              <label>Email</label>
              <p>{{ user.email || 'Not provided' }}</p>
            </div>
            <div class="detail-item">
              <label>First Name</label>
              <p>{{ user.first_name || 'Not provided' }}</p>
            </div>
            <div class="detail-item">
              <label>Last Name</label>
              <p>{{ user.last_name || 'Not provided' }}</p>
            </div>
            <div class="detail-item">
              <label>Phone</label>
              <p>{{ user.phone || 'Not provided' }}</p>
            </div>
            <div class="detail-item">
              <label>Role</label>
              <p class="role-badge" :class="user.role">{{ roleDisplay }}</p>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h3>Account Information</h3>
          <div class="detail-grid">
            <div class="detail-item">
              <label>User ID</label>
              <p>{{ user.id }}</p>
            </div>
            <div class="detail-item">
              <label>Account Type</label>
              <p>{{ user.role === 'manager' ? 'Manager (Full Access)' : 'Agent (Limited Access)' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit mode -->
      <div v-else class="profile-edit">
        <form @submit.prevent="updateProfile" class="profile-form">
          <div class="form-section">
            <h3>Personal Information</h3>
            <div class="form-grid">
              <div class="form-group">
                <label for="email">Email Address *</label>
                <input
                  id="email"
                  v-model="editForm.email"
                  type="email"
                  class="form-control"
                  required
                />
              </div>
              <div class="form-group">
                <label for="first_name">First Name</label>
                <input
                  id="first_name"
                  v-model="editForm.first_name"
                  type="text"
                  class="form-control"
                />
              </div>
              <div class="form-group">
                <label for="last_name">Last Name</label>
                <input
                  id="last_name"
                  v-model="editForm.last_name"
                  type="text"
                  class="form-control"
                />
              </div>
              <div class="form-group">
                <label for="phone">Phone Number</label>
                <input
                  id="phone"
                  v-model="editForm.phone"
                  type="tel"
                  class="form-control"
                  placeholder="e.g., 254712345678"
                />
              </div>
            </div>
          </div>

          <div class="form-section">
            <h3>Account Information</h3>
            <div class="form-grid">
              <div class="form-group">
                <label>Username</label>
                <input
                  :value="user.username"
                  type="text"
                  class="form-control"
                  disabled
                />
                <small class="form-help">Username cannot be changed</small>
              </div>
              <div class="form-group">
                <label>Role</label>
                <input
                  :value="roleDisplay"
                  type="text"
                  class="form-control"
                  disabled
                />
                <small class="form-help">Role cannot be changed</small>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn" :disabled="saving">
              <span v-if="saving">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
            <button type="button" @click="cancelEdit" class="btn btn-secondary">
              Cancel
            </button>
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
  name: 'Profile',
  setup() {
    const store = useStore()
    
    // State management
    const loading = ref(true)
    const editMode = ref(false)
    const saving = ref(false)
    const error = ref(null)
    const successMessage = ref(null)
    
    // Get current user from store
    const user = computed(() => store.getters['auth/currentUser'])
    
    // Edit form data
    const editForm = ref({
      email: '',
      first_name: '',
      last_name: '',
      phone: ''
    })
    
    /**
     * Computed property for user initials (for avatar)
     */
    const userInitials = computed(() => {
      if (user.value) {
        const first = user.value.first_name?.[0] || user.value.username[0]
        const last = user.value.last_name?.[0] || user.value.username[1] || ''
        return (first + last).toUpperCase()
      }
      return 'U'
    })
    
    /**
     * Computed property for full name
     */
    const fullName = computed(() => {
      if (user.value?.first_name || user.value?.last_name) {
        return `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
      }
      return null
    })
    
    /**
     * Computed property for role display
     */
    const roleDisplay = computed(() => {
      if (user.value?.role) {
        return user.value.role.charAt(0).toUpperCase() + user.value.role.slice(1)
      }
      return 'User'
    })
    
    /**
     * Fetch user profile data
     */
    const fetchProfile = async () => {
      loading.value = true
      error.value = null
      const result = await store.dispatch('auth/fetchCurrentUser')
      if (result.success) {
        // Initialize edit form with current user data
        editForm.value = {
          email: result.user.email || '',
          first_name: result.user.first_name || '',
          last_name: result.user.last_name || '',
          phone: result.user.phone || ''
        }
      } else {
        error.value = result.error || 'Failed to load profile'
      }
      loading.value = false
    }
    
    /**
     * Toggle edit mode
     */
    const toggleEditMode = () => {
      if (editMode.value) {
        // Cancel edit - reset form
        cancelEdit()
      } else {
        // Enter edit mode - populate form with current data
        editForm.value = {
          email: user.value.email || '',
          first_name: user.value.first_name || '',
          last_name: user.value.last_name || '',
          phone: user.value.phone || ''
        }
        editMode.value = true
        error.value = null
        successMessage.value = null
      }
    }
    
    /**
     * Cancel edit mode
     */
    const cancelEdit = () => {
      editMode.value = false
      editForm.value = {
        email: user.value.email || '',
        first_name: user.value.first_name || '',
        last_name: user.value.last_name || '',
        phone: user.value.phone || ''
      }
      error.value = null
      successMessage.value = null
    }
    
    /**
     * Update user profile
     */
    const updateProfile = async () => {
      saving.value = true
      error.value = null
      successMessage.value = null
      
      try {
        const result = await store.dispatch('auth/updateProfile', editForm.value)
        
        if (result.success) {
          successMessage.value = 'Profile updated successfully!'
          editMode.value = false
          // Clear success message after 3 seconds
          setTimeout(() => {
            successMessage.value = null
          }, 3000)
        } else {
          error.value = result.error || 'Failed to update profile'
        }
      } catch (err) {
        error.value = 'An error occurred while updating your profile'
        console.error('Profile update error:', err)
      } finally {
        saving.value = false
      }
    }
    
    // Load profile data on component mount
    onMounted(() => {
      if (!user.value) {
        fetchProfile()
      } else {
        // Initialize edit form with existing user data
        editForm.value = {
          email: user.value.email || '',
          first_name: user.value.first_name || '',
          last_name: user.value.last_name || '',
          phone: user.value.phone || ''
        }
        loading.value = false
      }
    })
    
    return {
      user,
      loading,
      editMode,
      saving,
      error,
      successMessage,
      editForm,
      userInitials,
      fullName,
      roleDisplay,
      toggleEditMode,
      cancelEdit,
      updateProfile
    }
  }
}
</script>

<style scoped>
.profile-content {
  max-width: 900px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.profile-info h2 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.75rem;
}

.profile-role {
  margin: 0 0 0.25rem 0;
  color: #7f8c8d;
  font-size: 1rem;
  font-weight: 600;
}

.profile-email {
  margin: 0;
  color: #95a5a6;
  font-size: 0.95rem;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
}

.profile-details {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.detail-section {
  margin-bottom: 2rem;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #eee;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.detail-item label {
  display: block;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-item p {
  margin: 0;
  color: #2c3e50;
  font-size: 1rem;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.9rem;
}

.role-badge.manager {
  background: #e3f2fd;
  color: #1976d2;
}

.role-badge.agent {
  background: #f3e5f5;
  color: #7b1fa2;
}

.profile-edit {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.profile-form {
  max-width: 700px;
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h3 {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #eee;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-control:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.7;
}

.form-help {
  display: block;
  margin-top: 0.25rem;
  color: #7f8c8d;
  font-size: 0.85rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.form-actions .btn {
  min-width: 120px;
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .detail-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}
</style>


