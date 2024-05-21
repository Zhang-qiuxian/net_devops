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
        path: 'device-search',
        name: 'deviceSearch',
        component: () => import('@/views/device/search.vue'),
        meta: {
          title: 'ARP检索',
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
      {
        path: 'device-arp',
        name: 'deviceArp',
        component: () => import('@/views/device/arp.vue'),
        meta: {
          title: '设备arp管理',
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
      // {
      //   path: 'cron-periodic',
      //   name: 'cronPeriodic',
      //   component: () => import('@/views/cron/periodic.vue'),
      //   meta: {
      //     title: '任务管理',
      //   },
      // },
      // {
      //   path: 'cron-clocked',
      //   name: 'cronClocked',
      //   component: () => import('@/views/cron/clocked.vue'),
      //   meta: {
      //     title: '定时任务',
      //   },
      // },
      // {
      //   path: 'cron-interval',
      //   name: 'cronInterval',
      //   component: () => import('@/views/cron/interval.vue'),
      //   meta: {
      //     title: '周期任务',
      //   },
      // },
      // {
      //   path: 'cron-crontab',
      //   name: 'cronCrontab',
      //   component: () => import('@/views/cron/crontab.vue'),
      //   meta: {
      //     title: 'crontab计划任务',
      //   },
      // },
      {
        path: 'cron-logs',
        name: 'cronLogs',
        component: () => import('@/views/cron/logs.vue'),
        meta: {
          title: '后台任务日志',
        },
      },
      {
        path: 'cron-result',
        name: 'cronResult',
        component: () => import('@/views/cron/result.vue'),
        meta: {
          title: '任务执行结果',
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
  history: createWebHashHistory(),
  routes
})

export default router
