<template>
    <div class="container">
        <div class="from-container">
            <!-- <div class="from-left">
                <el-text type="danger">后台任务详情</el-text>
            </div> -->
            <!-- <div class="from-right">
                <el-button type="info" @click="exportExcel('device/system/export_excel/')">导出系统信息</el-button>
            </div> -->
            <el-button type="success" round :icon="RefreshRight" @click="refreshPage">刷新页面</el-button>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加定时任务或检查定时任务是否在运行。" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="cron_result.data" border table-layout="auto" style="width: 100%">
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="任务完成情况" prop="status" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.status == 'SUCCESS'">成功</el-tag>
                            <el-tag type="warning" v-else-if="scope.row.status == 'STARTED'">正在运行</el-tag>
                            <el-tag type="danger" v-else>失败</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="执行结果" prop="result" align="center">
                        <template #default="scope">
                           {{ scope.row.result.job }}:{{ scope.row.result.message }}
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

const refreshPage = () => {
  window.location.reload();
};



// 导出
const handleExport = () => {
    exportExcel(cron_result.value.data, tableTitle, '定时任务结果')
}

// 控制表格字段
const tableTitle = {
    id: "序号",
    task_id: "任务ID",
    // periodic_task_name: "定时任务名称",
    // task_name: "任务名称",
    // task_args: "任务参数",
    // task_kwargs: "任务参数",
    // status: "任务状态",
    // worker: "执行者",
    content_type: "内容类型",
    content_encoding: "内容编码",
    date_created: "创建时间",
    date_done: "完成时间",
    traceback: "错误信息",
}

// {
//     "id": 786,
//     "result": {
//         "success": true,
//         "message": "成功了0台,失败了45台。"
//     },
//     "meta": {
//         "children": []
//     },
//     "task_id": "74d75e48-c167-4d38-987a-23a3b240f7c6",
//     "periodic_task_name": null,
//     "task_name": null,
//     "task_args": null,
//     "task_kwargs": null,
//     "status": "SUCCESS",
//     "worker": null,
//     "content_type": "application/x-python-serialize",
//     "content_encoding": "binary",
//     "date_created": "2024-05-21 09:41:47",
//     "date_done": "2024-05-21 09:41:51",
//     "traceback": null
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
