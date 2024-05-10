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
export const getAllDeiveApi = async (params) => {
    return await instance.get(infoApi, { params })
}

export const getAllInterfaceApi = async (params) => {
    return await instance.get(interfaceApi, { params })
}

export const getAllSystemApi = async (params) => {
    return await instance.get(systemApi, { params })
}

export const getAllSerialApi = async (params) => {
    return await instance.get(serialApi, { params })
}

export const getAllIplApi = async (params) => {
    return await instance.get(ipApi, { params })
}

export const getAllCompanyApi = async (params) => {
    return await instance.get(companyApi, { params })
}

export const getAllSnmpApi = async (params) => {
    return await instance.get(snmpApi, { params })
}

export const getAllArpApi = async (params) => {
    return await instance.get(arpApi, { params })
}

// 查询单个
export const getOneDeiveApi = async (id) => {
    return await instance.get(`${infoApi}${id}/`)
}

export const getOneInterfaceApi = async (id) => {
    return await instance.get(`${interfaceApi}${id}/`)
}

export const getOneSystemApi = async (id) => {
    return await instance.get(`${systemApi}${id}/`)
}

export const getOneSerialApi = async (id) => {
    return await instance.get(`${serialApi}${id}/`)
}

export const getOneIpApi = async (id) => {
    return await instance.get(`${ipApi}${id}/`)
}

export const getOneCompanyApi = async (id) => {
    return await instance.get(`${companyApi}${id}/`)
}

export const getOneSnmpApi = async (id) => {
    return await instance.get(`${snmpApi}${id}/`)
}

export const getOneArpApi = async (id) => {
    return await instance.get(`${arpApi}${id}/`)
}

// 新增
export const createOneDeiveApi = async (data) => {
    return await instance.post(infoApi, data )
}

export const createOneSnmpApi = async (data) => {
    return await instance.post(snmpApi, data )
}

export const createOneCompanyApi = async (data) => {
    return await instance.post(companyApi,  data )
}

export const createOneDeviceApi = async (data) => {
    return await instance.post(infoApi, data )
}
// 修改
export const updateOneDeiveApi = async (id, data) => {
    return await instance.put(`${infoApi}${id}/`, data )
}

export const updateOneSnmpApi = async (id, data) => {
    return await instance.put(`${snmpApi}${id}/`, data )
}

// 删除
export const deleteOneDeiveApi = async (id) => {
    return await instance.delete(`${infoApi}${id}/`)
}

export const deleteOneSnmpApi = async (id) => {
    return await instance.delete(`${snmpApi}${id}/`)
}