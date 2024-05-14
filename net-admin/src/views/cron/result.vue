<template>
    <div class="container">
        <!-- 表格 -->
        <div class="table-container">
            <el-empty description="没有数据，请先添加定时任务" v-if="!isData" style="height: 100%;" />
            <el-scrollbar v-else>
                <el-table :data="cron_result.data" border table-layout="auto" style="width: 100%"
                    ref="multipleTableRef" @selection-change="handleSelectionChange">
                    <el-table-column :label="v" :prop="k" v-for="(v, k) in tableTitle" :key="k" align="center">
                    </el-table-column>
                    <el-table-column label="单位" prop="period" align="center">
                        <template #default="scope">
                            <template v-for="(v, k) in selectPeriod" :key="k">
                                <template v-if="scope.row.period == k">{{ v }}</template>
                            </template>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" align="center" width="240">
                        <template #default="scope">
                            <el-button size="small" @click="handleEdit(scope.row)">
                                <span>编辑</span>
                            </el-button>
                            <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">
                                <span>删除</span>
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-scrollbar>
        </div>
        <!-- 分页 -->
        <div class="page-container">
            <el-pagination v-model:current-page="cron_result.page" v-model:page-size="cron_result.page_size"
                :page-sizes="[20, 40, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="cron_result.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <!-- 添加定时任务 -->
    <!-- <el-drawer v-model="drawer" direction="rtl">
        <template #header>
            <h4>添加定时任务</h4>
        </template>
        <template #default>
            <div class="form-drawer">
                <div class="form-content">
                    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules"
                        label-width="auto" status-icon>
                        <el-row :gutter="20" style="margin:0px;">
                            <el-col :span="24">
                                <el-form-item prop="every" label="间隔">
                                    <el-input v-model.number="ruleForm.every" />
                                </el-form-item>
                            </el-col>
                            <el-col :span="24">
                                <el-form-item prop="period" label="单位">
                                    <el-select v-model="ruleForm.period">
                                        <el-option v-for="(v, k) in selectPeriod" :key="k" :label="v" :value="k" />
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
    </el-drawer> -->
    <!-- 修改设备弹窗 -->
    <!-- <el-dialog v-model="dialogTableVisible" title="修改定时任务信息" :width="600">
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
                        <el-button type="primary" @click="editDevice(ruleFormRef)">提交</el-button>
                    </el-form-item>
                </el-col>
            </el-row>

        </el-form>
    </el-dialog> -->

</template>
<script setup>
import { useCrontore } from '@/stores/cron/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
import { ElLoading } from 'element-plus'


const stores = useCrontore();
const { cron_result } = storeToRefs(stores);

const isData = computed(() => {
    return cron_result.value.data.length > 0 ? true : false;
})




// 抽屉
const drawer = ref(false)

// 表单
const ruleFormRef = ref()

const ruleForm = reactive({
    clocked_time: 1,
    period: "minutes",

})

const editForm = reactive({})

// 控制表单渲染
const ruleFields = {
    "every": "间隔",
    // "period": "单位"

}
const selectPeriod = ref({
    "microseconds": "毫秒",
    "seconds": "秒钟",
    "minutes": "分钟",
    "hours": "小时",
    "days": "天",

})

const rules = reactive({
    clocked_time: [{ required: true, message: '必填项', trigger: 'blur' },],
    period: [{ required: true, message: '必选项', trigger: 'blur' },],
})

// 添加表单
async function confirmClick(formEl) {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.addResult(ruleForm).then((res) => {
                // console.log(res);
                if (res) {
                    stores.getResult();
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
    stores.deleteResult(row.id).then(() => {
        ElMessage.success('删除成功')
        stores.getResult();
    })
}
const closeClick = () => {
    ruleFormRef.value.resetFields()
    dialogTableVisible.value = false
}

const editResult = async (formEl) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            stores.updateResult(editForm.id, editForm).then(() => {
                stores.getResult();
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
    cron_result.page_size = val
    stores.getResult();
    // loading.close()
}
const handleCurrentChange = (val) => {
    cron_result.page = val
    stores.getResult();
    // loading.close()
}
// 控制表格字段
const tableTitle = {
    "id": "ID",
    "every": "间隔",
    // "period": "单位"
}
// {
//     "id": 1,
//     "every": 30,
//     "period": "seconds"
// }

const periodField = computed(() => {
    return
})

function cancelClick() {
    drawer.value = false
}

onMounted(() => {
    stores.getResult()
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
