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
                <d-button variant="solid" color="primary" @click="conter.increment()">新增</d-button>
                <d-button color="primary">导出为excel</d-button>
                {{ conter.count }}
            </div>
        </div>
        <div class="table">
            <d-table ref="tableRef" :data="data" :row-key="(item) => item.device_id" @cell-click="onCellClick"
                @row-click="onRowClick" @check-change="checkChange" @check-all-change="checkAllChange"
                table-height="100%" fix-header>
                <d-column type="checkable" width="40" :checkable="checkable" reserve-check></d-column>
                <d-column v-for="(v, k) in fileds" :field=k :header=v align="center"></d-column>
                <d-column header="操作" class="opera">
                    <template #default="scope">
                        <d-button @click="handleClick1(scope.row)" color="primary">编辑</d-button>
                        <d-button @click="handleClick1(scope.row)">详细</d-button>
                    </template>
                </d-column>
            </d-table>
        </div>
        <div class="page">
            <d-pagination :total="pager.total" v-model:pageSize="pager.pageSize" v-model:pageIndex="pager.pageIndex"
                :can-view-total="true" :can-change-page-size="true" :can-jump-page="true" :max-items="5" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { getDeice } from '@/api/device';
import { useCounterStore } from '@/stores/counter.js'

const conter = useCounterStore()

console.log("count:::::",conter.count);
console.log("count:::::",conter.count);



onMounted(() => {
    // getDeice()
    // useCounterStore().increment()

})

function test(params) {
    console.log(import.meta.env);
    let data = getDeice(params)
    console.log(data);
}

const handleClick1 = (row) => {
    console.log(row);
};
const selectOptions = reactive(['Options1', 'Options2', 'Options3']);
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
const data = ref([
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "8b77c2f9-f035-45e2-a513-09c56563950e",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "1F-switch",
        "ip": "10.10.10.1",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 08:42:35",
        "update_time": "2024-04-08 08:42:35"
    },
    {
        "device_id": "dce1b2ed-659c-4d30-83ee-f052580efdc5",
        "snmp": "px",
        "company": null,
        "name": "1F交换机",
        "description": "1F交换机",
        "hostname": "2F-switch",
        "ip": "10.10.10.2",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 09:03:32",
        "update_time": "2024-04-08 09:03:32"
    },
    {
        "device_id": "ac7a889d-1483-4ddb-994e-092c339a40d5",
        "snmp": "px",
        "company": null,
        "name": "3F交换机",
        "description": "3F交换机",
        "hostname": "3F-switch",
        "ip": "10.10.10.3",
        "login": "ssh",
        "url": "",
        "username": "admin",
        "password": "admin",
        "remark": "",
        "create_time": "2024-04-08 12:47:56",
        "update_time": "2024-04-08 12:47:56"
    }
]);

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

// console.log(fileds);

const pager = shallowReactive({
    total: 306,
    pageIndex: 5,
    pageSize: 10,
    pageSizeOptions: [10, 20, 30, 40, 50],
});

const preLink = '<span class="icon-arrow-left"></span>';
const nextLink = '<span class="icon-arrow-right"></span>';

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

const insertRow = () => {
    data.value.push({
        id: `${data.value.length}`,
        firstName: 'Jeff',
        lastName: 'You',
        gender: 'Male',
        date: '1989/05/19',
    });
};

const deleteRow = () => {
    data.value.splice(0, 1);
};

const onResizeStart = (e) => {
    console.log('resize start', e);
};

const onResizing = (e) => {
    console.log('resizing', e);
};

const onResizeEnd = (e) => {
    console.log('resize end', e);
};

</script>

<style lang="less" scoped>
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