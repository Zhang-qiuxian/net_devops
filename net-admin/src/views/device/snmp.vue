<template>
    <div class="container">
        <div class="from-container">
            <el-button type="success" @click="drawer = true">添加SNMP模板</el-button>
            <!-- <el-button type="info" @click="exportExcel('device/info/export_excel/')">导出设备</el-button> -->
        </div>
        <div class="table-container">
            <el-scrollbar>
                <el-table :data="device_snmp.data" border table-layout="auto" style="width: 100%">
                    <!-- <el-table-column type="selection" width="50" /> -->
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="操作" align="center" width="150">
                        <template #default="scope">
                            <el-button size="small" @click="handleEdit(scope.row)">
                                <span>编辑</span>
                            </el-button>
                            <el-popconfirm title="确认删除吗？" @confirm="handleDelete(scope.row)">
                                <template #reference>
                                    <el-button size="small" type="danger">
                                        <span>删除</span>
                                    </el-button>
                                </template>
                            </el-popconfirm>
                            <!-- // <el-button size="small" type="danger" @click="handleDelete(scope.row)">
                            //     <span>删除</span>
                            // </el-button> -->
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="pages.page" v-model:page-size="pages.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_snmp.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加设备</h4>
        </template>
        <template #default>
            <div class="form-drawer">
                <div class="form-text">
                    <el-text type="danger">注意！ v1和v2c只需要填写三项。v3需要根据实际填写。推荐v2c</el-text>
                </div>
                <div class="form-content">
                    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules"
                        label-width="auto" status-icon>
                        <el-form-item label="版本" prop="version">
                            <el-select v-model="ruleForm.version" placeholder="请选择" style="width: 240px">
                                <!-- <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" /> -->
                                <el-option v-for="item in versionOptions" :key="item.value" :label="item.label"
                                    :value="item.value" />
                            </el-select>
                        </el-form-item>
                        <el-form-item :label="v" :prop="k" v-for="(v, k) in ruleFields" :key="k">
                            <el-input v-model="ruleForm[k]" />
                        </el-form-item>
                        <el-form-item style="">
                            <el-button @click="cancelClick">关闭</el-button>
                            <el-button type="primary" @click="confirmClick(ruleFormRef)">提交</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </template>
    </el-drawer>
    <el-dialog v-model="dialogTableVisible" title="修改SNMP模板" :width="600">
        <el-form ref="ruleFormRef" style="max-width: 600px" :model="editForm" :rules="rules" label-width="auto"
            status-icon>
            <el-row>
                <el-col :span="12">
                    <el-form-item label="版本" prop="version">
                        <el-select v-model="editForm.version" placeholder="请选择" style="width: 240px">
                            <el-option v-for="item in versionOptions" :key="item.value" :label="item.label"
                                :value="item.value" />
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12" v-for="(v, k) in ruleFields" :key="k">
                    <el-form-item :label="v" :prop="k">
                        <el-input v-model="editForm[k]" />
                    </el-form-item>
                </el-col>
            </el-row>
            <el-row justify="end">
                <el-col>
                    <el-form-item>
                        <el-button @click="closeClick">关闭</el-button>
                        <el-button type="primary" @click="editSnmp(ruleFormRef)">提交</el-button>
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
import { ElMessage } from 'element-plus';


const stores = useDeviceStore();
const { device_snmp, pages } = storeToRefs(stores);

// 表单
const ruleFormRef = ref()
const ruleForm = reactive({
    name: "public",
    version: 2,
    community: "public",
    security_username: "user",
    auth_password: "pass",
    auth_protocol: "MD5",
    security_level: "noAuthNoPriv",
    privacy_protocol: "EDS",
    privacy_password: "otherPass",
    context: "context",
})
// 控制表单渲染
const ruleFields = {
    // version: "版本",
    name: "模板名称",
    community: "团体字",
    security_username: "用户名(v3)",
    auth_password: "密码(v3)",
    auth_protocol: "认证协议(v3)",
    security_level: "认证级别(v3)",
    privacy_protocol: "私有协议(v3)",
    privacy_password: "私有密码(v3)",
    context: "上下文(v3)",
}

const versionOptions = [
    {
        label: 'v1',
        value: 1,
    },
    {
        label: 'v2c',
        value: 2,
    },
    {
        label: 'v3',
        value: 3,
    },
]

const editForm=reactive({})

const rules = reactive({
    version: [{ required: true, message: '必选项', trigger: 'blur' },],
    name: [{ required: true, message: '必选项', trigger: 'blur' },],
    community: [{ required: true, message: '必填项', trigger: 'change', },],
})
// 添加表单
async function confirmClick(formEl) {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.addSnmp(ruleForm).then((res) => {
                // console.log(res);
                stores.getSnmp();
                ElMessage.success('添加成功')
                ruleFormRef.value.resetFields()
                drawer.value = false
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
    // console.log(row)
    dialogTableVisible.value = true
    // ruleFormRef.value.resetFields()
    editForm.id = row.id
    editForm.version = row.version
    editForm.name = row.name
    editForm.community = row.community
    editForm.security_username = row.security_username
    editForm.auth_password = row.auth_password
    editForm.auth_protocol = row.auth_protocol
    editForm.security_level = row.security_level
    editForm.privacy_protocol = row.privacy_protocol
}
const handleDelete = (row) => {
    stores.deleteSnmp(row.id).then(() => {
        ElMessage.success('删除成功')
        stores.getSnmp();
    })
}
const closeClick = () => {
    ruleFormRef.value.resetFields()
    dialogTableVisible.value = false
}
const editSnmp = async (formEl) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.updateSnmp(editForm.id, editForm).then(() => {
                stores.getSnmp();
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
    pages.page_size = val
    stores.getSnmp()
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getSnmp();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "模板名称",
    version: "版本",
    community: "团体字",
    security_username: "用户名",
    auth_password: "密码",
    auth_protocol: "认证协议",
    security_level: "认证级别",
    privacy_protocol: "私有协议",
    privacy_password: "私有密码",
    context: "上下文",
}
// 抽屉
const drawer = ref(false)

function cancelClick() {
    drawer.value = false
    ruleFormRef.value.resetFields()
}



onMounted(() => {
    stores.getSnmp();
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

<style lang="scss">
.el-drawer__body {
    padding: 0 20px;
}
</style>
