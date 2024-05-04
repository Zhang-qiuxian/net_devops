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

} from '@/api/device/index.js'


export const useDeviceStore = defineStore('device', () => {
  const device_info = ref({
    total: 0,
    data: []
  })
  const device_snmp = ref({
    total: 0,
    data: []
  })
  const device_interface = ref({
    total: 0,
    data: []
  })
  const device_ip = ref({
    total: 0,
    data: []
  })
  const device_system = ref({
    total: 0,
    data: []
  })
  const device_serial = ref({
    total: 0,
    data: []
  })
  const device_company = ref({
    total: 0,
    data: []
  })

  const pages = ref({
    page: 1,
    page_size: 15
  })

  // const changePage = (page) => { pages.value.page = page }
  // 查询
  const getDeviceInfo = () => { getAllDeiveApi(pages.value).then(res => { device_info.value = res }) }
  const getSnmp = () => { getAllSnmpApi(pages.value).then(res => { device_snmp.value = res }) }
  const getInterface = () => { getAllInterfaceApi(pages.value).then(res => { device_interface.value = res }) }
  const getIp = () => { getAllIplApi(pages.value).then(res => { device_ip.value = res }) }
  const getSystem = () => { getAllSystemApi(pages.value).then(res => { device_system.value = res }) }
  const getSerial = () => { getAllSerialApi(pages.value).then(res => { device_serial.value = res }) }
  const getCompany = () => { getAllCompanyApi(pages.value).then(res => { device_company.value = res }) }

  // 新增
  const addSnmp = (data) => { createOneSnmpApi(data).then(res => res) }

  return {
    pages,
    device_info, device_snmp, device_interface, device_ip, device_system, device_serial, device_company,
    getDeviceInfo, getSnmp, getInterface, getIp, getSystem, getSerial, getCompany,
    addSnmp,
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
