import instance from "../service";

const cronResult = "/cron/task_result/";
const cronClock = "/cron/clock/";
const cronInterval = "/cron/interval/";
const cronCrontab = "/cron/periodic/";
const cronPeriodic = "/cron/periodic/";

// 获取列表
export const getAllCronResultApi = async (params) => {
    return instance.get(cronResult, { params });
}

export const getAllCronClockApi = async (params) => {
    return instance.get(cronClock, { params });
}

export const getAllCronIntervalApi = async (params) => {
    return instance.get(cronInterval, { params });
}

export const getAllCronPeriodicApi = async (params) => {
    return instance.get(cronPeriodic, { params });
}