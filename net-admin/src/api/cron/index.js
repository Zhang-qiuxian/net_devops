import instance from "../service";

const cronResult = "/cron/task_result/";
const cronClock = "/cron/clock/";
const cronInterval = "/cron/interval/";
const cronCrontab = "/cron/crontab/";
const cronPeriodic = "/cron/periodic/";

// 获取列表
export const getCronResultApi = async (params) => {
    return instance.get(cronResult, { params });
}

export const getCronClockApi = async (params) => {
    return instance.get(cronClock, { params });
}

export const getCronIntervalApi = async (params) => {
    return instance.get(cronInterval, { params });
}

export const getCronPeriodicApi = async (params) => {
    return instance.get(cronPeriodic, { params });
}

export const getCronCrontabApi = async (params) => {
    return instance.get(cronCrontab, { params });
}

// 获取详情
export const getCronResultDetailApi = async (id) => {
    return instance.get(`${cronResult}${id}/`);
}

export const getCronClockDetailApi = async (id) => {
    return instance.get(`${cronClock}${id}/`);
}

export const getCronIntervalDetailApi = async (id) => {
    return instance.get(`${cronInterval}${id}/`);
}

export const getCronPeriodicDetailApi = async (id) => {
    return instance.get(`${cronPeriodic}${id}/`);
}

export const getCronCrontabDetailApi = async (id) => {
    return instance.get(`${cronCrontab}${id}/`);
}

// 删除
export const deleteCronResultApi = async (id) => {
    return instance.delete(`${cronResult}${id}/`);
}

export const deleteCronClockApi = async (id) => {
    return instance.delete(`${cronClock}${id}/`);
}

export const deleteCronIntervalApi = async (id) => {
    return instance.delete(`${cronInterval}${id}/`);
}

export const deleteCronPeriodicApi = async (id) => {
    return instance.delete(`${cronPeriodic}${id}/`);
}

export const deleteCronCrontabApi = async (id) => {
    return instance.delete(`${cronCrontab}${id}/`);
}

// 创建
export const createCronResultApi = async (data) => {
    return instance.post(cronResult, data);
}

export const createCronClockApi = async (data) => {
    return instance.post(cronClock, data);
}

export const createCronIntervalApi = async (data) => {
    return instance.post(cronInterval, data);
}

export const createCronPeriodicApi = async (data) => {
    return instance.post(cronPeriodic, data);
}

export const createCronCrontabApi = async (data) => {
    return instance.post(cronCrontab, data);
}

// 更新
export const updateCronResultApi = async (id, data) => {
    return instance.put(`${cronResult}${id}/`, data);
}

export const updateCronClockApi = async (id, data) => {
    return instance.put(`${cronClock}${id}/`, data);
}

export const updateCronIntervalApi = async (id, data) => {
    return instance.put(`${cronInterval}${id}/`, data);
}

export const updateCronPeriodicApi = async (id, data) => {
    return instance.put(`${cronPeriodic}${id}/`, data);
}

export const updateCronCrontabApi = async (id, data) => {
    return instance.put(`${cronCrontab}${id}/`, data);
}

