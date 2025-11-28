import { createStore } from 'vuex'
import auth from './modules/auth'
import leads from './modules/leads'
import contacts from './modules/contacts'
import reminders from './modules/reminders'

export default createStore({
  modules: {
    auth,
    leads,
    contacts,
    reminders
  }
})



