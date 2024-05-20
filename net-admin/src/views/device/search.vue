<template>
    <div class="search-main">
        <el-card shadow="hover">
            <template #header>
                <div class="card-header">
                    <div class="search-form">
                        <el-form ref="formRef" :model="searchForm" :inline="true" label-width="auto" size="large"
                            status-icon>
                            <el-form-item label="查找IP地址" prop="ipNetToMediaNetAddress">
                                <el-input v-model="searchForm.ipNetToMediaNetAddress" placeholder="请输入IP地址" />
                            </el-form-item>
                            <el-form-item label="查找MAC地址" prop="ipNetToMediaPhysAddress">
                                <el-input v-model="searchForm.ipNetToMediaPhysAddress" placeholder="格式:xx:xx:xx:xx,请输入MAC地址" />
                            </el-form-item>
                            <el-form-item>
                                <!-- <el-button type="primary" @click="submitForm(formRef)">查询</el-button> -->
                                <el-button type="danger" @click="resetForm(formRef)">重置</el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                    <div class="total-status">
                        <el-statistic title="共搜索到" :value="total">
                            <template #suffix>
                                <el-icon style="vertical-align: -0.125em">
                                    <Platform />
                                </el-icon>
                            </template>
                        </el-statistic>
                    </div>

                </div>

            </template>
            <el-empty description="没有数据，请先添加设备" v-if="!isData" style="height: 100%;" />
            <el-table v-else :data="searchData" border table-layout="auto" style="width: 100%">
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
        </el-card>
    </div>
</template>
<script setup>

import { onMounted, ref, computed, reactive, watch } from 'vue'
import { searchArpApi } from '@/api/device/index.js'





const formRef = ref()
const resetForm = (formEl) => {
    if (!formEl) return
    formEl.resetFields()
}

const searchData = ref([])
const total = ref(0)

const searchForm = reactive({
    ipNetToMediaNetAddress: '',
    ipNetToMediaPhysAddress: '',
})

const isData = computed(() => {
    return searchData.value.length > 0 ? true : false;
})
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

watch(searchForm, (newVal, oldVal) => {
    if (newVal.ipNetToMediaNetAddress != '') {
        searchData.value = searchArpApi({ search: newVal.ipNetToMediaNetAddress }).then(res => {
            searchData.value = res.data
            total.value = res.total
        })
    } else if (newVal.ipNetToMediaPhysAddress != '') {
        searchData.value = searchArpApi({ search: newVal.ipNetToMediaPhysAddress }).then(res => {
            searchData.value = res.data
            total.value = res.total
        })
    } else {
        searchData.value = []
        total.value = 0
    }
})



</script>
<style lang="scss" scoped>
.search-main {
    // height: 100%;
    // width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.el-card {
    height: 100%;
    width: 100%;
}



.text {
    font-size: 14px;
}

.card-header {
    display: flex;
    justify-content: space-evenly;
}
</style>