<template>
  <div class="tietle">
    <span>网络devops后台</span>
  </div>
  <d-menu mode="vertical" :default-select-keys="['home']" width="200px">
    <d-menu-item key="home">
      <template #icon>
        <i class="icon-homepage"></i>
      </template>
      <span>首页</span>
    </d-menu-item>
    <d-sub-menu title="控制台" key="console">
      <template #icon>
        <i class="icon-deploy-store"></i>
      </template>
      <d-menu-item key="setting-item">
        <span>Setting item</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="定时任务" key="cron">
      <template #icon>
        <i class="icon-date"></i>
      </template>
      <d-menu-item key="setting-item">
        <span>Setting item</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="设备管理" key="device">
      <template #icon>
        <i class="icon-clearup"></i>
      </template>
      <d-menu-item key="setting-item">
        <span>Setting item</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="IP管理" key="ip">
      <template #icon>
        <i class="icon-version-history  "></i>
      </template>
      <d-menu-item key="setting-item">
        <span>Setting item</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="Setting" key="setting">
      <template #icon>
        <i class="icon-setting"></i>
      </template>
      <d-menu-item key="setting-item">
        <span>Setting item</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="系统管理" key="system">
      <template #icon>
        <i class="icon-system"></i>
      </template>
      <d-menu-item key="system-item">
        <span>System item</span>
      </d-menu-item>
    </d-sub-menu>
  </d-menu>
</template>

<script setup>
import { ref } from 'vue';

</script>

<style lang="less" scoped>
.tietle {
  height: 39px;
  line-height: 39px;
  text-align: center;
  font-size: 14px;
  border-bottom: #333854 1px solid;
}
</style>