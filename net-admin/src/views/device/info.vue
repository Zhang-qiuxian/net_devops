<template>
    <div class="container">
        <div class="from-container">
            <el-button @click="exportExcel('device/info/export_excel_templates/')">导入设备模板</el-button>
            <el-button type="primary" @click="importExcel('device/info/import_excel/')">批量导入设备</el-button>
            <el-button type="success" @click="drawer = true">添加设备</el-button>
            <el-button type="info" @click="exportExcel('device/info/export_excel/')">导出设备</el-button>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加设备或刷新页面" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="device_info.data" border table-layout="auto" style="width: 100%">
                    <el-table-column type="selection" width="50" />
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="是否同步" prop="is_sync" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.is_sync == 1">已同步</el-tag>
                            <el-tag type="danger" v-else>未同步</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" align="center">
                        <template #default="scope">
                            <el-button size="small" @click="handleEdit(scope.row)">
                                <span>编辑</span>
                            </el-button>
                            <!-- <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                                <span>删除</span>
                            </el-button> -->
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="device_info.page" v-model:page-size="device_info.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_info.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加设备</h4>
        </template>
        <template #default>
            <div class="form-drawer">
                <div class="form-text">
                    <el-text type="danger">注意请先添加SNMP模板,设备厂家后再添加设备。</el-text>
                </div>
                <div class="form-content">
                    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules"
                        label-width="auto" status-icon>
                        <el-row :gutter="20" style="margin:0px;">
                            <el-col :span="12" v-for="(v, k) in ruleFields">
                                <el-form-item :prop="k" :key="k" :label="v">
                                    <el-input v-model="ruleForm[k]" />
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item prop="snmp_id" label="SNMP模板">
                                    <el-select v-model="ruleForm.snmp_id">
                                        <el-option v-for="item in snmpOptions" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item prop="company_id" label="设备厂家">
                                    <el-select v-model="ruleForm.company_id">
                                        <el-option v-for="item in companyOptions" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>

                        <el-form-item>
                            <el-button @click="cancelClick">关闭</el-button>
                            <el-button type="primary" @click="confirmClick(ruleFormRef)">提交</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </template>
    </el-drawer>
    <el-dialog v-model="dialogTableVisible" title="修改设备信息" :width="600">
        <el-form ref="ruleFormRef" style="max-width: 600px" :model="editForm" :rules="rules" label-width="auto"
            status-icon>
            <el-row>
                <el-col :span="12" v-for="(v, k) in ruleFields" :key="k">
                    <el-form-item :label="v" :prop="k">
                        <el-input v-model="editForm[k]" />
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item prop="snmp_id" label="SNMP模板">
                        <el-select v-model="editForm.snmp_id">
                            <el-option v-for="item in snmpOptions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item prop="company_id" label="设备厂家">
                        <el-select v-model="editForm.company_id">
                            <el-option v-for="item in companyOptions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row justify="end">
                <el-col>
                    <el-form-item>
                        <el-button @click="closeClick">关闭</el-button>
                        <el-button type="primary" @click="editDevice(ruleFormRef)">提交</el-button>
                    </el-form-item>
                </el-col>
            </el-row>

        </el-form>
    </el-dialog>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';
import { ElLoading } from 'element-plus'


const stores = useDeviceStore();
const { device_info, device_snmp, device_company } = storeToRefs(stores);

const isData = computed(() => {
    return device_info.value.data.length > 0 ? true : false;
})

// const loading = ElLoading.service({
//     lock: true,
//     text: '正在加载...',
//     background: 'rgba(0, 0, 0, 0.7)',
// })

// 抽屉
const drawer = ref(false)

// 表单
const ruleFormRef = ref()

const ruleForm = reactive({
    name: "",
    description: "",
    hostname: "",
    ip: "",
    login: "ssh",
    url: "-",
    username: "root",
    password: "root",
    snmp_id: 1,
    company_id: 1,
})

const editForm = reactive({})

// 控制表单渲染
const ruleFields = {
    name: "设备名称",
    description: "设备描述",
    hostname: "设备主机名",
    ip: "设备IP",
    login: "设备登录方式",
    url: "登录网址",
    username: "登录账号",
    password: "登录密码",

}

