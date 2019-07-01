import Vue from 'vue'

import 'normalize.css/normalize.css' // a modern alternative to CSS resets

import Element from 'element-ui'
import './styles/element-variables.scss'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import './icons' // icon
import './permission' // permission control
import './utils/error-log' // error log
import { getVuexFromStorage } from './utils'

import * as filters from './filters' // global filters

let uiSize = 'medium'
const vuexJ = getVuexFromStorage()
if (vuexJ.app && vuexJ.app.size) {
  uiSize = vuexJ.app.size
}
Vue.use(Element, {
  size: uiSize
})

// register global utility filters
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
