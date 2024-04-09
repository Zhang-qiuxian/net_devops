<script setup>
// import { RouterLink, RouterView } from 'vue-router'
// import '@devui-design/icons'
</script>

<template>
  <h1>Hello</h1>
  <d-button>确定</d-button>
  <d-button variant="solid" color="primary">
    Primary
  </d-button>
  <d-button color="primary">
    Primary
  </d-button>
  <d-button variant="text" color="primary">
    Primary
  </d-button>

  <div class="demo-spacing">
    <d-button variant="solid" color="secondary">
      Secondary
    </d-button>
    <d-button color="secondary">
      Secondary
    </d-button>
    <d-button variant="text" color="secondary">
      Secondary
    </d-button>
  </div>

  <div class="demo-spacing">
    <d-button variant="solid" color="danger">
      Danger
    </d-button>
    <d-button color="danger">
      Danger
    </d-button>
    <d-button variant="text" color="danger">
      Danger
    </d-button>
  </div>
  <div>
    <d-icon name="setting" operable>
      <template #prefix>
        <span>设置</span>
      </template>
    </d-icon>
    <br />
    <br />
    <d-icon name="setting" operable>
      <template #suffix>
        <span>设置</span>
      </template>
    </d-icon>
    <br />
    <br />
    <d-icon name="https://devui.design/components/assets/logo.svg" size="16px" operable>
      <template #suffix>
        <span>Logo</span>
      </template>
    </d-icon>
    <br />
    <br />
    <d-icon name="refresh" rotate="infinite" operable>
      <template #suffix>
        <span>运行中</span>
      </template>
    </d-icon>
    <br />
    <br />
    <d-icon name="edit" :rotate="180">
      <template #suffix>
        <span>编辑</span>
      </template>
    </d-icon>
    <br />
    <br />
    <d-icon name="edit" disabled>
      <template #suffix>
        <span>无权编辑</span>
      </template>
    </d-icon>
  </div>
  <!-- <RouterView /> -->
</template>

<style scoped></style>
