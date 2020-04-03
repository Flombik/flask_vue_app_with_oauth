import "bootstrap/dist/css/bootstrap.css";
import BootstrapVue from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap-social.css";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faGithub, faYandexInternational, faVk } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Vue from "vue";
import Axios from "axios";
import App from "./App.vue";
import router from "./router";
import store from "./store";

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
library.add(faGithub, faVk, faYandexInternational);
Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.prototype.$http = Axios;
const token = localStorage.getItem("token");
if (token) {
  Vue.prototype.$http.defaults.headers.common.Authorization = token;
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
