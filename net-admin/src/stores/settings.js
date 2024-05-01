import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import router from '@/router';

export const useSettingsStore = defineStore('settings', () => {
  const routers = ref([]) || addRouter()
  const default_active = ref('/')
  // const doubleCount = computed(() => count.value * 2)
  // function increment() {
  //   count.value++
  // }
  // const allRouters = computed(() => routers.value)
  // const acitve_menu = computed(() => default_active.value)

  const addRouter = () => {
    routers.value = router.getRoutes().filter((item) => { if (item.children.length > 0 && item.path != '/') return item })
  }
  const setDefaultActive = (path) => {
    default_active.value = path
  }
  return { routers, default_active,addRouter,setDefaultActive }
},
  {
    // persist: {
    //   // 在这里进行自定义配置
    //   // paths: ['save.me', 'saveMeToo'],
    //   key: setLocalStore('settings'),
    // },
    persist:[
      {
        key: setLocalStore('settings'),
        paths:['routers','default_active']
      }
    ],
  })
