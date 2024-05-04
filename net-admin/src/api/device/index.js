import instance from "../service";

const infoApi = "device/info/"
const interfaceApi = "device/interface/"
const ipApi = "device/ip/"
const systemApi = "device/system/"
const serialApi = "device/serial/"
const companyApi = "device/company/"
const snmpApi = "device/snmp/"

export const getAllDeiveApi = async (params) => {
    return await instance.get(infoApi, { params })
}

export const getOneDeiveApi = async (id) => {
    return await instance.get(`"${infoApi}${id}/"`)
}

export const createOneDeiveApi = async (data) => {
    return await instance.post(infoApi, { data })
}

// export const exportDeiveApi = async () => {
//     return await instance.get(`${infoApi}export_excel/`,
//         // {responseType: 'blob'}
//     )
// }

export const getAllInterfaceApi = async (params) => {
    return await instance.get(interfaceApi, { params })
}

export const getOneInterfaceApi = async (id) => {
    return await instance.get(`"${interfaceApi}${id}/"`)
}

export const getAllSystemApi = async (params) => {
    return await instance.get(systemApi, { params })
}

export const getOneSystemApi = async (id) => {
    return await instance.get(`"${systemApi}${id}/"`)
}

export const getAllSerialApi = async (params) => {
    return await instance.get(serialApi, { params })
}

export const getOneSerialApi = async (id) => {
    return await instance.get(`"${serialApi}${id}/"`)
}

export const getAllIplApi = async (params) => {
    return await instance.get(ipApi, { params })
}

export const getOneIpApi = async (id) => {
    return await instance.get(`"${ipApi}${id}/"`)
}

export const getAllCompanyApi = async (params) => {
    return await instance.get(companyApi, { params })
}

export const getOneCompanyApi = async (id) => {
    return await instance.get(`"${companyApi}${id}/"`)
}
export const createOneCompanyApi = async (data) => {
    return await instance.post(companyApi, { data })
}

export const getAllSnmpApi = async (params) => {
    return await instance.get(snmpApi, { params })
}

export const getOneSnmpApi = async (id) => {
    return await instance.get(`"${snmpApi}${id}/"`)
}

export const createOneSnmpApi = async (data) => {
    return await instance.post(snmpApi, { data })
}
