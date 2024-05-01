<template>
    <div>
        <h1>设备管理</h1>
    </div>
</template>
<script setup>
import { useDeviceStore } from '@/stores/device/index.js';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue'


const deviceStore = useDeviceStore();
const { device_info, devcie_snmp, page, } = storeToRefs(deviceStore);

onMounted(() => {
    deviceStore.getDeviceInfo();
    // deviceStore.getDeviceSnmp();
})


</script>
