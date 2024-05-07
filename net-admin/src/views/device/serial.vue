<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">序列号信息通过SNMP同步获取，暂不支持修改！</el-text>
            </div>
            <div class="from-right">
                <el-button type="info" @click="exportExcel('device/serial/export_excel/')">导出序列号</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加设备或刷新页面" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="device_serial.data" border table-layout="auto" style="width: 100%">
                    <!-- <el-table-column type="selection" width="50" /> -->
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="device_serial.page" v-model:page-size="device_serial.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_serial.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';


const stores = useDeviceStore();
const { device_serial } = storeToRefs(stores);

const isData = computed(() => {
    return device_serial.value.data.length > 0 ? true : false;
})
// 处理分页
const handleSizeChange = (val) => {
    device_serial.page_size = val
    stores.getSerial()
}
const handleCurrentChange = (val) => {
    device_serial.page = val
    stores.getSerial();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "设备名称",
    ip: "设备ip",
    entPhysicalDescr: "物理实体描述",
    entPhysicalName: "物理实体名",
    entPhysicalSerialNum: "序列号",
    entPhysicalSoftwareRev: "软件版本号",
    entPhysicalModelName: "模型名称",
}

// {
//     "id": 932,
//     "device_id": "0d37703e-a77c-4420-baec-7a5fd6216c54",
//     "name": "浦西办公网核心-s7506x",
//     "ip": "10.254.11.249",
//     "entPhysicalDescr": "GigabitEthernet0/0/22",
//     "entPhysicalName": "GigabitEthernet0/0/22",
//     "entPhysicalSerialNum": "210231A961X2090002ZM",
//     "entPhysicalSoftwareRev": "",
//     "entPhysicalModelName": "SFP-GE-SX-MM850-D"
// }


onMounted(() => {
    stores.getSerial();
    stores.getSerial().then(res => { console.log(res) });
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
