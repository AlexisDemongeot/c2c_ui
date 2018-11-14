// Require the main Sass manifest file
require('./assets/sass/main.scss')
require('@/js/polyfills.js')

import Vue from 'vue'
import App from '@/App.vue'

import router from '@/js/vue-plugins/router'
import documentUtils from '@/js/vue-plugins/document-utils'
import fontAwesome from '@/js/vue-plugins/font-awesome-config'
import helperWindow from '@/js/vue-plugins/helper-window'
import getText from '@/js/vue-plugins/gettext-plugin'
import globalComponents from '@/js/vue-plugins/generic-components'
import localStorage from '@/js/vue-plugins/local-storage'
import tooltip from '@/js/vue-plugins/tooltip'
import user from '@/js/vue-plugins/user'
import vueMoment from '@/js/vue-plugins/vue-moment.js'

Vue.config.productionTip = false
Vue.config.silent = false

Vue.use(localStorage)       // First, vm.$localStorage property
Vue.use(vueMoment)          // moment functions
Vue.use(documentUtils)      // getDocumentType, getLocale functions
Vue.use(fontAwesome)        // <fa-icon /> component
Vue.use(getText)            // vm.$gettext() function and v-translate directive
Vue.use(helperWindow)       // vm.$helper property
Vue.use(globalComponents)   // Components available everywhere
Vue.use(tooltip)            // v-tooltip directive
Vue.use(user)               // vm.$user property

new Vue({
    router:router,
    created(){
        this.$language.setCurrent(this.$user.lang)
    },
    render: h => h(App),
}).$mount('#app')
