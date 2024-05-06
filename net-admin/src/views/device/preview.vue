<template>
    <el-empty description="没有数据，请先添加设备" v-if="!isData" style="height: 100%;"/>
    <el-scrollbar v-else>
        <el-row :gutter="20">
            <el-col :span="6" v-for="d in data" :key="d.device_id">
                <el-card  shadow="hover">
                    <template #header>
                        <div class="card-header">
                            <span>{{ d.name }}</span>
                        </div>
                    </template>
                    <!-- <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p> -->
                    <!-- <template #footer>Footer content</template> -->
                    {{ d.system[0].sysName }}
                </el-card>
            </el-col>
        </el-row>
    </el-scrollbar>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted, ref, computed, reactive } from 'vue'
const stores = useDeviceStore();
const { device_info, pages } = storeToRefs(stores);
console.log(device_info.value.data);

const data = device_info.value.data;

const isData = computed(() => {
    return data.length > 0 ? true : false;
})

onMounted(() => {
    stores.getDeviceInfo();
})


</script>
<style lang="scss" scoped>
.el-row {
    margin-left: 0 !important;
    margin-right: 0px !important;

    .el-col {
        margin-top: 10px;
    }
}
</style>