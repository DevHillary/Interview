<template>
  <div class="main-content">
    <div class="container" style="max-width: 500px; margin-top: 4rem;">
      <h2 class="page-title" style="text-align: center; margin-bottom: 2rem;">Register</h2>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">Registration successful! Please login.</div>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label class="form-label">Username</label>
          <input
            v-model="userData.username"
            type="text"
            class="form-input"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Email</label>
          <input
            v-model="userData.email"
            type="email"
            class="form-input"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">First Name</label>
          <input
            v-model="userData.first_name"
            type="text"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Last Name</label>
          <input
            v-model="userData.last_name"
            type="text"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Role</label>
          <select v-model="userData.role" class="form-select" required>
            <option value="agent">Agent</option>
            <option value="manager">Manager</option>
          </select>
        </div>
        
        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="userData.password"
            type="password"
            class="form-input"
            required
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Confirm Password</label>
          <input
            v-model="userData.password2"
            type="password"
            class="form-input"
            required
          />
        </div>
        
        <button type="submit" class="btn btn-primary" style="width: 100%;" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      
      <p style="text-align: center; margin-top: 1rem;">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const userData = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      role: 'agent',
      password: '',
      password2: ''
    })
    
    const error = ref(null)
    const success = ref(false)
    const loading = computed(() => store.state.auth.loading)
    
    const handleRegister = async () => {
      error.value = null
      success.value = false
      
      if (userData.value.password !== userData.value.password2) {
        error.value = 'Passwords do not match'
        return
      }
      
      const result = await store.dispatch('auth/register', userData.value)
      
      if (result.success) {
        success.value = true
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } else {
        error.value = typeof result.error === 'string' 
          ? result.error 
          : JSON.stringify(result.error)
      }
    }
    
    return {
      userData,
      error,
      success,
      loading,
      handleRegister
    }
  }
}
</script>



