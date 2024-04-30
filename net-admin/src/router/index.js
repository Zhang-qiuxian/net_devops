import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Layout from '@/layout/main.vue'
import NotFound from '@/views/NotFound.vue'

const deviceRouters = [
  {
    path: '/device',
    meta: {
      title: '设备管理',
      icon: 'Platform'
    },
    redirect: Layout,
    children: [
      {
        path: 'device-preview',
        name: 'devicePreview',
        component: () => import('@/views/device/preview.vue'),
        meta: {
          title: '设备预览',
        },
      },
      {
        path: 'device-info',
        name: 'deviceInfo',
        component: () => import('@/views/device/info.vue'),
        meta: {
          title: '设备信息',
          // icon: 'Platform'
        },
      },

    ]
  }
]
const cronRouters = [
  {
    path: '/cron',
    meta: {
      title: '定时任务',
      icon: 'AlarmClock'
    },
    redirect: Layout,
    children: [
      {
        path: 'cron-info',
        name: 'cronInfo',
        component: () => import('@/views/cron/info.vue'),
        meta: {
          title: '任务管理',
          // icon: 'Platform'
        },
      },
    ]
  }
]
const routes = [
  {
    path: '/',
    name: 'home',
    component: Layout,
    children: [...deviceRouters, ...cronRouters]
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
  history: createWebHistory(),
  routes
})

export default router
