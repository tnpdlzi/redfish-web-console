import axios from 'axios';

/* eslint-disable */
// eslint-disable-next-line
export default {
  namespaced: true,
  state: {
    dashboard: [],
  },
  getters: {
    dashboard(state) {
      return state.dashboard
    }
  },
  actions: {
    fetchDashboard({commit}) {

      return axios.get('/api/dashboard').then((res) => {   
          if (res.length == 0) {
            return; 
          }  
          commit('setDashboard', res);
        })
      }
  },
  mutations: {
    setDashboard: (state, data) => {
      state.dashboard = data
    }
  },

}


