import Vue from 'vue';
import VueRouter from 'vue-router';
import First from '../components/First.vue';
import Books from '../components/Books.vue';
import Authors from '../components/Authors.vue';
import Publishers from '../components/Publishers.vue';
import Genres from '../components/Genres.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'First',
    component: First,
  },
  {
    path: '/books',
    name: 'Books',
    component: Books,
  },
  {
    path: '/authors',
    name: 'Authors',
    component: Authors,
  },
  {
    path: '/publishers',
    name: 'Publishers',
    component: Publishers,
  },
  {
    path: '/genres',
    name: 'Genres',
    component: Genres,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
