import Vue from 'vue'
import Vuex from 'vuex'

import dashboard from '@/store/modules/dashboard'
import tabs from '@/store/modules/tabs'

/* eslint-disable */
// eslint-disable-next-line
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    dashboard,
    tabs
  }
})
