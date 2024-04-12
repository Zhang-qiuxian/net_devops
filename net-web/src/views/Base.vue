<script setup>
import Aside from "@/views/Aside.vue";
import Header from "@/views/Header.vue";
import Main from "@/views/Main.vue";

</script>

<template>
  <d-layout>
    <d-aside class="daside">
      <Aside />
    </d-aside>
    <d-layout>
      <d-header class="dheader" style="flex:none">
        <Header />
      </d-header>
      <d-content class="main-content" style="min-height: 400px;">
        <Main />
      </d-content>
      <d-footer class="dfooter" style="line-height: 40px;">
        <span>@Zhang.qiuxian</span>
      </d-footer>
    </d-layout>
  </d-layout>
  <!-- <RouterView /> -->
</template>

<style lang="less">
.daside {
  background: #f8f8f8;
  width: 200px;
  //min-height: 200px;
  //display: flex;
  //align-items: center;
  //justify-content: center;
}

.dheader,
.dfooter {
  background: #333854;
  color: #fff;
  text-align: center;
  height: 40px;
}

.devui-layout__content {
  height: calc(100vh - 80px);
  text-align: center;
}

.main-content {
  padding: 10px;
}
</style>
