import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'

import NotFound from '@/views/NotFound.vue'
import HomeView from '@/App.vue'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            redirect: { name: 'console-info' },
            children:[
                {
                    path: '/console',
                    children: [
                        { path: 'console-info', name: 'console-info', component: () => import('@/views/console/Info.vue') }
                    ],
                },
                {
                    path: '/device',
                    children: [
                        { path: 'device-info', name: 'device-info', component: () => import('@/views/device/Info.vue') }
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

export default router
