import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import { getDeice } from '@/api/device.js'


export const useDeviceStore = defineStore('net_device', () => {
    const total = ref(0)
    const device = ref([])
    // const doubleCount = computed(() => count.value * 2)
    async function get(params) {
        let data = await getDeice({
            params: params
        })
        device.value = data.data
        console.log(data);
        total.value = data.total
        return data
    }
    return { total, device, get }
},
    {
        //持久化存储到 localStorage 中
        persist: true
    })
