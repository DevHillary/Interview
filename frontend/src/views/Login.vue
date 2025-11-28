<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Left side - Branding -->
      <div class="login-brand">
        <div class="brand-content">
          <div class="logo">
            <div class="logo-icon">🇰🇪</div>
            <h1>CRM Kenya</h1>
          </div>
          <p class="tagline">Manage your business relationships efficiently</p>
          <div class="features">
            <div class="feature">
              <span class="feature-icon">✓</span>
              <span>Lead Management</span>
            </div>
            <div class="feature">
              <span class="feature-icon">✓</span>
              <span>Contact Tracking</span>
            </div>
            <div class="feature">
              <span class="feature-icon">✓</span>
              <span>Smart Reminders</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right side - Login Form -->
      <div class="login-form-section">
        <div class="login-form-container">
          <h2 class="form-title">Welcome Back</h2>
          <p class="form-subtitle">Sign in to your account to continue</p>
          
          <!-- Error message display -->
          <div v-if="error" class="error-message">
            <span class="error-icon">⚠</span>
            {{ error }}
          </div>
          
          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label class="form-label">Username</label>
              <div class="input-wrapper">
                <span class="input-icon">👤</span>
                <input
                  v-model="credentials.username"
                  type="text"
                  class="form-input"
                  placeholder="Enter your username"
                  required
                  autocomplete="username"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">Password</label>
              <div class="input-wrapper">
                <span class="input-icon">🔒</span>
                <input
                  v-model="credentials.password"
                  type="password"
                  class="form-input"
                  placeholder="Enter your password"
                  required
                  autocomplete="current-password"
                />
              </div>
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary btn-login" 
              :disabled="loading"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>Sign In</span>
            </button>
          </form>
          
          <div class="form-footer">
            <p>Don't have an account? 
              <router-link to="/register" class="link">Create one</router-link>
            </p>
          </div>
          
          <!-- Demo credentials -->
          <div class="demo-credentials">
            <p class="demo-title">Demo Accounts:</p>
            <div class="demo-account">
              <strong>Manager:</strong> manager / password123
            </div>
            <div class="demo-account">
              <strong>Agent:</strong> agent / password123
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    // Form data state
    const credentials = ref({
      username: '',
      password: ''
    })
    
    // Error state for displaying login failures
    const error = ref(null)
    
    // Loading state from Vuex store
    const loading = computed(() => store.state.auth.loading)
    
    /**
     * Handle login form submission
     * Dispatches login action to Vuex store and redirects on success
     */
    const handleLogin = async () => {
      error.value = null
      const result = await store.dispatch('auth/login', credentials.value)
      
      if (result.success) {
        // Redirect to dashboard after successful login
        router.push('/dashboard')
      } else {
        error.value = result.error
      }
    }
    
    return {
      credentials,
      error,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 2rem;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-brand {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-content {
  max-width: 350px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.logo-icon {
  font-size: 3rem;
}

.logo h1 {
  font-size: 2rem;
  margin: 0;
  font-weight: 700;
}

.tagline {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
}

.feature-icon {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.login-form-section {
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
}

.form-title {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-weight: 700;
}

.form-subtitle {
  color: #7f8c8d;
  margin: 0 0 2rem 0;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.error-icon {
  font-size: 1.25rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 1.25rem;
  opacity: 0.6;
  pointer-events: none;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn-login {
  width: 100%;
  padding: 1rem;
  font-size: 1.05rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.form-footer p {
  color: #7f8c8d;
  margin: 0;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.demo-credentials {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  font-size: 0.85rem;
}

.demo-title {
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.demo-account {
  color: #7f8c8d;
  margin: 0.25rem 0;
  font-family: 'Courier New', monospace;
}

@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  
  .login-brand {
    display: none;
  }
  
  .login-form-section {
    padding: 2rem 1.5rem;
  }
}
</style>


