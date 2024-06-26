import axios from 'axios';
import { Message } from 'vue-devui';
URL = import.meta.env.VITE_APP_BASE_API

const instance = axios.create({
    baseURL: URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// 添加请求拦截器
instance.interceptors.request.use(
    (config) => {
        // 在发送请求之前做些什么 token
        // if (Session.get('token')) {
        //     config.headers['Authorization'] = `${Session.get('token')}`;
        // }
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);

// 添加响应拦截器
instance.interceptors.response.use(
    (response) => {
        // 对响应数据做点什么
        const res = response.data;
        if (res.code && res.code !== 0) {
            // `token` 过期或者账号已在别处登录
            if (res.code === 401) {
                window.location.href = '/'; // 去登录页
                Message({
                    type: 'error',
                    message: '你已被登出，请重新登录'
                });
                // ElMessageBox.alert('你已被登出，请重新登录', '提示', {})
                //     .then(() => { })
                //     .catch(() => { });
            }
            return Promise.reject(service.interceptors.response);
        } else {
            return res;
        }
    },
    (error) => {
        // 对响应错误做点什么
        if (error.message.indexOf('timeout') != -1) {
            Message({ type: 'error', message: '网络超时' });
            // ElMessage.error('网络超时');
        } else if (error.message == 'Network Error') {
            Message({ type: 'error', message: '网络超时' });
            // ElMessage.error('网络连接错误');
        } else {
            // if (error.response.data) this.$message({ type: 'error', message: '接口路径找不到' });
            // // else ElMessage.error('接口路径找不到');
            // else this.$message({ type: 'error', message: '接口路径找不到' });
        }
        return Promise.reject(error);
    }
);


export default instance