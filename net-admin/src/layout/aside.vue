<template>
    <div class="title">
        <span>net_devops管理系统</span>
    </div>
    <el-scrollbar style="height: calc(100vh - 60px);">
        <el-menu :default-openeds="['1', '3']" :router="true"  @open="handleOpen" @close="handleClose">
            <el-menu-item index="/">
                <el-icon>
                    <House />
                </el-icon>
                <span>首页</span>
            </el-menu-item>
            <el-sub-menu :index="item.path" v-for="item in r" :key="item.path">
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
import router from '@/router';

console.log(router.getRoutes());
let r = router.getRoutes().filter((item) => { if (item.children.length > 0 && item.path != '/') return item })
for (let i = 0; i < r.length; i++) {
    console.log(r[i]);
}
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}

const itemclick = (item) => {
    console.log(item);
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