import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import {
  getAllDeiveApi,
  getOneDeiveApi,
  createOneDeiveApi,
  getAllInterfaceApi,
  getOneInterfaceApi,
  getAllSystemApi,
  getOneSystemApi,
  getAllSerialApi,
  getOneSerialApi,
  getAllIplApi,
  getOneIpApi,
  getAllCompanyApi,
  getOneCompanyApi,
  createOneCompanyApi,
  getAllSnmpApi,
  getOneSnmpApi,
  createOneSnmpApi,
  createOneDeviceApi,
  updateOneDeiveApi,
  updateOneSnmpApi,
  deleteOneDeiveApi,
  deleteOneSnmpApi,

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

  const pages = ref({
    page: 1,
    page_size: 20,
    page: 1,
    page_size: 20
  })

  // const changePage = (page) => { { page: device_info.value.page, page_size: device_info.value.page_size }.page = page }
  // 查询
  const getDeviceInfo = () => {
    getAllDeiveApi({ page: device_info.value.page, page_size: device_info.value.page_size }).then(res => {
      device_info.value.total = res.total
      device_info.value.data = res.data
    })
  }
  const getSnmp = () => {
    getAllSnmpApi({ page: device_snmp.value.page, page_size: device_snmp.value.page_size }).then(res => {
      device_snmp.value.total = res.total
      device_snmp.value.data = res.data
    })
  }
  const getInterface = () => {
    getAllInterfaceApi({ page: device_interface.value.page, page_size: device_interface.value.page_size }).then(res => {
      device_interface.value.total = res.total
      device_interface.value.data = res.data
    })
  }
  const getIp = () => {
    getAllIplApi({ page: device_ip.value.page, page_size: device_ip.value.page_size }).then(res => {
      device_ip.value.total = res.total
      device_ip.value.data = res.data
    })
  }
  const getSystem = () => {
    getAllSystemApi({ page: device_system.value.page, page_size: device_system.value.page_size }).then(res => {
      device_system.value.total = res.total
      device_system.value.data = res.data
    })
  }
  const getSerial = () => {
    getAllSerialApi({ page: device_serial.value.page, page_size: device_serial.value.page_size }).then(res => {
      device_serial.value.total = res.total
      device_serial.value.data = res.data
    })
  }
  const getCompany = () => {
    getAllCompanyApi({ page: device_company.value.page, page_size: device_company.value.page_size }).then(res => {
      device_company.value.total = res.total
      device_company.value.data = res.data
    })
  }

  // 新增
  const addSnmp = async (data) => createOneSnmpApi(data)
  const addDevice = async (data) => createOneDeiveApi(data)

  // 修改
  const updateSnmp = async (id, data) => updateOneSnmpApi(id, data)
  const updateDevice = async (id, data) => updateOneDeiveApi(id, data)

  // 删除
  const deleteSnmp = async (id) => deleteOneSnmpApi(id)
  const deleteDevice = async (id) => deleteOneDeiveApi(id)
  return {
    pages,
    device_info, device_snmp, device_interface, device_ip, device_system, device_serial, device_company,
    getDeviceInfo, getSnmp, getInterface, getIp, getSystem, getSerial, getCompany,
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
        paths: ['device_info', 'device_snmp', 'device_interface', 'device_ip', 'device_system', 'device_serial', 'device_company', 'pages']
      }
    ],
  })
