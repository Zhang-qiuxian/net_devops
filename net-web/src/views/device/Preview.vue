<template>
  <d-row wrap="true" :gutter="10" align="middle" justify="center">
    <d-col :lg="6" :xs="24" v-if="true">
        <d-result icon="info" title="暂无数据" desc="请等待snmp同步！"></d-result>
      </d-col>
    <d-col :span="8" v-for="i in 32" v-if="false">
      <d-card>
        <template #content> never{{ i }} </template>
      </d-card>
    </d-col>
  </d-row>
</template>

<script setup>
import { computed } from 'vue';

</script>

<style lang="less" scoped>
.devui-row {
  height: 100%;
  overflow: auto;
}

.card-container {
  height: 100px;
  margin: 5px;
}
</style>