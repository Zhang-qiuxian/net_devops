import instance from "../service";

const result = "/cron/task_result/";
const clock = "/cron/clock/";
const interval = "/cron/interval/";
const crontab = "/cron/crontab/";
const periodic = "/cron/periodic/";
const tasks = "/cron/periodic/tasks/";

// 获取列表
export const getResultApi = async (params) => {
    return instance.get(result, { params });
}

export const getClockApi = async (params) => {
    return instance.get(clock, { params });
}

export const getIntervalApi = async (params) => {
    return instance.get(interval, { params });
}

export const getPeriodicApi = async (params) => {
    return instance.get(periodic, { params });
}

export const getCrontabApi = async (params) => {
    return instance.get(crontab, { params });
}

export const getTasksApi = async () => {
    return instance.get(tasks);
}

// 获取详情
export const getResultDetailApi = async (id) => {
    return instance.get(`${result}${id}/`);
}

export const getClockDetailApi = async (id) => {
    return instance.get(`${clock}${id}/`);
}

export const getIntervalDetailApi = async (id) => {
    return instance.get(`${interval}${id}/`);
}

export const getPeriodicDetailApi = async (id) => {
    return instance.get(`${periodic}${id}/`);
}

export const getCrontabDetailApi = async (id) => {
    return instance.get(`${crontab}${id}/`);
}

// 删除
// export const deleteCronResultApi = async (id) => {
//     return instance.delete(`${result}${id}/`);
// }

export const deleteCronClockApi = async (id) => {
    return instance.delete(`${clock}${id}/`);
}

export const deleteCronIntervalApi = async (id) => {
    return instance.delete(`${interval}${id}/`);
}

export const deleteCronPeriodicApi = async (id) => {
    return instance.delete(`${periodic}${id}/`);
}

export const deleteCronCrontabApi = async (id) => {
    return instance.delete(`${crontab}${id}/`);
}

// 创建
// export const createCronResultApi = async (data) => {
//     return instance.post(result, data);
// }

export const createCronClockApi = async (data) => {
    return instance.post(clock, data);
}

export const createCronIntervalApi = async (data) => {
    return instance.post(interval, data);
}

export const createCronPeriodicApi = async (data) => {
    return instance.post(periodic, data);
}

export const createCronCrontabApi = async (data) => {
    return instance.post(crontab, data);
}

// 更新
// export const updateCronResultApi = async (id, data) => {
//     return instance.put(`${result}${id}/`, data);
// }

export const updateCronClockApi = async (id, data) => {
    return instance.put(`${clock}${id}/`, data);
}

export const updateCronIntervalApi = async (id, data) => {
    return instance.put(`${interval}${id}/`, data);
}

export const updateCronPeriodicApi = async (id, data) => {
    return instance.put(`${periodic}${id}/`, data);
}

export const updateCronCrontabApi = async (id, data) => {
    return instance.put(`${crontab}${id}/`, data);
}

