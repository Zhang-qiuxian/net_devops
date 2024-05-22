#!/bin/bash

PASSWORD=$1

PYTHON_VERSION='Python-3.12.3'
NODEJS_VERSION='node-v22.2.0'

SOFTWARE_DIR="/opt/software"
PYTHON="https://mirrors.huaweicloud.com/python/3.12.3/$PYTHON_VERSION.tar.xz"
NODEJS="https://mirrors.huaweicloud.com/nodejs/v22.2.0/$NODEJS_VERSION-linux-x64.tar.xz"
# PYTHON="https://mirrors.huaweicloud.com/python/3.12.3/Python-3.12.3.tar.xz"

PWD_FILES=$(pwd)

DJANGO='django_server'
VUE='net-admin'

function mkdir_files() 
{
    echo "创建文件夹"
    echo $PASSWORD | sudo -S mkdir -p $SOFTWARE_DIR
    return 0
}

function download_package() 
{
    # 安装Python
    wget -O $SOFTWARE_DIR/$PYTHON_VERSION $PYTHON
    tar -xvf Python-3.12.3.tar.xz
    cd Python-3.12.3
    ./configure --prefix=/usr/local/python3
    make && make install
    cd ..
    rm -rf Python-3.12.3*

    # 安装Node.js
    wget $NODEJS
    tar -xvf node-v22.2.0-linux-x64.tar.xz
    mv node-v22.2.0-linux-x64 /usr/local/nodejs
    ln -s /usr/local/nodejs/bin/node /usr/local/bin/node
    ln -s /usr/local/nodejs/bin/npm /usr/local/bin/npm
}

function install_nodejs()
{
    echo '安装Node.js'
    sudo wget -O $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64.tar.xz $NODEJS
    sudo tar -xvf $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64.tar.xz -C $SOFTWARE_DIR
    # sudo mv node-v22.2.0-linux-x64 /usr/local/nodejs
    # sudo ln -s /usr/local/nodejs/bin/node /usr/local/bin/node
}

function start_django()
{
    echo "开始创建django"
}

function install_python() 
{
    # 安装Python
    echo '开始安装Python'

    sudo wget -O $SOFTWARE_DIR/$PYTHON_VERSION.tar.xz $PYTHON
    sudo tar -xvf $SOFTWARE_DIR/$PYTHON_VERSION.tar.xz -C $SOFTWARE_DIR
    # 安装Python依赖包
    # pip3 install -r requirements.txt
}

function hash_python_version(){
    v=$(python3 -V | awk  '{print $2}' | awk -F '.' '{print $2}')
    if [ $v -le 10 ]
    then
        echo "当前Python版本$v,需要升级Python版本"
        install_python
    else
        echo "大于10,开始安装django虚拟环境"
    fi
}



function main() {
    
    # download_package
    # install_package
    
    echo $PASSWORD
    mkdir_files
    start_django
    # install_python
    # install_nodejs
    # if [ "$ROOT" != "root" ]; then
    #     echo "请使用root用户运行"
    #     echo $ROOT
    # fi

}

main

# function download_package() {
#     # 安装MariaDB
#     sudo apt-get install -y mariadb-server
# }

# # 更新系统软件包
# sudo apt-get update

# # 安装必要的依赖包
# sudo apt-get install -y mariadb-server

# # 启动mariadb服务
# sudo systemctl start mariadb

# # 设置mariadb服务开机自启动
# sudo systemctl enable mariadb

# # 输出mariadb版本
# sudo mysql -V
