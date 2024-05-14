<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">定时任务详情</el-text>
            </div>
            <div class="from-right">
                <el-button type="info" @click="exportExcel('device/system/export_excel/')">导出系统信息</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加定时任务或检查定时任务是否在运行。" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="cron_result.data" border table-layout="auto" style="width: 100%">
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="cron_result.page" v-model:page-size="cron_result.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="cron_result.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>
<script setup>
import { useCrontore } from '@/stores/cron/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';
import { ElLoading } from 'element-plus'

const stores = useCrontore();
const { cron_result } = storeToRefs(stores);


const isData = computed(() => {
    return cron_result.value.data.length > 0 ? true : false;
})

// 处理分页
const handleSizeChange = (val) => {
    cron_result.page_size = val
    stores.getResult()
}
const handleCurrentChange = (val) => {
    cron_result.page = val
    stores.getResult();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "设备名称",
    ip: "设备ip",
    sysName: "设备名称",
    sysUpTime: "系统启动时间",
    sysDescr: "系统描述",
}

// {
//     "id": 50,
//     "device_id": "63297486-d08d-467c-b31a-3b91e33459e8",
//     "name": "2F交换机",
//     "ip": "1.1.1.1",
//     "sysDescr": "H3C Comware Platform Software, Software Version 7.1.070, Release 6318P01\r\n",
//     "sysUpTime": "326:0:53:39.48",
//     "sysName": "2F_IRF"
// }

const loading = ElLoading.service({
    lock: true,
    text: '正在加载',
    background: 'rgba(0, 0, 0, 0.7)',
})

onMounted(() => {
    stores.getResult();
    loading.close()
})


</script>

<style lang="scss" scoped>
.container {
    height: 100%;
    display: flex;
    flex-direction: column;
}

.from-container {
    height: 39px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    border-bottom: 1px solid #ccc;
    padding-right: 20px;
}

.table-container {
    padding: 10px 10px 0 10px;
    flex: 1;
    overflow: auto;
}

.page-container {
    height: 39px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding-right: 20px;
}
</style>
