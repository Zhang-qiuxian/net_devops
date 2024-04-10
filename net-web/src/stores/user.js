// stores/authStore.js  
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {lsManager} from '@/utlis/local'

export const useUseStore = defineStore('user', () => {
    const token = ref(null)


    // 使用getter来获取token，优先从localStorage中获取  
    function getToken() {
         const storedToken = lsManager.getItem('token')
         return storedToken || token.value
    }

    function setToken(token) {
        // 设置token到state和localStorage  
        token.value = token
        lsManager.setItem('token',token)
    }
    function removeToken() {
        // 清除token从state和localStorage  
        token.value = null
        lsManager.removeItem('token')
    }
})