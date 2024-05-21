<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">后台任务日志</el-text>
            </div>
            <div class="from-right">
                <el-button type="info" @click="exportExcel('device/system/export_excel/')">导出系统信息</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加定时任务或检查定时任务是否在运行。" v-if="!isData" style="height: 100%;" row-key="id" />
            <el-scrollbar v-else>
                <el-table :data="cron_logs.data" border table-layout="auto" style="width: 100%" >
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="任务完成状态" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.status == 'success'">成功</el-tag>
                            <el-tag type="danger" v-else>失败</el-tag>
                        </template>
                    </el-table-column>
                    
                    <el-table-column label="操作" align="center">
                        <template #default="scope">
                            <el-button type="primary" @click="handleInfo(scope.row)">详情</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="cron_logs.page" v-model:page-size="cron_logs.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="cron_logs.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
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
const { cron_logs } = storeToRefs(stores);


const isData = computed(() => {
    return cron_logs.value.data.length > 0 ? true : false;
})

// 处理分页
const handleSizeChange = (val) => {
    cron_logs.page_size = val
    stores.getResult()
}
const handleCurrentChange = (val) => {
    cron_logs.page = val
    stores.getResult();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    job: "任务名称",
    create_time: "任务执行时间",
    // status: "任务完成状态",
    // data: "任务执行结果",
}

// {
//     "id": 712,
//     "job": "同步基础信息",
//     "status": "success",
//     "data": [],
//     "create_time": "2024-05-21 09:01:51"
// }

const loading = ElLoading.service({
    lock: true,
    text: '正在加载',
    background: 'rgba(0, 0, 0, 0.7)',
})

onMounted(() => {
    stores.getLogs();
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
