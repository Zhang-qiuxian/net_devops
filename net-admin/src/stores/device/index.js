import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import { getAllDeiveApi } from '@/api/device'


export const useDeviceStore = defineStore('device', () => {
  const device_info = ref({
    total: 0,
    data: []
  })
  const device_snmp = ref({
    total: 0,
    data: []
  })
  const pages = ref({
    page: 1,
    page_size: 15
  })
  const changePage = (page) => {
    pages.value.page = page
  }
  const getDeviceInfo = () => {
    getAllDeiveApi(pages.value).then(res => {
      device_info.value = res
    })
  }

  return { device_info, device_snmp, pages, getDeviceInfo,changePage }
},
  {
    // persist: {
    //   // 在这里进行自定义配置
    //   // paths: ['save.me', 'saveMeToo'],
    //   key: setLocalStore('settings'),
    // },
    persist: [
      {
        key: setLocalStore('device'),
        paths: ['device_info', 'devcie_snmp', 'pages']
      }
    ],
  })
