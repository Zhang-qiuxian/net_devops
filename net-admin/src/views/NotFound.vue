<template>
  <el-result icon="error" title="错误提示" sub-title="页面不存在或在开发中">
    <template #extra>
      <el-button type="primary" @click="goHome">返回主页</el-button>

    </template>
  </el-result>
</template>

<script setup>
import {useRouter} from 'vue-router'
const router = useRouter()
const goHome = () => {
  router.push('/')
}

</script>

<style scoped>
.el-result{
  height: 100%;
}
</style>
