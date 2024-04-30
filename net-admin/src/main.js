import { createApp } from 'vue'
import pinia from '@/stores/index.js'

import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'normalize.css'
import '@/assets/main.css'

const app = createApp(App)


// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(pinia)
app.use(router)


app.mount('#app')
