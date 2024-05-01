import instance from "../service";

export const getAllDeiveApi = async (params) => {
     return await instance.get("device/info/",
        params
    )
}


export const getOneDeiveApi = async (id) => {
    return await instance.get({
        url: `"device/info/${id}/"`,
    })
}


export const createOneDeiveApi = async (data) => {
    return await instance.get({
        url: "device/info/",
        data
    })
}

export const exportDeiveApi = async () => {
    return await instance.get({
        url: "device/info/export_excel/",
    })
}
