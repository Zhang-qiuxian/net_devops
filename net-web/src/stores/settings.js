import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'






export const useSettingsStore = defineStore('net_settings', () => {
    const default_menu = ref(['home'])
    function updateMenu(key) {
        console.log(default_menu.value);
        if (default_menu.value = key) {
            return default_menu.value
        } else {
            return default_menu.value = [key]
        }

    }
    // const doubleCount = computed(() => count.value * 2)
    // const meun = computed(() => [default_menu.value])
    return { default_menu, updateMenu }
},
    {
        //持久化存储到 localStorage 中
        persist: true
    })
