<template>
    <div class="container">
        <div class="from-container">
            <div class="from-left">
                <el-text type="danger">接口信息通过SNMP同步获取，暂不支持修改！</el-text>
            </div>
            <div class="from-right">
                <!-- <el-button type="success" @click="drawer = true">添加设备</el-button> -->
                <el-button type="info" @click="exportExcel('device/interface/export_excel/')">导出接口</el-button>
            </div>
        </div>
        <div class="table-container">
            <el-scrollbar>
                <el-table :data="device_interface.data" border table-layout="auto" style="width: 100%">
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
                :total="device_interface.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加设备</h4>
        </template>
        <template #default>
            <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules" label-width="auto"
                :size="formSize" status-icon>
                <el-form-item label="Activity name" prop="name">
                    <el-input v-model="ruleForm.name" />
                </el-form-item>
            </el-form>
        </template>
        <template #footer>
            <div style="flex: auto">
                <el-button @click="cancelClick">cancel</el-button>
                <el-button type="primary" @click="confirmClick">confirm</el-button>
            </div>
        </template>
    </el-drawer>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';


const stores = useDeviceStore();
const { device_interface, pages } = storeToRefs(stores);

console.log(device_interface.value);
console.log(pages.value);


const handleEdit = (index, row) => {
    console.log(index, row)
}
const handleDelete = (index, row) => {
    console.log(index, row)
}
// 处理分页
const handleSizeChange = (val) => {
    pages.page_size = val
    stores.getInterface()
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getInterface();
}
// 控制表格字段
const tableTitle = {
    id: "",
    name: "设备名称",
    ip: "设备ip",
    ifIndex: "接口索引",
    ifName: "接口名称",
    ifDescr: "接口描述",
    // ifOperStatus: "接口状态",
    ifAlias: "接口别名",
    ifPhysAddress: "接口物理地址",
    ifHighSpeed: "接口速率(Mbps)",
}
// 抽屉
const drawer = ref(false)
const handleClose = (done) => {
    ElMessageBox.confirm('Are you sure you want to close this?')
        .then(() => {
            done()
        })
        .catch(() => {
            // catch error
        })
}
function cancelClick() {
    drawer.value = false
}
function confirmClick() {
    ElMessageBox.confirm(`Are you confirm to chose ${radio1.value} ?`)
        .then(() => {
            drawer2.value = false
        })
        .catch(() => {
            // catch error
        })
}

// 表单
const ruleFormRef = ref()
const ruleForm = reactive({
    name: 'Hello',
})
const locationOptions = ['Home', 'Company', 'School']

const rules = reactive({
    name: [
        { required: true, message: 'Please input Activity name', trigger: 'blur' },
        { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
    ],
})

const submitForm = async (formEl) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            console.log('submit!')
        } else {
            console.log('error submit!', fields)
        }
    })
}

const resetForm = (formEl) => {
    if (!formEl) return
    formEl.resetFields()
}

const options = Array.from({ length: 10000 }).map((_, idx) => ({
    value: `${idx + 1}`,
    label: `${idx + 1}`,
}))



onMounted(() => {
    stores.getInterface();
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
