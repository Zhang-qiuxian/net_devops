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
        },
      },
      {
        path: 'device-snmp',
        name: 'deviceSnmp',
        component: () => import('@/views/device/snmp.vue'),
        meta: {
          title: 'SNMP模板',
        },
      },
      {
        path: 'device-company',
        name: 'deviceCompany',
        component: () => import('@/views/device/company.vue'),
        meta: {
          title: '设备厂家',
        },
      },
      {
        path: 'device-interface',
        name: 'deviceInterface',
        component: () => import('@/views/device/interface.vue'),
        meta: {
          title: '接口管理',
        },
      },
      {
        path: 'device-ip',
        name: 'deviceIp',
        component: () => import('@/views/device/ip.vue'),
        meta: {
          title: '设备IP管理',
        },
      },
      {
        path: 'device-serial',
        name: 'deviceSerial',
        component: () => import('@/views/device/serial.vue'),
        meta: {
          title: '序列号管理',
        },
      },
      {
        path: 'device-system',
        name: 'deviceSystem',
        component: () => import('@/views/device/system.vue'),
        meta: {
          title: '系统信息',
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
