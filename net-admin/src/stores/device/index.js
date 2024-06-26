import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import {
  getDeiveApi,
  createDeiveApi,
  getInterfaceApi,
  getInterfaceDetailApi,
  getSystemApi,
  getSystemDetailApi,
  getSerialApi,
  getSerialDetailApi,
  getIplApi,
  getIpDetailApi,
  getCompanyApi,
  getSnmpApi,
  createSnmpApi,
  createDeviceApi,
  createCompanyApi,
  updateDeiveApi,
  updateSnmpApi,
  updateCompanyApi,
  deleteDeiveApi,
  deleteSnmpApi,
  deleteCompanyApi,
  getArpApi,
  getArpDetailApi,
  searchArpApi,
  searchInterfaceApi,
  searchIpApi,
  searchSerialApi,
  searchSystemApi,
} from '@/api/device/index.js'


export const useDeviceStore = defineStore('device', () => {
  const device_info = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_snmp = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_interface = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_ip = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_system = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_serial = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_company = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })
  const device_arp = ref({
    total: 0,
    data: [],
    page: 1,
    page_size: 20
  })


  // 查询
  const getDeviceInfo = async () => {
    return await getDeiveApi({ page: device_info.value.page, page_size: device_info.value.page_size }).then(res => {
      device_info.value.total = res.total
      device_info.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getSnmp = async () => {
    return await getSnmpApi({ page: device_snmp.value.page, page_size: device_snmp.value.page_size }).then(res => {
      device_snmp.value.total = res.total
      device_snmp.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getInterface = async () => {
    return await getInterfaceApi({ page: device_interface.value.page, page_size: device_interface.value.page_size }).then(res => {
      device_interface.value.total = res.total
      device_interface.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getIp = async () => {
    return await getIplApi({ page: device_ip.value.page, page_size: device_ip.value.page_size }).then(res => {
      device_ip.value.total = res.total
      device_ip.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getSystem = async () => {
    return await getSystemApi({ page: device_system.value.page, page_size: device_system.value.page_size }).then(res => {
      device_system.value.total = res.total
      device_system.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getSerial = async () => {
    return await getSerialApi({ page: device_serial.value.page, page_size: device_serial.value.page_size }).then(res => {
      device_serial.value.total = res.total
      device_serial.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getCompany = async () => {
    return await getCompanyApi({ page: device_company.value.page, page_size: device_company.value.page_size }).then(res => {
      device_company.value.total = res.total
      device_company.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getArp = async () => {
    return await getArpApi({ page: device_arp.value.page, page_size: device_arp.value.page_size }).then(res => {
      device_arp.value.total = res.total
      device_arp.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  // 详情
  const getInterfaceDetail = async (id) => {
    return await getInterfaceDetailApi(id).then(res => {
      device_interface.value.total = res.total
      device_interface.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getIpDetail = async (id) => {
    return await getIpDetailApi(id).then(res => {
      device_ip.value.total = res.total
      device_ip.value.data = res.data
      return true
    })
  }

  const getSystemDetail = async (id) => {
    return await getSystemDetailApi(id).then(res => {
      device_system.value.total = res.total
      device_system.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getSerialDetail = async (id) => {
    return await getSerialDetailApi(id).then(res => {
      device_serial.value.total = res.total
      device_serial.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const getArpDetail = async (id) => {
    return await getArpDetailApi(id).then(res => {
      device_arp.value.total = res.total
      device_arp.value.data = data
      return true
    }).catch(err => {
      return false
    })
  }

  // 模糊查询

  const searchInterface = async (params) => {
    return await searchInterfaceApi(params).then(res => {
      device_interface.value.total = res.total
      device_interface.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }
  const searchIp = async (params) => {
    return await searchIpApi(params).then(res => {
      device_ip.value.total = res.total
      device_ip.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }
  const searchSystem = async (params) => {
    return await searchSystemApi(params).then(res => {
      device_system.value.total = res.total
      device_system.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  const searchSerial = async (params) => {
    return await searchSerialApi(params).then(res => {
      device_serial.value.total = res.total
      device_serial.value.data = res.data
      return true
    })
  }

  const searchArp = async (params) => {
    return await searchArpApi(params).then(res => {
      device_arp.value.total = res.total
      device_arp.value.data = res.data
      return true
    }).catch(err => {
      return false
    })
  }

  // 新增
  const addSnmp = async (data) => createSnmpApi(data)
  const addDevice = async (data) => createDeiveApi(data)
  const addCompany = async (data) => createCompanyApi(data)

  // 修改
  const updateSnmp = async (id, data) => updateSnmpApi(id, data)
  const updateDevice = async (id, data) => updateDeiveApi(id, data)
  const updateCompany = async (id, data) => updateCompanyApi(id, data)

  // 删除
  const deleteSnmp = async (id) => deleteSnmpApi(id)
  const deleteDevice = async (data) => deleteDeiveApi({ device_ids: data })
  const deleteCompany = async (id) => deleteCompanyApi(id)

  const refreshAll = () => {
    getDeviceInfo()
    getInterface()
    getIp()
    getSystem()
    getSerial()
    getArp()
  }

  return {
    device_info, device_snmp, device_interface, device_ip, device_system, device_serial, device_company, device_arp,
    getDeviceInfo, getSnmp, getInterface, getIp, getSystem, getSerial, getCompany, getArp,
    addSnmp, addDevice,addCompany,
    updateSnmp, updateDevice,updateCompany,
    deleteSnmp, deleteDevice,deleteCompany,
    getArpDetail, getInterfaceDetail, getIpDetail, getSystemDetail, getSerialDetail,
    searchInterface, searchIp, searchSystem, searchSerial, searchArp,
    refreshAll
  }
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
        paths: ['device_info', 'device_snmp', 'device_interface',
          'device_ip', 'device_system', 'device_serial',
          'device_company', 'device_arp'
        ]
      }
    ],
  })
