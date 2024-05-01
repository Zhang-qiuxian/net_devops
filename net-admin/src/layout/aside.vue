<template>
    <div class="title">
        <span>{{ title }}</span>
    </div>
    <el-scrollbar style="height: calc(100vh - 60px);">
        <el-menu :default-active="default_active" :router="true">
            <el-menu-item index="/" @click="itemclick">
                <el-icon>
                    <House />
                </el-icon>
                <span>首页</span>
            </el-menu-item>
            <el-sub-menu :index="item.path" v-for="item in routers" :key="item.path">
                <template #title>
                    <el-icon>
                        <component :is="item.meta.icon"></component>
                    </el-icon>
                    <span>{{ item.meta.title }}</span>
                </template>
                <el-menu-item :index="item2.path" v-for="item2 in item.children" :key="item2.name"
                    :route="{ name: item2.name }" @click="itemclick">
                    {{ item2.meta.title }}
                </el-menu-item>
            </el-sub-menu>
        </el-menu>
    </el-scrollbar>
</template>

<script setup>
import { Menu as IconMenu } from '@element-plus/icons-vue'
import { useSettingsStore } from '@/stores/settings.js'
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const settingsStore = useSettingsStore()
const { routers, default_active } = storeToRefs(settingsStore)
const title = import.meta.env.VITE_APP_TITLE;

onMounted(() => {
    useSettingsStore().addRouter()
})

const itemclick = (item) => {
    settingsStore.setDefaultActive(item.index)
}
</script>

<style lang="scss" scoped>
.title {
    width: 100%;
    height: 60px;
    background-color: #333;
    color: #fff;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
}
</style>