<template>
    <div class="container">
        <div class="from-container">
            <div class="from-button">
                <el-button @click="exportExcel('device/info/export_excel_templates/')">导出设备模板</el-button>
            </div>
            <div class="from-button">
                <el-button type="primary" @click="dialogUploadVisible = true">批量导入设备</el-button>
            </div>
            <div class="from-button">
                <el-button type="success" @click="drawer = true">添加设备</el-button>
            </div>
            <div class="from-button">
                <el-button type="info" @click="exportExcel('device/info/export_excel/')">导出设备</el-button>
            </div>
            <div class="from-button">
                <el-button type="danger" @click="deleteSelect">删除设备</el-button>
            </div>

        </div>
        <!-- 表格 -->
        <div class="table-container">
            <el-empty description="没有数据，请先添加任务" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="cron_periodic.data" border table-layout="auto" style="width: 100%"
                    ref="multipleTableRef" @selection-change="handleSelectionChange">
                    <el-table-column type="selection" width="50" />
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="一次性任务" prop="one_off" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.one_off == true">是</el-tag>
                            <el-tag type="warning" v-else>否</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="任务状态" prop="enabled" align="center">
                        <template #default="scope">
                            <el-tag type="success" v-if="scope.row.enabled == true">正在运行</el-tag>
                            <el-tag type="danger" v-else>停止运行</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" align="center">
                        <template #default="scope">
                            <el-button size="small" @click="handleEdit(scope.row)">
                                <span>编辑</span>
                            </el-button>
                            <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                                <span>详情</span>
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <!-- 分页 -->
        <div class="page-container">
            <el-pagination v-model:current-page="cron_periodic.page" v-model:page-size="cron_periodic.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="cron_periodic.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <!-- 添加定时任务 -->
    <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加定时任务</h4>
        </template>
        <template #default>
            <div class="form-drawer">
                <div class="form-text">
                    <el-text type="danger">注意定时任务类型只需要选择其中一种</el-text>
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
    <!-- 修改设备弹窗 -->
    <el-dialog v-model="dialogTableVisible" title="修改定时任务信息" :width="600">
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
import { useCrontore } from '@/stores/cron/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { exportExcel } from '@/api/export-import';
import { ElLoading } from 'element-plus'


const stores = useCrontore();
const { cron_clocked, cron_crontab, cron_interval, cron_periodic, cron_tasks } = storeToRefs(stores);

const isData = computed(() => {
    return cron_periodic.value.data.length > 0 ? true : false;
})

// 上传文件
const dialogUploadVisible = ref(false)

const uploadUrl = ref(import.meta.env.VITE_API_URL + "device/info/import_excel/")

const handleUpload = (response, files, uploadFiles) => {
    if (response.code == 200) {
        ElMessage.success(response.message)
        dialogUploadVisible.value = false
        stores.getPeriodic()
    } else {
        ElMessage.error(response.message)
        dialogUploadVisible.value = false
        for (let item of response.data) {
            setTimeout(() => {
                ElNotification({
                    title: '导入失败',
                    message: `
                    name: ${item.name}
                    ip: ${item.ip}`,
                    type: 'error',
                    duration: 0
                })
            }, 500)
        }
    }
    //   ElMessage.warning(
    //     `The limit is 3, you selected ${files.length} files this time, add up to ${
    //       files.length + uploadFiles.length
    //     } totally`
    //   )
    console.log(response, files, uploadFiles);
}

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
    "id": "ID",
    "name": "任务名称",
    "description": "任务描述",
    "task": "任务函数",
    "args": "args参数",
    "kwargs": "kwargs参数",
    // "queue": null,
    // "exchange": null,
    // "routing_key": null,
    "headers": "请求头",
    "priority": "优先级",
    "expires": "到期",
    "expire_seconds": "到期时间",
    "one_off": "一次性任务",
    "start_time": "开始运行时间",
    "enabled": "任务状态",
    "last_run_at": "最后运行时间",
    "total_run_count": "任务运行次数",
    "date_changed": "最后改变时间",
    "interval": "间隔任务",
    "crontab": "crontab任务",
    // "solar": null,
    "clocked": "定时任务"

}



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
                    stores.getPeriodic();
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
        stores.getPeriodic();
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
                stores.getPeriodic();
                ElMessage.success('修改成功')
                ruleFormRef.value.resetFields()
                dialogTableVisible.value = false
            })
        } else {
            console.log('error submit!', fields)
        }
    })
}


// 处理分页
const handleSizeChange = (val) => {
    cron_periodic.page_size = val
    stores.getPeriodic();
    // loading.close()
}
const handleCurrentChange = (val) => {
    cron_periodic.page = val
    stores.getPeriodic();
    // loading.close()
}
// 控制表格字段
const tableTitle = {
    "id": "ID",
    "name": "任务名称",
    "description": "任务描述",
    "task": "任务函数",
    // "args": "args参数",
    // "kwargs": "kwargs参数",
    // "queue": null,
    // "exchange": null,
    // "routing_key": null,
    // "headers": "请求头",
    // "priority": "优先级",
    // "expires": "到期",
    // "expire_seconds": "到期时间",
    // "one_off": "一次性任务",
    // "start_time": "开始运行时间",
    // "enabled": "任务状态",
    "last_run_at": "最后运行时间",
    "total_run_count": "任务运行次数",
    // "date_changed": "最后改变时间",
    // "interval": "间隔任务",
    // "crontab": "crontab任务",
    // "solar": null,
    // "clocked": "定时任务"
}
// {
//     "id": 1,
//     "name": "celery.backend_cleanup",
//     "task": "celery.backend_cleanup",
//     "args": "[]",
//     "kwargs": "{}",
//     "queue": null,
//     "exchange": null,
//     "routing_key": null,
//     "headers": "{}",
//     "priority": null,
//     "expires": null,
//     "expire_seconds": 43200,
//     "one_off": false,
//     "start_time": null,
//     "enabled": true,
//     "last_run_at": null,
//     "total_run_count": 0,
//     "date_changed": "2024-05-13 20:51:21",
//     "description": "",
//     "interval": null,
//     "crontab": 1,
//     "solar": null,
//     "clocked": null
// }

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
const multipleTableRef = ref()
const multipleSelection = ref([])
const deleteSelect = () => {
    if (multipleSelection.value.length == 0) {
        ElMessage.error('请选择要删除的设备')
        return
    }
    console.log(multipleSelection.value);
    ElMessageBox.confirm('此操作将永久删除该设备以及SNMP同步的信息, 是否继续?')
        .then(() => {
            let device_ids = []
            multipleSelection.value.forEach((item) => {
                device_ids.push(item.device_id)
            })
            console.log(device_ids);
            stores.deleteDevice(device_ids).then((res) => {
                ElMessage.success('删除成功')
                stores.refreshAll()
            }).catch(res => {
                ElMessage.error('删除失败')
            })
        })
}

const handleSelectionChange = (val) => {
    multipleSelection.value = val
}

onMounted(() => {
    stores.getPeriodic()
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

    .from-button {
        margin: 0px 5px 0px 5px;
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
