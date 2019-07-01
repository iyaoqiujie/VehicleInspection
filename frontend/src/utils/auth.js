import { getVuexFromStorage } from './index'

export function getToken() {
  const vuexJ = getVuexFromStorage()
  if (vuexJ.user) {
    return vuexJ.user.token
  } else {
    return ''
  }
}
