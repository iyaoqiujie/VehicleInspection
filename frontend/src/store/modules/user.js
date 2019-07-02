import { login, getInfo } from '@/api/user'
import router, { resetRouter } from '@/router'
import { getVuexFromStorage } from '@/utils'

/**
 * Fetch userinfo from Storage
 *
 */
const vuexJ = getVuexFromStorage()
let userInfo = {}
if (vuexJ.user) {
  userInfo = vuexJ.user
}
const state = {
  token: userInfo.token || '',
  id: userInfo.id || '',
  username: userInfo.username || '',
  mobile: userInfo.mobile || '',
  avatar: userInfo.avatar || '',
  usertype: userInfo.usertype || '',
  is_certificated: userInfo.is_certificated || false,
  roles: userInfo.roles || []
}

const mutations = {
  SET_USERINFO: (state, info) => {
    state.token = info.token
    state.id = info.id
    state.username = info.username
    state.mobile = info.mobile
    state.usertype = info.usertype
    state.is_certificated = info.is_certificated
    state.avatar = info.avatar
    state.roles = []
  },
  CLEAR_USERINFO: (state) => {
    state.token = ''
    state.id = ''
    state.username = ''
    state.mobile = ''
    state.usertype = ''
    state.is_certificated = ''
    state.avatar = ''
    state.roles = []
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        commit('SET_USERINFO', response)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          reject('Verification failed, please Login again.')
        }

        const { roles, name, avatar, introduction } = data

        // roles must be a non-empty array
        if (!roles || roles.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }

        commit('SET_ROLES', roles)
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        commit('SET_INTRODUCTION', introduction)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // User logout
  logout({ commit }) {
    return new Promise((resolve) => {
      commit('CLEAR_USERINFO')
      resetRouter()
      resolve()
    })
  },
  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('CLEAR_USERINFO')
      resolve()
    })
  },
  // Set role
  setRole({ commit }, roles) {
    return new Promise(resolve => {
      commit('SET_ROLES', roles)
      resetRouter()
      resolve()
    })
  },
  // Refresh routes
  refreshRoutes({ commit, dispatch }, role) {
    return new Promise(async resolve => {
      const roles = ['admin', role]
      commit('SET_ROLES', roles)
      resetRouter()

      // generate accessible routes map based on roles
      const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })

      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      resolve()
    })
  },
  // dynamically modify permissions
  changeRoles({ commit, dispatch }, role) {
    return new Promise(async resolve => {
      const token = role + '-token'

      commit('SET_TOKEN', token)

      const { roles } = await dispatch('getInfo')

      resetRouter()

      // generate accessible routes map based on roles
      const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })

      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
