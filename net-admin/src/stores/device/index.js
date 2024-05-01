import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import { getAllDeiveApi } from '@/api/device'


export const useDeviceStore = defineStore('device', () => {
  const devcie_info = ref({
    total: 0,
    data:[]
  })
  const devcie_snmp = ref([])
  const page = ref({
    page: 1,
    page_size: 10
  })

  const getDeviceInfo = (params) => {
    getAllDeiveApi(params).then(res => {
      devcie_info.value = res
    })
    console.log(devcie_info);
  }

  return { devcie_info, devcie_snmp, page, getDeviceInfo }
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
        paths: ['devcie_info', 'devcie_snmp', 'page']
      }
    ],
  })