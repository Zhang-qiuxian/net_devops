<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">设备ARP信息通过SNMP同步获取，暂不支持修改！</el-text>
            </div>
            <div class="from-right">
                <el-button type="info" @click="exportExcel('device/arp/export_excel/')">导出arp信息</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加设备或刷新页面" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="device_arp.data" border table-layout="auto" style="width: 100%">
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="接口状态" prop="ifOperStatus" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.ifOperStatus == 1">已启用</el-tag>
                            <el-tag type="danger" v-else>未启用</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="更新时间" prop="update_time" align="center">
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="device_arp.page" v-model:page-size="device_arp.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_arp.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';


const stores = useDeviceStore();
const { device_arp } = storeToRefs(stores);

const isData = computed(() => {
    return device_arp.value.data.length > 0 ? true : false;
})

// 处理分页
const handleSizeChange = (val) => {
    device_arp.page_size = val
    stores.getArp()
}
const handleCurrentChange = (val) => {
    device_arp.page = val
    stores.getArp();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "设备名称",
    ip: "设备ip",
    // atIfIndex: "接口索引",
    atNetAddress: "IP地址",
    atPhysAddress: "MAC地址",
    ifName: "接口名称",
    ifAlias: "接口别名",
    // ifOperStatus: "接口状态",
    // update_time: "更新时间"
}

// {
//     "id": 1,
//     "device_id": "2a2e69a8-65ed-4871-99e6-460b2df34915",
//     "name": "6604",
//     "ip": "1.1.1.1",
//     "atIfIndex": 655,
//     "atPhysAddress": "24:e9:b3:2c:46:53",
//     "atNetAddress": "1.1.1.1",
//     "ifName": "GigabitEthernet2/0/14",
//     "ifAlias": "GigabitEthernet2/0/14 Interface",
//     "ifOperStatus": 1,
//     "update_time": "2024-05-10 14:56:37"
// }

onMounted(() => {
    stores.getArp();
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
