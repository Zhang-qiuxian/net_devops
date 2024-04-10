import axios from 'axios';
import { MessageBox } from 'element-ui'; // 如果你使用 Element UI，可以添加提示框  
import store from '@/stores'; // 如果你使用 Vuex，可以添加状态管理  

// 创建 axios 实例  
const service = axios.create({
    baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url  
    // 当发送跨域请求时携带凭证信息（cookies）  
    withCredentials: true,
    timeout: 5000 // 请求超时时间  
});

// 请求拦截器  
service.interceptors.request.use(
    config => {
        // 在发送请求之前做些什么，例如添加 token 到 headers  
        const token = store.getters.token;
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        // 对请求错误做些什么  
        console.log(error); // for debug  
        return Promise.reject(error);
    }
);

// 响应拦截器  
service.interceptors.response.use(
    response => {
        // 对响应数据做点什么，例如根据状态码判断登录状态  
        const res = response.data;
        if (res.code !== 200) {
            MessageBox.error(res.message || 'Error');
            return Promise.reject(new Error(res.message || 'Error'));
        } else {
            return res;
        }
    },
    error => {
        // 对响应错误做点什么，例如网络错误提示  
        if (error.response.status === 401) {
            // 未授权，跳转到登录页面  
            store.dispatch('FedLogOut').then(() => {
                location.reload(); // 为了重新实例化vue-router对象 避免bug  
            });
        } else {
            MessageBox.error(error.message);
            return Promise.reject(error);
        }
    }
);

export default service;