<template>
    <el-container class="layout-container">
        <el-aside width="200px">
            <Aside />
        </el-aside>
        <el-container>
            <el-header style="text-align: right; font-size: 12px">
                <Header />
            </el-header>
            <el-main>
                <!-- <div class="main-content"> -->
                <!-- </div> -->
                <RouterView />
            </el-main>
        </el-container>
    </el-container>
</template>

<script setup>
import { ref } from 'vue'
// import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'
import Aside from './aside.vue'
import Header from './header.vue'




const item = {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))
</script>

<style>
.layout-container .el-header {
    position: relative;
    background-color: var(--el-color-primary-light-7);
    color: var(--el-text-color-primary);
}

.layout-container .el-aside {
    color: var(--el-text-color-primary);
    background: var(--el-color-primary-light-8);
    border-right: solid 1px var(--el-color-info-light-7);
}

.layout-container .el-menu {
    border-right: none;
}

.layout-container .el-main {
    padding: 0;
    /* height: calc(100vh - 60px); */
}

/* .layout-container .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
}

.layout-container .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
} */

/* .main-content{
    height: calc(100vh - 60px);
} */
</style>