<template>
    <div class="container">
        <div class="from-container">
            <el-button type="success" @click="drawer = true">添加设备厂家</el-button>
        </div>
        <div class="table-container">
            <el-empty description="没有数据，请先添加设备厂家或刷新页面" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="device_company.data" border table-layout="auto" style="width: 100%">
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
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <div class="page-container">
            <el-pagination v-model:current-page="device_company.page" v-model:page-size="device_company.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_company.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加设备厂家</h4>
        </template>
        <template #default>
            <div class="form-drawer">
                <div class="form-text">
                    <el-text type="danger">注意！ 厂家代码就是厂家的英文小写。</el-text>
                </div>
                <div class="form-content">
                    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules"
                        label-width="auto" status-icon>
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
    <el-dialog v-model="dialogTableVisible" title="修改厂家信息" :width="600">
        <el-form ref="ruleFormRef" style="max-width: 600px" :model="editForm" :rules="rules" label-width="auto"
            status-icon>
            <el-row>
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
                        <el-button type="primary" @click="editCompany(ruleFormRef)">提交</el-button>
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
const { device_company } = storeToRefs(stores);

const isData = computed(() => {
    return device_company.value.data.length > 0 ? true : false;
})

// 表单
const ruleFormRef = ref()
const ruleForm = reactive({
    name: "",
    code: "",
    model: "",
})
// 控制表单渲染
const ruleFields = {
    name: "厂家名称",
    code: "厂家代码",
    model: "设备型号",
}

// {
//   "code": "string",
//   "name": "string",
//   "model": "string"
// }



const editForm = reactive({})

const rules = reactive({
    name: [{ required: true, message: '必选项', trigger: 'blur' },],
    code: [{ required: true, message: '必选项', trigger: 'blur' },],
    model: [{ required: true, message: '必填项', trigger: 'change', },],
})
// 添加表单
async function confirmClick(formEl) {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.addCompany(ruleForm).then((res) => {
                // console.log(res);
                stores.getCompany();
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
    editForm.name = row.name
    editForm.code = row.code
    editForm.model = row.model

}
const handleDelete = (row) => {
    stores.deleteCompany(row.id).then(() => {
        ElMessage.success('删除成功')
        stores.getCompany();
    })
}
const closeClick = () => {
    ruleFormRef.value.resetFields()
    dialogTableVisible.value = false
}
const editCompany = async (formEl) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.updateCompany(editForm.id, editForm).then(() => {
                stores.getCompany();
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
    stores.getCompany()
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getCompany();
}
// 控制表格字段
const tableTitle = {
    id: "序号",
    name: "团体字",
    code: "厂家代码",
    model: "设备型号",

}
// 抽屉
const drawer = ref(false)

function cancelClick() {
    drawer.value = false
    ruleFormRef.value.resetFields()
}



onMounted(() => {
    stores.getCompany();
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
