import path from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { DevUiResolver } from 'unplugin-vue-components/resolvers'
import AutoImport from 'unplugin-auto-import/vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // 新增
    Components({
      resolvers: [
        DevUiResolver()
      ]
    }),
    AutoImport({
      dts: true,
      imports: ["vue", "vue-router"],
    }),

  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname,'src')
    }
  }
})
