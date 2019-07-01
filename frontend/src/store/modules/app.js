import { getVuexFromStorage } from '../../utils'
const vuexJ = getVuexFromStorage()
let uiSize = 'medium'
let sbOpened = true
if (vuexJ.app) {
  uiSize = vuexJ.app.size
  if (vuexJ.app.sidebar) {
    sbOpened = vuexJ.app.sidebar.opened
  }
}
const state = {
  sidebar: {
    opened: sbOpened,
    withoutAnimation: false
  },
  device: 'desktop',
  size: uiSize || 'medium'
}

const mutations = {
  TOGGLE_SIDEBAR: state => {
    state.sidebar.opened = !state.sidebar.opened
    state.sidebar.withoutAnimation = false
  },
  CLOSE_SIDEBAR: (state, withoutAnimation) => {
    state.sidebar.opened = false
    state.sidebar.withoutAnimation = withoutAnimation
  },
  TOGGLE_DEVICE: (state, deviceType) => {
    state.device = deviceType
  },
  SET_SIZE: (state, fontSize) => {
    state.size = fontSize
  }
}

const actions = {
  toggleSideBar({ commit }) {
    commit('TOGGLE_SIDEBAR')
  },
  closeSideBar({ commit }, { withoutAnimation }) {
    commit('CLOSE_SIDEBAR', withoutAnimation)
  },
  toggleDevice({ commit }, deviceType) {
    commit('TOGGLE_DEVICE', deviceType)
  },
  setSize({ commit }, fontSize) {
    commit('SET_SIZE', fontSize)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
