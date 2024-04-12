import service from './service.js'


const getDeice = async (params) => {
    let data = await service.get("device/",params)
    console.log(data);
    return data
}
// function getDeice(params) {

// }

async function removeDevice(params) {
    return
}

export {getDeice}