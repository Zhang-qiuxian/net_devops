<template>
    <div class="main">
        <div class="form">
            <d-button variant="solid" color="primary" @click="handleAdd">新增</d-button>
            <d-modal v-model="visible" title="添加SNMP模板">
                <d-form ref="formRef" layout="vertical" :data="fromdata" :rules="rules" :pop-position="['right']">
                    <d-row :gutter="16">
                        <d-col :span="8">
                            <d-form-item field="name" :show-feedback="false" label="模板名">
                                <d-input v-model="fromdata.name" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="select" label="版本">
                                <d-select v-model="fromdata.version" :options="selecVersion" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="community" :show-feedback="false" label="团体字">
                                <d-input v-model="fromdata.community" />
                            </d-form-item>
                        </d-col>
                    </d-row>
                    <d-row :gutter="16">

                        <d-col :span="8">
                            <d-form-item field="username" label="用户名">
                                <d-input v-model="fromdata.username" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="password" :show-feedback="false" label="密码">
                                <d-input v-model="fromdata.password" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="auth_protocol" label="认证协议">
                                <d-input v-model="fromdata.auth_protocol" />
                            </d-form-item>
                        </d-col>
                    </d-row>
                    <d-row :gutter="16">
                        <d-col :span="8">
                            <d-form-item field="security_level" :show-feedback="false" label="安全级别">
                                <d-input v-model="fromdata.security_level" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="privacy_protocol" label="私有协议">
                                <d-input v-model="fromdata.privacy_protocol" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-form-item field="privacy_password" label="私有协议密码">
                                <d-input v-model="fromdata.privacy_password" />
                            </d-form-item>
                        </d-col>
                    </d-row>
                    <d-row :gutter="16" style="display: flex;align-items: center;">
                        <d-col :span="16">
                            <d-form-item field="context" :show-feedback="false" label="上下文">
                                <d-input v-model="fromdata.context" />
                            </d-form-item>
                        </d-col>
                        <d-col :span="8">
                            <d-button variant="solid">提交</d-button>
                        </d-col>
                    </d-row>
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

const selecVersion = reactive([1, 2, 3]);


const rules = {
    name: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
    community: [{ required: true, message: '用户信息不能为空', trigger: 'blur' }],
    select: [{ required: true, message: '请选择', trigger: 'change' }],
};

const visible = ref(false);
const fromdata = ref({
    "name": "default",
    "version": 2,
    "community": "public",
    "username": "user",
    "password": "pass",
    "auth_protocol": "MD5",
    "security_level": "noAuthNoPriv",
    "privacy_protocol": "DES",
    "privacy_password": "otherPass",
    "context": "context"
});
const defaultSnmp = {
    "name": "default",
    "version": 2,
    "community": "public",
    "username": "user",
    "password": "pass",
    "auth_protocol": "MD5",
    "security_level": "noAuthNoPriv",
    "privacy_protocol": "DES",
    "privacy_password": "otherPass",
    "context": "context"
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

let formModel = reactive({
    "id": 2,
    "name": "v2c",
    "version": 2,
    "community": "public",
    "username": "",
    "password": "",
    "auth_protocol": "",
    "security_level": "",
    "privacy_protocol": "",
    "privacy_password": "",
    "context": ""
});

const tableRef = ref();
const data = ref([
    {
        "id": 2,
        "name": "v2c",
        "version": 2,
        "community": "public",
        "username": "",
        "password": "",
        "auth_protocol": "",
        "security_level": "",
        "privacy_protocol": "",
        "privacy_password": "",
        "context": ""
    }
])

const fileds = {
    // "id": 2,
    "name": "模板名",
    "version": "版本",
    "community": "团体字",
    "username": "用户名",
    "password": "密码",
    "auth_protocol": "认证协议",
    "security_level": "认证等级",
    "privacy_protocol": "私有协议",
    "privacy_password": "私有密码",
    "context": "上下文"

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