// {
//     "device_id": "0d37703e-a77c-4420-baec-7a5fd6216c54",
//     "system": [
//     ],
//     "name": "办公网核心-s7506x",
//     "description": "核心交换机",
//     "hostname": "cs7506x-4f",
//     "ip": "10.1.1.2",
//     "login": "ssh",
//     "url": "-",
//     "username": "root",
//     "password": "xxx",
//     "remark": null,
//     "create_time": "2024-04-19 10:32:38",
//     "update_time": "2024-04-19 10:33:07",
//     "is_sync": true
// }

const snmpOptions = computed(() => {
    return device_snmp.value.data.map((item) => {
        return { label: item.name, value: item.id }
    })
})

const companyOptions = computed(() => {
    return device_company.value.data.map((item) => {
        return { label: item.name, value: item.id }
    })
})




const rules = reactive({
    name: [{ required: true, message: '必选项', trigger: 'blur' },],
    description: [{ required: true, message: '必选项', trigger: 'blur' },],
    hostname: [{ required: true, message: '必填项', trigger: 'blur', },],
    ip: [{ required: true, message: '必填项', trigger: 'blur', },],
    login: [{ required: true, message: '必填项', trigger: 'blur', },],
    url: [{ required: true, message: '必填项', trigger: 'blur', },],
    username: [{ required: true, message: '必填项', trigger: 'blur', },],
    password: [{ required: true, message: '必填项', trigger: 'blur', },],
    snmp_id: [{ required: true, message: '必选项', trigger: 'blur', },],
    company_id: [{ required: true, message: '必选项', trigger: 'blur', },],
})
// 添加表单
async function confirmClick(formEl) {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.addDevice(ruleForm).then((res) => {
                // console.log(res);
                if (res) {
                    stores.getDeviceInfo();
                    ElMessage.success('添加成功')
                    ruleFormRef.value.resetFields()
                    drawer.value = false
                } else {
                    ElMessage.error('添加失败')
                }

            }).catch((err) => {
                console.log(err);
                ElMessage.error('添加失败')
            })

        } else {
            console.log('error submit!', fields)
        }
    })
}

// 修改表单
const dialogTableVisible = ref(false)

const handleEdit = (row) => {
    console.log(row)
    dialogTableVisible.value = true
    // ruleFormRef.value.resetFields()
    editForm.device_id = row.device_id
    editForm.name = row.name
    editForm.description = row.description
    editForm.hostname = row.hostname
    editForm.ip = row.ip
    editForm.login = row.login
    editForm.url = row.url
    editForm.username = row.username
    editForm.password = row.password
    editForm.snmp_id = row.snmp_id
    editForm.company_id = row.company_id

}
const handleDelete = (row) => {
    stores.deleteDevice(row.id).then(() => {
        ElMessage.success('删除成功')
        stores.getDeviceInfo();
    })
}
const closeClick = () => {
    ruleFormRef.value.resetFields()
    dialogTableVisible.value = false
}

const editDevice = async (formEl) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.updateDevice(editForm.device_id, editForm).then(() => {
                stores.getDeviceInfo();
                ElMessage.success('修改成功')
                ruleFormRef.value.resetFields()
                dialogTableVisible.value = false
            })
        } else {
            console.log('error submit!', fields)
        }
    })
}

// const handleEdit = (index, row) => {
//     console.log(index, row)
// }
// const handleDelete = (index, row) => {
//     console.log(index, row)
// }
// 处理分页
const handleSizeChange = (val) => {
    device_info.page_size = val
    stores.getDeviceInfo();
    // loading.close()
}
const handleCurrentChange = (val) => {
    device_info.page = val
    stores.getDeviceInfo();
    // loading.close()
}
// 控制表格字段
const tableTitle = {
    name: "设备名称",
    description: "描述",
    hostname: "主机名",
    ip: "设备ip",
    login: "登录方式",
    username: "账号",
    password: "密码",
    url: "网址",
    // is_sync: "是否同步",
    create_time: "创建时间",
}

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



onMounted(() => {
    stores.getDeviceInfo()
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

.form-drawer {
    height: 100%;
    display: flex;
    flex-direction: column;

    .form-text {
        margin-bottom: 20px;
    }

    .form-content {
        flex: 1;
        overflow: auto;
    }

    .el-form {
        height: 100%;
    }
}
</style>
