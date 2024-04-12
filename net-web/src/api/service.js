import axios from 'axios';

URL = import.meta.env.VITE_APP_BASE_API

const instance = axios.create({
    baseURL: URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.request.use(
    (config) => {
        // 在发送请求之前做些什么
        // 添加请求头等操作
        return config;
    },
    (error) => {
        // 对请求错误做些什么
        return Promise.reject(error);
    }
);

instance.interceptors.response.use(
    (response) => {
        // 对响应数据做些什么
        // 统一处理响应数据等操作
        console.log(response);
        if (response.data.code === 200) {
            return response.data.data;
        }else {
            return response.data
        }
        
    },
    (error) => {
        console.log(error);
        // 对响应错误做些什么
        // 统一处理错误等操作
        return Promise.reject(error);
    }
);

export default instance