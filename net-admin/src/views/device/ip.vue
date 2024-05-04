<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">IP信息通过SNMP同步获取，暂不支持修改！</el-text>
            </div>
            <div class="from-right">
                <!-- <el-button type="success" @click="drawer = true">添加设备</el-button> -->
                <el-button type="info" @click="exportExcel('device/ip/export_excel/')">导出IP</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-scrollbar>
                <el-table :data="device_ip.data" border table-layout="auto" style="width: 100%">
                    <el-table-column type="selection" width="50" />
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="接口状态" prop="ifOperStatus" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.ifOperStatus == 1">已启用</el-tag>
                            <el-tag type="danger" v-else>未启用</el-tag>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="pages.page" v-model:page-size="pages.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_ip.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';


const stores = useDeviceStore();
const { device_ip, pages } = storeToRefs(stores);

console.log(device_ip.value);
console.log(pages.value);


// 处理分页
const handleSizeChange = (val) => {
    pages.page_size = val
    stores.getIp()
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getIp();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "设备名称",
    ip: "设备ip",
    ifName: "接口名称",
    ifAlias: "接口别名",
    // ipAdEntIfIndex: "接口索引",
    ipAdEntAddr: "IP地址",
    ipAdEntNetMask: "子网掩码",
    // ifOperStatus: "接口状态",
}

// {
//     "id": 427,
//     "device_id": "63297486-d08d-467c-b31a-3b91e33459e8",
//     "name": "浦西2F交换机",
//     "ip": "10.254.11.2",
//     "ipAdEntAddr": "10.254.11.2",
//     "ipAdEntIfIndex": 638,
//     "ipAdEntNetMask": "255.255.255.0",
//     "ifName": "Vlan-interface126",
//     "ifAlias": "IDF_MAN_NEW"
// }


onMounted(() => {
    stores.getIp();
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
