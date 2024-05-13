import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import {
  getDeiveApi,
  getDeiveDetailApi,
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
  getCompanyDetailApi,
  createCompanyApi,
  getSnmpApi,
  getSnmpDetailApi,
  createSnmpApi,
  createDeviceApi,
  updateDeiveApi,
  updateSnmpApi,
  deleteDeiveApi,
  deleteSnmpApi,
  getArpApi,
  getArpDetailApi,

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


  // const changePage = (page) => { { page: device_info.value.page, page_size: device_info.value.page_size }.page = page }
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

  // 新增
  const addSnmp = async (data) => createSnmpApi(data)
  const addDevice = async (data) => createDeiveApi(data)

  // 修改
  const updateSnmp = async (id, data) => updateSnmpApi(id, data)
  const updateDevice = async (id, data) => updateDeiveApi(id, data)

  // 删除
  const deleteSnmp = async (id) => deleteSnmpApi(id)
  const deleteDevice = async (data) => deleteDeiveApi({device_ids:data})

  return {
    device_info, device_snmp, device_interface, device_ip, device_system, device_serial, device_company, device_arp,
    getDeviceInfo, getSnmp, getInterface, getIp, getSystem, getSerial, getCompany, getArp,
    addSnmp, addDevice,
    updateSnmp, updateDevice,
    deleteSnmp, deleteDevice
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
