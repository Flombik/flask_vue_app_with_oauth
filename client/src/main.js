import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap-social.css';
import '@fortawesome/free-brands-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faGithub } from '@fortawesome/free-brands-svg-icons/faGithub';
import { faYandexInternational } from '@fortawesome/free-brands-svg-icons/faYandexInternational';
import { faVk } from '@fortawesome/free-brands-svg-icons/faVk';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
library.add(faGithub);
library.add(faVk);
library.add(faYandexInternational);
Vue.component('font-awesome-icon', FontAwesomeIcon);

new Vue({
  router,
  render: (h) => (h(App)),
}).$mount('#app');
