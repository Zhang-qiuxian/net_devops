import axios from "axios"
//点击导出，导出数据表格
function exportTableAPI(url, data, params) {
    return axios({
        url: `${import.meta.env.VITE_API_URL}${url}`,
        method: "get",
        data: data,
        params: params,
        responseType: 'blob',
        headers: {
            'Content-Type': 'application/json'
        },
    })
}

export function exportExcel(url, data, params) {
    exportTableAPI(url, data, params).then(res => {
        let blob = new Blob([res.data]);
        //从response的headers中获取filename, 后端response.setHeader("Content-disposition", "attachment; filename=xxxx.docx") 设置的文件名;
        let contentDisposition = res.headers['content-disposition'];  
        let patt = new RegExp("filename=([^;]+\\.[^\\.;]+);*");
        let result = patt.exec(contentDisposition);
        let filename = result[1];
        let downloadElement = document.createElement('a');
        let href = window.URL.createObjectURL(blob); //创建下载的链接
        downloadElement.style.display = 'none';
        downloadElement.href = href;
        downloadElement.download = filename; //下载后文件名
        document.body.appendChild(downloadElement);
        downloadElement.click(); //点击下载
        document.body.removeChild(downloadElement); //下载完成移除元素
        window.URL.revokeObjectURL(href); //释放掉blob对象
    })
}


//用于导出excel表格
// export const exportExcel = ({ method = 'get', url, data = {}, fileName }) => {
//     const field = method === 'get' ? 'params' : 'data';
//     axios({
//         method,
//         url:`${import.meta.env.VITE_API_URL}${url}`,
//         [field]: data,
//         responseType: 'blob'
//     })
//         .then((res) => {
//             //导出接口失败 返回的也是blob type为application/json
//             if (res.data?.type === 'application/json') throw new Error();

//             const blob = new Blob([res.data], {
//                 type: 'application/vnd.ms-excel'
//             });
//             if ('download' in document.createElement('a')) {
//                 // 非IE浏览器下载
//                 // 创建a标签
//                 const link = document.createElement('a');
//                 // 规定下载的超链接
//                 link.setAttribute('download', `${fileName}.xlsx`);
//                 // 未点击前隐藏a链接
//                 link.style.display = 'none';
//                 // 创建URL对象，指向该文件url
//                 link.href = URL.createObjectURL(blob);
//                 // 将a标签添加到dom中
//                 document.body.append(link);
//                 // 触发a标签点击事件
//                 link.click();
//                 // 释放之前的URL对象
//                 URL.revokeObjectURL(link.href);
//                 // 从dom中移除该a链接
//                 document.body.removeChild(link);
//             } else {
//                 // IE10+ 下载
//                 navigator.msSaveBlob(blob, filename);
//             }
//             console.log('导出成功');
//         })
//         .catch(() => {
//             console.log('导出失败');
//         });
// };

// const downloadExcel = async (url) => {
//     try {
//         // 假设你的 API 端点是 '/api/export-excel'  
//         const response = await axios({
//             method: 'get',
//             url: `${import.meta.env.VITE_API_URL}${url}`,
//             responseType: 'blob', // 重要！告诉 axios 这是一个文件  
//         });

//         // 创建一个指向 Blob 对象的 URL  
//         const download_url = window.URL.createObjectURL(new Blob([response.data]));

//         // 创建一个 a 标签用于下载  
//         const link = document.createElement('a');
//         link.href = download_url;
//         // 设置文件名，假设后端没有设置 Content-Disposition 响应头  
//         link.setAttribute('download', 'exported-data.xlsx');

//         // 触发点击  
//         document.body.appendChild(link);
//         link.click();

//         // 清理  
//         window.URL.revokeObjectURL(download_url);
//         document.body.removeChild(link);
//     } catch (error) {
//         console.error('下载 Excel 文件时发生错误:', error);
//     }
// };  