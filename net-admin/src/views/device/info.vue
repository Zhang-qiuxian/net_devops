<template>
    <div class="container">
        <div class="from-container">
            <el-button type="success" @click="drawer2 = true">添加设备</el-button>
            <el-button type="info">导出设备</el-button>
        </div>
        <div class="table-container">
            <el-scrollbar>
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
                            <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
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
            <el-pagination v-model:current-page="pages.page" v-model:page-size="pages.page_size"
                :page-sizes="[15, 30, 50, 100]" layout="total, sizes, prev, pager, next, jumper"
                :total="device_info.total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>
    </div>
    <el-drawer v-model="drawer2" :direction="direction">
        <template #header>
            <h4>添加设备</h4>
        </template>
        <template #default>
            <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" :rules="rules" label-width="auto"
                :size="formSize" status-icon>
                <el-form-item label="Activity name" prop="name">
                    <el-input v-model="ruleForm.name" />
                </el-form-item>
                <el-form-item label="Activity zone" prop="region">
                    <el-select v-model="ruleForm.region" placeholder="Activity zone">
                        <el-option label="Zone one" value="shanghai" />
                        <el-option label="Zone two" value="beijing" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Activity count" prop="count">
                    <el-select-v2 v-model="ruleForm.count" placeholder="Activity count" :options="options" />
                </el-form-item>
                <el-form-item label="Activity time" required>
                    <el-col :span="11">
                        <el-form-item prop="date1">
                            <el-date-picker v-model="ruleForm.date1" type="date" label="Pick a date"
                                placeholder="Pick a date" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col class="text-center" :span="2">
                        <span class="text-gray-500">-</span>
                    </el-col>
                    <el-col :span="11">
                        <el-form-item prop="date2">
                            <el-time-picker v-model="ruleForm.date2" label="Pick a time" placeholder="Pick a time"
                                style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-form-item>
                <el-form-item label="Instant delivery" prop="delivery">
                    <el-switch v-model="ruleForm.delivery" />
                </el-form-item>
                <el-form-item label="Activity location" prop="location">
                    <el-segmented v-model="ruleForm.location" :options="locationOptions" />
                </el-form-item>
                <el-form-item label="Activity type" prop="type">
                    <el-checkbox-group v-model="ruleForm.type">
                        <el-checkbox value="Online activities" name="type">
                            Online activities
                        </el-checkbox>
                        <el-checkbox value="Promotion activities" name="type">
                            Promotion activities
                        </el-checkbox>
                        <el-checkbox value="Offline activities" name="type">
                            Offline activities
                        </el-checkbox>
                        <el-checkbox value="Simple brand exposure" name="type">
                            Simple brand exposure
                        </el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
                <el-form-item label="Resources" prop="resource">
                    <el-radio-group v-model="ruleForm.resource">
                        <el-radio value="Sponsorship">Sponsorship</el-radio>
                        <el-radio value="Venue">Venue</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="Activity form" prop="desc">
                    <el-input v-model="ruleForm.desc" type="textarea" />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(ruleFormRef)">
                        Create
                    </el-button>
                    <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
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


const stores = useDeviceStore();
const { device_info, pages } = storeToRefs(stores);

const handleEdit = (index, row) => {
    console.log(index, row)
}
const handleDelete = (index, row) => {
    console.log(index, row)
}
// 处理分页
const handleSizeChange = (val) => {
    pages.page_size = val
    stores.getDeviceInfo();
}
const handleCurrentChange = (val) => {
    pages.page = val
    stores.getDeviceInfo();
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
// 抽屉
const drawer2 = ref(false)
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
    drawer2.value = false
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
    region: '',
    count: '',
    date1: '',
    date2: '',
    delivery: false,
    location: '',
    type: [],
    resource: '',
    desc: '',
})
const locationOptions = ['Home', 'Company', 'School']

const rules = reactive({
    name: [
        { required: true, message: 'Please input Activity name', trigger: 'blur' },
        { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
    ],
    region: [
        {
            required: true,
            message: 'Please select Activity zone',
            trigger: 'change',
        },
    ],
    count: [
        {
            required: true,
            message: 'Please select Activity count',
            trigger: 'change',
        },
    ],
    date1: [
        {
            type: 'date',
            required: true,
            message: 'Please pick a date',
            trigger: 'change',
        },
    ],
    date2: [
        {
            type: 'date',
            required: true,
            message: 'Please pick a time',
            trigger: 'change',
        },
    ],
    location: [
        {
            required: true,
            message: 'Please select a location',
            trigger: 'change',
        },
    ],
    type: [
        {
            type: 'array',
            required: true,
            message: 'Please select at least one activity type',
            trigger: 'change',
        },
    ],
    resource: [
        {
            required: true,
            message: 'Please select activity resource',
            trigger: 'change',
        },
    ],
    desc: [
        { required: true, message: 'Please input activity form', trigger: 'blur' },
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
    stores.getDeviceInfo();
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
    padding: 10px 20px 0 20px;
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
