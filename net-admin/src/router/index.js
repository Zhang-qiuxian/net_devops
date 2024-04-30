import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Layout from '@/layout/main.vue'
import NotFound from '@/views/NotFound.vue'

const deviceRouters = [
  {
    path: '/device',
    name: 'device',
    component: () => import('../views/device/index.vue'),
    children: []
  }
]
const routes = [
  {
    path: '/',
    name: 'home',
    component: Layout,
    children: [...deviceRouters]
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (About.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import('../views/AboutView.vue')
  // },
]


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
