<template>
    <div class="main">
        <div class="form">
            <div class="form-left">
                <d-form :data="formModel" label-size="sm" label-align="align">
                    <d-row :gutter="16">
                        <d-col :span="7">
                            <d-form-item field="设备名" label="Name" help-tips="请输入设备名">
                                <d-input v-model="formModel.name" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="7">
                            <d-form-item field="select" label="Select">
                                <d-select v-model="formModel.select" :options="selectOptions" />
                            </d-form-item>
                        </d-col>
                    </d-row>
                </d-form>
            </div>
            <div class="form-right">
                <d-button variant="solid" color="primary" @click="test">新增</d-button>
                <d-button color="primary">导出为excel</d-button>
            </div>
        </div>
        <div class="table">
            <d-table ref="tableRef" :data="device" :row-key="(item) => item.device_id" @cell-click="onCellClick"
                @row-click="onRowClick" @check-change="checkChange" @check-all-change="checkAllChange"
                table-height="100%">

                <d-column type="index" width="40"></d-column>
                <d-column type="checkable" width="40" :checkable="checkable" reserve-check></d-column>
                <d-column v-for="(v, k) in fileds" :field=k :header=v align="center"></d-column>
                <d-column header="操作" class="opera">
                    <template #default="scope">
                        <d-button @click="handleClick1(scope.row)" color="primary">编辑</d-button>
                        <d-button @click="handleClick1(scope.row)">详细</d-button>
                    </template>
                </d-column>
                <template #empty>
                    <div style="text-align: center;">No Data</div>
                </template>
            </d-table>
        </div>
        <div class="page">
            <d-pagination :total="total" v-model:pageSize="pager.pageSize" v-model:pageIndex="pager.pageIndex"
                :can-view-total="true" :can-change-page-size="true" :auto-fix-page-index="false" :auto-hide="true"
                @page-index-change="pageIndexChange" @page-size-change="pageSizeChange" :max-items="5" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { getDeice } from '@/api/device';
import { useDeviceStore } from '@/stores/device.js'
import { storeToRefs } from 'pinia';

const store = useDeviceStore()

const { total, device } = storeToRefs(store)

const pager = shallowReactive({
    // total: total,
    pageIndex: 1,
    pageSize: 10,
    pageSizeOptions: [10, 20, 30, 40, 50],
});


onMounted(() => {
    // getDeice()
    // useCounterStore().increment()
    store.get({
        page: pager.pageIndex,
        page_size: pager.pageSize
    })
    console.log(store.total);


})

function test(params) {
    let data = getDeice(params)
    console.log(data);
}

const handleClick1 = (row) => {
    console.log(row);
};
let formModel = reactive({
    "name": '',
    "description": '',
    "hostname": '',
    "ip": '',
    "login": '',
    "username": '',
    "password": '',
    "url": '',
    "snmp": '',
    "snmp_id": 1,
    "company": '',
    "company_id": 1
});
const tableRef = ref();


const fileds = {
    // "device_id": "设备id",
    "name": "设备名",
    // "description": "设备描述",
    "hostname": "主机名",
    "ip": "设备ip",
    "login": "登录方式",
    "username": "账号",
    "password": "密码",
    "url": "网址",
    // "snmp": "snmp",
    // "company": "厂家",
    // "remark": "",
    // "create_time": "创建时间",
    // "update_time": "更新时间",

}


const handleClick = () => {
    console.log(tableRef.value.store.getCheckedRows());
};
const onCellClick = (params) => {
    console.log('cell-click', params);
};
const onRowClick = (params) => {
    console.log('row-click', params);
};

const checkChange = (checked, row, selection) => {
    console.log('checked row:', checked, row, selection);
};

const checkAllChange = (checked, selection) => {
    console.log('checked:', checked, selection);
};

const toggleRow = () => {
    tableRef.value.store.toggleRowSelection(data.value[0]);
};

const checkable = (row, rowIndex) => {
    return row.lastName === 'Li' || false;
};

const pageSizeChange = (val) => {
    pager.pageSize = val;
    console.log(pager);
    console.log("pageSize", val);
    store.get({
        page: pager.page,
        page_size: pager.pageSize
    })
};
const pageIndexChange = (val) => {
    console.log("index", val);
    pager.page
    store.get({
        page: pager.pageIndex,
        page_size: pager.pageSize
    })
};


</script>

<style lang="scss" scoped>
.main {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.form {
    height: 52px;
    display: flex;
    align-items: center;

    .devui-button {
        margin: 10px;
    }
}

.table {
    height: calc(100% - 84px);
}

.page {
    height: 32px;
}

::v-deep(.header-container) {
    justify-content: center;
}

.devui-table__cell>button {
    margin: 4px;

}
</style>