<template>
    <div class="title">
        <span>net_devops管理系统</span>
    </div>
    <el-scrollbar style="height: calc(100vh - 60px);">
        <el-menu :default-openeds="['1', '3']">
            <el-menu-item index="2">
                <el-icon><House /></el-icon>
                <span>首页</span>
            </el-menu-item>
            <el-sub-menu index="1">
                <template #title>
                    <el-icon><message /></el-icon>
                    <span>Navigator One</span>
                </template>
                <el-menu-item index="1-1">Option 1</el-menu-item>
                <el-menu-item index="1-2">Option 2</el-menu-item>
            </el-sub-menu>
            <el-sub-menu index="2">
                <template #title>
                    <el-icon><icon-menu /></el-icon>Navigator Two
                </template>
                <el-menu-item index="2-1">Option 1</el-menu-item>
                <el-menu-item index="2-2">Option 2</el-menu-item>
                <el-menu-item index="2-3">Option 3</el-menu-item>
                <el-sub-menu index="2-4">
                    <template #title>Option 4</template>
                    <el-menu-item index="2-4-1">Option 4-1</el-menu-item>
                </el-sub-menu>
            </el-sub-menu>
        </el-menu>
    </el-scrollbar>
</template>

<script setup>
import { Menu as IconMenu} from '@element-plus/icons-vue' 

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