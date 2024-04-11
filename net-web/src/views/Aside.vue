<template>
  <div class="tietle">
    <span>网络devops后台</span>
  </div>
  <d-menu mode="vertical" :default-select-keys="['home']" width="200px" :router="true">
    <d-menu-item key="home" :route="{ path: '/' }">
      <template #icon>
        <i class="icon-homepage"></i>
      </template>
      <span>首页</span>
    </d-menu-item>
    <d-sub-menu title="控制台" key="console" >
      <template #icon>
        <i class="icon-deploy-store"></i>
      </template>
      <d-menu-item key="console-info" :route="{ name: 'console-info' }">
        <span>控制面板</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="定时任务" key="cron">
      <template #icon>
        <i class="icon-date"></i>
      </template>
      <d-menu-item key="cron-info" :route="{ name: 'cron-info' }">
        <span>定时任务详情</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="设备管理" key="device">
      <template #icon>
        <i class="icon-clearup"></i>
      </template>
      <d-menu-item key="device-info" :route="{ name: 'device-info' }">
        <span>设备信息</span>
      </d-menu-item>
    </d-sub-menu>
    <d-sub-menu title="IP管理" key="ipam">
      <template #icon>
        <i class="icon-version-history  "></i>
      </template>
      <d-menu-item key="ipam-info" :route="{ name: 'ipam-info' }">
        <span>网段信息</span>
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