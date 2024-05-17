<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <div class="from-refresh">
                    <el-text type="danger">手动刷新ARP，注意！点击后后台会自动刷新，每分钟限定刷新一次！</el-text>
                    <el-button type="primary" round :icon="Refresh" @click="refreshARP">更新ARP</el-button>
                </div>
            </div>
            <div class="from-right">
                <el-text type="danger">设备ARP信息通过SNMP同步获取，暂不支持修改！30分钟同步一次！</el-text>
                <el-button type="info" @click="exportExcel('device/arp/export_excel/')">导出arp信息</el-button>
                <el-button type="success" round :icon="RefreshRight" @click="refreshPage">刷新页面</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先手动同步或刷新页面。" v-if="!isData" style="height: 100%;" />
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
                    <el-table-column label="IP在线状态" prop="is_active" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.is_active == true">在线</el-tag>
                            <el-tag type="danger" v-else>离线</el-tag>
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
import { ElLoading } from 'element-plus';
import { refreshArpApi } from '@/api/device/index.js';
import {
    Refresh,
    RefreshRight
} from '@element-plus/icons-vue'


const stores = useDeviceStore();
const { device_arp, device_info } = storeToRefs(stores);

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
    ipNetToMediaNetAddress: "IP地址",
    ipNetToMediaPhysAddress: "MAC地址",
    ifName: "接口名称",
    ifAlias: "接口别名",
    // ifOperStatus: "接口状态",
    // update_time: "更新时间"
}

// 手动刷新ARP
const refreshARP = () => { refreshArpApi().then(res => ElMessage.success(res)) }

const refreshPage = () => {
  window.location.reload();
};

// 导出arp信息
const exportExcelData = () => {
    exportExcel('device/arp/export_excel/')
}

const loading = ElLoading.service({
    lock: true,
    text: '正在加载',
    background: 'rgba(0, 0, 0, 0.7)',
})

onMounted(() => {
    stores.getArp();
    loading.close();
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
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ccc;
    padding-right: 20px;
    padding-left: 20px;

    .from-left {
        height: 100%;
        line-height: 40px;

        .el-form-item {
            margin-bottom: 0px;

        }
    }
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
