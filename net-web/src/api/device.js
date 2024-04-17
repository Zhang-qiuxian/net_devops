import service from './service.js'


const getDeice = async (params) => {
    let data = await service.get("device/info/", params)
    console.log(data);
    return data
}

const getOneDevice = async (id) => {
    // let data = 
    return await service.get(`"device/info/${id}/"`)
}

const addDevice = async (params) => {
    // let data = 
    return await service.post("device/info/",params)
}

// function getDeice(params) {

// }

async function removeDevice(params) {
    return
}

export { getDeice }