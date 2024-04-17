<template>
    <div class="main">
        <div class="form">
            <d-button variant="solid" color="primary" @click="handleAdd">新增</d-button>
            <d-modal v-model="visible" title="添加厂商">
                <d-form ref="formRef" layout="vertical" :data="fromdata" :rules="rules" :pop-position="['right']">
                    <d-form-item v-for="(v, k) in fileds" :field=k :show-feedback="false" :label=v>
                        <d-input v-model="fromdata[k]" />
                    </d-form-item>
                    <d-button variant="solid" style="width: 100%;">提交</d-button>
                </d-form>
            </d-modal>
        </div>
        <div class="table">
            <d-table ref="tableRef" :data="data" :row-key="(item) => item.id" @check-change="checkChange"
                @check-all-change="checkAllChange" table-layout='fixed' table-height="100%" fix-header
                style="width: 100%">
                <d-column type="checkable" width="40" reserve-check></d-column>
                <d-column v-for="(v, k) in fileds" :field=k :header=v></d-column>
                <d-column header="操作">
                    <template #default="scope">
                        <d-button @click="handleEdit(scope.row)">编辑</d-button>
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


onMounted(() => {
    // getDeice()
    // console.log();

})


const rules = {
    code: [{ required: true, message: '厂家代码不能为空', trigger: 'blur' }],
    name: [{ required: true, message: '厂家信息不能为空', trigger: 'blur' }],
    model: [{ required: true, message: '设备型号不能为空', trigger: 'blur' }],
};

const visible = ref(false);
const fromdata = ref({
    "code": "huawei",
    "name": "华为",
    "model": "S5700"
});
const defaultSnmp = {
    "code": "huawei",
    "name": "华为",
    "model": "S5700"
}

const handleAdd = () => {
    visible.value = true;
    fromdata.value = defaultSnmp
};


const handleEdit = (row) => {
    console.log(row);
    fromdata.value = row
    visible.value = !visible.value
};



const tableRef = ref();
const data = ref([
    {
        "code": "huawei",
        "name": "华为",
        "model": "S5700"
    }
])

const fileds = {
    // "id": 2,
    "code": "厂家代码(英文名)",
    "name": "厂家名称",
    "model": "设备型号"

}


const pager = shallowReactive({
    total: 306,
    pageIndex: 5,
    pageSize: 10,
    pageSizeOptions: [10, 20, 30, 40, 50],
});

const preLink = '<span class="icon-arrow-left"></span>';
const nextLink = '<span class="icon-arrow-right"></span>';


const checkChange = (checked, row, selection) => {
    console.log('checked row:', checked, row, selection);
};

const checkAllChange = (checked, selection) => {
    console.log('checked:', checked, selection);
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
</style>