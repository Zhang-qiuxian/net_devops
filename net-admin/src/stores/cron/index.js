import { ref, computed, reactive } from 'vue'
import { defineStore } from 'pinia'
import setLocalStore from '@/utils/setLocalStore'
import {
    getResultApi,
    getClockApi,
    getIntervalApi,
    getPeriodicApi,
    getCrontabApi,
    getResultDetailApi,
    getClockDetailApi,
    getIntervalDetailApi,
    getPeriodicDetailApi,
    getCrontabDetailApi,
    // deleteCronResultApi,
    deleteCronClockApi,
    deleteCronIntervalApi,
    deleteCronPeriodicApi,
    deleteCronCrontabApi,
    // createCronResultApi,
    createCronClockApi,
    createCronIntervalApi,
    createCronPeriodicApi,
    createCronCrontabApi,
    // updateCronResultApi,
    updateCronClockApi,
    updateCronIntervalApi,
    updateCronPeriodicApi,
    updateCronCrontabApi,
    getTasksApi,
    getLogsApi

} from '@/api/cron/index.js'



export const useCrontore = defineStore('cron', () => {
    const cron_clocked = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })
    const cron_crontab = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })
    const cron_interval = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })
    const cron_periodic = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })
    const cron_tasks = ref({
        tasks: [],
    })
    const cron_result = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })
    const cron_logs = ref({
        total: 0,
        data: [],
        page: 1,
        page_size: 20
    })



    // 查询
    const getClocked = async () => {
        return await getClockApi({ page: cron_clocked.value.page, page_size: cron_clocked.value.page_size }).then(res => {
            cron_clocked.value.total = res.total
            cron_clocked.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    const getCrontab = async () => {
        return await getCrontabApi({ page: cron_crontab.value.page, page_size: cron_crontab.value.page_size }).then(res => {
            cron_crontab.value.total = res.total
            cron_crontab.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    const getInterval = async () => {
        return await getIntervalApi({ page: cron_interval.value.page, page_size: cron_interval.value.page_size }).then(res => {
            cron_interval.value.total = res.total
            cron_interval.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    const getPeriodic = async () => {
        return await getPeriodicApi({ page: cron_periodic.value.page, page_size: cron_periodic.value.page_size }).then(res => {
            cron_periodic.value.total = res.total
            cron_periodic.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    const getResult = async () => {
        return await getResultApi({ page: cron_result.value.page, page_size: cron_result.value.page_size }).then(res => {
            cron_result.value.total = res.total
            cron_result.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    const getTasks = async () => {
        return await getTasksApi().then(res => {
            cron_tasks.value.tasks = res.tasks
        })
    }

    const getLogs = async () => {
        return await getLogsApi({ page: cron_logs.value.page, page_size: cron_logs.value.page_size }).then(res => {
            cron_logs.value.total = res.total
            cron_logs.value.data = res.data
            return true
        }).catch(err => {
            return false
        })
    }

    // 新增
    const addClocked = async (data) => createCronClockApi(data)
    const addCrontab = async (data) => createCronCrontabApi(data)
    const addInterval = async (data) => createCronIntervalApi(data)
    const addPeriodic = async (data) => createCronPeriodicApi(data)

    // 修改
    const updateClocked = async (id, data) => updateCronClockApi(id, data)
    const updateCrontab = async (id, data) => updateCronCrontabApi(id, data)
    const updateInterval = async (id, data) => updateCronIntervalApi(id, data)
    const updatePeriodic = async (id, data) => updateCronPeriodicApi(id, data)

    // 删除
    const deleteClocked = async (id) => deleteCronClockApi(id)
    const deleteCrontab = async (id) => deleteCronCrontabApi(id)
    const deleteInterval = async (id) => deleteCronIntervalApi(id)
    const deletePeriodic = async (id) => deleteCronPeriodicApi(id)

    const refreshAll = () => {
        getClocked()
        getInterval()
        getCrontab()
        getPeriodic()
        getTasks()
    }

    return {
        cron_clocked, cron_crontab, cron_interval, cron_periodic, cron_tasks, cron_result,cron_logs,
        getClocked, getCrontab, getInterval, getPeriodic, getResult,getTasks,getLogs,
        addClocked, addCrontab, addInterval, addPeriodic,
        updateClocked, updateCrontab, updateInterval, updatePeriodic,
        deleteClocked, deleteCrontab, deleteInterval, deletePeriodic,
        refreshAll
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
                key: setLocalStore('cron'),
                paths: ['cron_clocked', 'cron_crontab', 'cron_interval', 'cron_periodic', 'cron_tasks', 'cron_result','cron_logs']
            }
        ],
    })
