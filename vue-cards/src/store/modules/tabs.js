/* eslint-disable */
// eslint-disable-next-line
export default {
  namespaced: true,
  state: {
    tabs: ['Dashboard', 'Server List', 'Details', 'Charts', 'bios', 'logs'],
  },
  getters: {
    getTabs(state) {
      return state.tabs
    }
  },

}


