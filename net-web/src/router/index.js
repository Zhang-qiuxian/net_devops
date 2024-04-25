import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'

import NotFound from '@/views/NotFound.vue'
import HomeView from '@/views/Base.vue'


const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            children: [
                {
                    path: '/console',
                    children: [
                        { path: 'console-info', name: 'console-info', component: () => import('@/views/console/Info.vue') }
                    ],
                },
                {
                    path: '/device',
                    children: [
                        {
                            path: 'info', name: 'device-info', component: () => import('@/views/device/Info.vue'),
                        },
                        {
                            path: 'snmp', name: 'device-snmp', component: () => import('@/views/device/Snmp.vue'),
                        },
                        {
                            path: 'company', name: 'device-company', component: () => import('@/views/device/Company.vue'),
                        },
                        {
                            path: 'preview', name: 'device-preview', component: () => import('@/views/device/Preview.vue'),
                        }
                    ],
                },
                {
                    path: '/cron',
                    children: [
                        { path: 'cron-info', name: 'cron-info', component: () => import('@/views/cron/Info.vue') }
                    ],
                },
                {
                    path: '/ipam',
                    children: [
                        { path: 'ipam-info', name: 'ipam-info', component: () => import('@/views/ipam/Info.vue') }
                    ],
                },
            ]
        },

        { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
    ]
})

// 打印所有路由
// function printAllRoutes(router) {
//     const routesToPrint = router.getRoutes();
//     console.log('所有路由:', routesToPrint);
// }

// // 调用函数打印所有路由
// printAllRoutes(router);
export default router
