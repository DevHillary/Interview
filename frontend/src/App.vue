<template>
  <div id="app">
    <nav v-if="isAuthenticated" class="navbar">
      <div class="nav-container">
        <h1 class="nav-title">🇰🇪 CRM Kenya</h1>
        <div class="nav-links">
          <router-link to="/dashboard">Dashboard</router-link>
          <router-link to="/leads">Leads</router-link>
          <router-link to="/contacts">Contacts</router-link>
          <router-link to="/reminders">Reminders</router-link>
          <router-link to="/profile" class="profile-link">Profile</router-link>
          <span class="user-info">{{ currentUser?.username }} ({{ currentUser?.role }})</span>
          <button @click="logout" class="btn btn-secondary">Logout</button>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view/>
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const currentUser = computed(() => store.state.auth.user)

    const logout = () => {
      store.dispatch('auth/logout')
      router.push('/login')
    }

    return {
      isAuthenticated,
      currentUser,
      logout
    }
  }
}
</script>


