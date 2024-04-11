import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// devui


// import { ThemeServiceInit, infinityTheme } from 'devui-theme';

// ThemeServiceInit({ infinityTheme }, 'infinityTheme');

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
