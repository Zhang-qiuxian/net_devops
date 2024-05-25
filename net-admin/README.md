# net-admin

net_devops的前端项目

## 建议的IDE设置

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## 安装/设置
首先将项目克隆到本地（如果已经克隆了就忽略），代码的目录如图
```shell
git clone https://gitee.com/Zhangqiuxian/net_devops.git
```
```md
── net_devops
    ├── 架构图.drawio
    ├── django_server
    ├── install.sh
    ├── net-admin
    ├── net-web
    └── README.md
```
环境要求 服务器上要安装 nodejs 如果npm 下载慢，可以使用淘宝镜像

```sh
 pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
```

修改`.env`文件中的IP地址为你的服务器IP地址
```sh
VITE_API_URL=http://127.0.0.1:8000/api/v1/
```
### 安装依赖
```sh
cd net-admin/
yarn
```
### 运行项目

```sh
yarn dev --host=服务器IP
```

### 编译项目
在编译项目时需要修改`.env`文件中的ip地址

```sh
VITE_API_URL=http://127.0.0.1:8000/api/v1/
```

为你的后端地址，不然前端页面请求会报错

```sh
yarn build
```
