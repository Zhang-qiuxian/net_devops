<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">设备系统信息通过SNMP同步获取，暂不支持修改！</el-text>
            </div>
            <div class="from-right">
                <!-- <el-button type="success" @click="drawer = true">添加设备</el-button> -->
                <el-button type="info" @click="exportExcel('device/system/export_excel/')">导出系统信息</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-scrollbar>
                <el-table :data="device_system.data" border table-layout="auto" style="width: 100%">
                    <!-- <el-table-column type="selection" width="50" /> -->
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="pages.page" v-model:page-size="pages.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_system.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';


const stores = useDeviceStore();
const { device_system, pages } = storeToRefs(stores);

console.log(device_system.value);
console.log(pages.value);


// 处理分页
const handleSizeChange = (val) => {
    pages.page_size = val
    stores.getSystem()
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getSystem();
}
// 控制表格字段
const tableTitle = {
    id: "",
    name: "设备名称",
    ip: "设备ip",
    sysName: "设备名称",
    sysUpTime: "系统启动时间",
    sysDescr: "系统描述",
}

// {
//     "id": 50,
//     "device_id": "63297486-d08d-467c-b31a-3b91e33459e8",
//     "name": "浦西2F交换机",
//     "ip": "10.254.11.2",
//     "sysDescr": "H3C Comware Platform Software, Software Version 7.1.070, Release 6318P01\r\nH3C S5130S-52P-EI\r\nCopyright (c) 2004-2020 New H3C Technologies Co., Ltd. All rights reserved.",
//     "sysUpTime": "326:0:53:39.48",
//     "sysName": "ZWY_2F_IRF"
// }


onMounted(() => {
    stores.getSystem();
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
