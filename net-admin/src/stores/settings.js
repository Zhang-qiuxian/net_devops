import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useSettingsStore = defineStore('settings', () => {
  const routers = ref([])
  // const doubleCount = computed(() => count.value * 2)
  // function increment() {
  //   count.value++
  // }
  const allRouters = computed(() => routers.value)

  const addRouter = (routers) => {
    routers.value = routers.getRoutes().filter((item) => { if (item.children.length > 0) return item })
  }
  return { allRouters, addRouter }
})
