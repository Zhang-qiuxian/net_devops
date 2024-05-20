import instance from "../service";

const infoApi = "device/info/"
const interfaceApi = "device/interface/"
const ipApi = "device/ip/"
const systemApi = "device/system/"
const serialApi = "device/serial/"
const companyApi = "device/company/"
const snmpApi = "device/snmp/"
const arpApi = "device/arp/"

// 查询列表
export const getDeiveApi = async (params) => {
    return instance.get(infoApi, { params })
}

export const getInterfaceApi = async (params) => {
    return instance.get(interfaceApi, { params })
}

export const getSystemApi = async (params) => {
    return instance.get(systemApi, { params })
}

export const getSerialApi = async (params) => {
    return instance.get(serialApi, { params })
}

export const getIplApi = async (params) => {
    return instance.get(ipApi, { params })
}

export const getCompanyApi = async (params) => {
    return instance.get(companyApi, { params })
}

export const getSnmpApi = async (params) => {
    return instance.get(snmpApi, { params })
}

export const getArpApi = async (params) => {
    return instance.get(arpApi, { params })
}

// 查询单个
export const getDeiveDetailApi = async (id) => {
    return instance.get(`${infoApi}${id}/`)
}

export const getInterfaceDetailApi = async (id) => {
    return instance.get(`${interfaceApi}${id}/`)
}

export const getSystemDetailApi = async (id) => {
    return instance.get(`${systemApi}${id}/`)
}

export const getSerialDetailApi = async (id) => {
    return instance.get(`${serialApi}${id}/`)
}

export const getIpDetailApi = async (id) => {
    return instance.get(`${ipApi}${id}/`)
}

export const getCompanyDetailApi = async (id) => {
    return instance.get(`${companyApi}${id}/`)
}

export const getSnmpDetailApi = async (id) => {
    return instance.get(`${snmpApi}${id}/`)
}

export const getArpDetailApi = async (id) => {
    return instance.get(`${arpApi}${id}/`)
}

// 模糊查询
export const searchDeviceApi = async (params) => {
    return instance.get(infoApi, { params })
}

export const searchInterfaceApi = async (params) => {
    return instance.get(interfaceApi, { params })
}

export const searchSystemApi = async (params) => {
    return instance.get(systemApi, { params })
}

export const searchSerialApi = async (params) => {
    return instance.get(serialApi, { params })
}

export const searchIpApi = async (params) => {
    return instance.get(ipApi, { params })
}


export const searchArpApi = async (params) => {
    return instance.get(arpApi, { params })
}


// 新增
export const createDeiveApi = async (data) => {
    return instance.post(infoApi, data)
}

export const createSnmpApi = async (data) => {
    return instance.post(snmpApi, data)
}

export const createCompanyApi = async (data) => {
    return instance.post(companyApi, data)
}

export const createDeviceApi = async (data) => {
    return instance.post(infoApi, data)
}
// 修改
export const updateDeiveApi = async (id, data) => {
    return instance.put(`${infoApi}${id}/`, data)
}

export const updateSnmpApi = async (id, data) => {
    return instance.put(`${snmpApi}${id}/`, data)
}

export const updateCompanyApi = async (id, data) => {
    return instance.put(`${companyApi}${id}/`, data)
}

// 删除
export const deleteDeiveApi = async (data) => {
    return instance.post(`${infoApi}delete/`, data)
}

export const deleteSnmpApi = async (id) => {
    return instance.delete(`${snmpApi}${id}/`)
}

export const deleteCompanyApi = async (id) => {
    return instance.delete(`${companyApi}${id}/`)
}

// 刷新arp
export const refreshArpApi = async () => {
    return instance.post(`${arpApi}refresh/`)
}
