#!/bin/bash

PASSWORD=$1
PWD_FILES=$(pwd)
IP=$(hostname -I | awk '{print $1}')
MIRRORS_FILE='/etc/apt/sources.list'

PYTHON_VERSION='Python-3.12.3'
NODEJS_VERSION='node-v22.2.0'

SOFTWARE_DIR="/opt/software"
PYTHON="https://mirrors.huaweicloud.com/python/3.12.3/$PYTHON_VERSION.tar.xz"
NODEJS="https://mirrors.huaweicloud.com/nodejs/v22.2.0/$NODEJS_VERSION-linux-x64.tar.xz"

DJANGO='django_server'
VUE='net-admin'
VENV='venv/venv'

function mkdir_files() {
    echo "创建文件夹"
    echo $PASSWORD | sudo -S mkdir -p $SOFTWARE_DIR
    return 0
}

function start_django() {
    # 启动django项目
    echo "开始创建django"
    cd $PWD_FILES
    echo 当前目录：$PWD_FILES
    python -m venv venv
    venv/bin/pip install -r $DJANGO/requirements.txt
    venv/bin/python $DJANGO/manage.py makemigrations && venv/bin/python $DJANGO/manage.py migrate
    nohup venv/bin/python $DJANGO/manage.py runserver $IP:8000 >django_run.log 2>&1 &
    echo "django已启动，请在浏览器中打开 http://$IP:8000/swagger 查看是否启动成功。日志文件在当前目录下的 django_run.log 文件中。"
}

function start_celery() { # 启动celery服务
    cd $DJANGO
    echo "开始启动Celery后台定时任务"
    nohup $PWD_FILES/venv/bin/celery -A django_server beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler >celery_beat_run.log 2>&1 &
    echo "celery定时任务已启动，日志文件在当前目录下的 celery_beat_run.log 文件中。"
    echo "开始启动Celery服务"
    nohup $PWD_FILES/venv/bin/celery -A django_server worker -l INFO >celery_worker_run.log 2>&1 &
    echo "celery已启动，日志文件在当前目录下的 celery_worker_run.log 文件中。"
}

function start_vue() { # 启动前端vue项目
    echo "开始启动前端"
    cd $PWD_FILES/$VUE
    sed -i 's/127.0.0.1/'$IP'/g' .env
    yarn
    yarn dev --host=$IP >net-admin.log 2>&1 &
    echo "vue已启动，请在浏览器中打开 http://$IP:5173 查看是否启动成功。日志文件在当前目录下的 vue_run.log 文件中。"
}

function install_nodejs() {
    echo '安装Node.js'
    echo $PASSWORD | sudo -S wget -O $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64.tar.xz $NODEJS
    echo $PASSWORD | sudo -S tar -xvf $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64.tar.xz -C $SOFTWARE_DIR
    # sudo mv node-v22.2.0-linux-x64 /usr/local/nodejs
    cd $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64/bin/
    echo $PASSWORD | sudo -S npm config set registry https://registry.npmmirror.com
    echo $PASSWORD | sudo -S npm install -g yarn pnpm
    echo $PASSWORD | sudo -S yarn config set registry https://registry.npmmirror.com
    echo $PASSWORD | sudo -S pnpm config set registry https://registry.npmmirror.com
    echo $PASSWORD | sudo -S ln -s $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64/bin/node /usr/bin/node
    echo $PASSWORD | sudo -S ln -s $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64/bin/npm /usr/bin/npm
    echo $PASSWORD | sudo -S ln -s $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64/bin/yarn /usr/bin/yarn
    echo $PASSWORD | sudo -S ln -s $SOFTWARE_DIR/$NODEJS_VERSION-linux-x64/bin/pnpm /usr/bin/pnpm
    echo 'Node.js 安装完毕 当前版本'$(node -v)
}

function install_python_package_ubuntu() {
    echo '安装Python编译所需依赖'
    echo $PASSWORD | sudo -S apt-get -y install build-essential gdb lcov pkg-config \
        libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
        libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
        lzma lzma-dev tk-dev uuid-dev zlib1g-dev libmpdec-dev
}

function install_python() {
    # 编译Python
    echo '开始编译Python'
    echo $PASSWORD | sudo -S wget -O $SOFTWARE_DIR/$PYTHON_VERSION.tar.xz $PYTHON
    echo $PASSWORD | sudo -S tar -xvf $SOFTWARE_DIR/$PYTHON_VERSION.tar.xz -C $SOFTWARE_DIR
    cd $SOFTWARE_DIR/$PYTHON_VERSION/
    # 配置编译选项
    echo $PASSWORD | sudo -S ./configure --enable-optimizations

    # 编译 (使用 -j 选项加速编译过程，N 代表使用 N 核进行编译)
    echo $PASSWORD | sudo -S make -j$(nproc) && sudo make altinstall

    # 创建软连接
    echo $PASSWORD | sudo -S ln -s /usr/local/bin/python3.12 /usr/bin/python
    echo $PASSWORD | sudo -S ln -s /usr/local/bin/pip3.12 /usr/bin/pip
    pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple
    cd $PWD_FILES
    echo "Python 3.12 安装成功！" 当前Python版本$(python -V)
}

function hash_python_version() {
    v=$(python3 -V | awk '{print $2}' | awk -F '.' '{print $2}')
    if [ $v -le 10 ]; then
        echo "当前Python版本$v,需要升级Python版本"
        install_python
    else
        echo "大于10,开始安装django虚拟环境"
        start_django
    fi
}

function install_redis_ubuntu() {
    echo $PASSWORD | sudo -S apt install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg
    echo $PASSWORD | sudo -S gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    echo $PASSWORD | sudo -S tee /etc/apt/sources.list.d/redis.list <<EOF
deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main
EOF
    echo $PASSWORD | sudo -S apt-get update
    echo $PASSWORD | sudo -S apt-get install redis -y
}

function install_project_package_ubuntu() {
    # 安装项目依赖的软件
    echo $PASSWORD | sudo -S apt-get -y install snmp* libsnmp-dev libmysqlclient-dev libpq-dev python3-dev
}

function change_mirrors_ubuntu() {
    echo "配置南京大学镜像"
    # 备份原有源
    echo $PASSWORD | sudo -S cp /etc/apt/sources.list{,.back}
    # 更新sources.list文件
    echo $PASSWORD | sudo -S tee /etc/apt/sources.list <<EOF
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirror.nju.edu.cn/ubuntu/ jammy main restricted universe multiverse
# deb-src https://mirror.nju.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirror.nju.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
# deb-src https://mirror.nju.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirror.nju.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
# deb-src https://mirror.nju.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb https://mirror.nju.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
# deb-src https://mirror.nju.edu.cn/ubuntu/ jammy-security main restricted universe multiverse

# deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse
# # deb-src http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirror.nju.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
# # deb-src https://mirror.nju.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
EOF
    echo $PASSWORD | sudo -S apt update && sudo apt upgradable -y
}

function main() {

    echo "本机IP地址是: $IP"
    change_mirrors
    install_project_package_ubuntu
    mkdir_files
    install_python
    install_nodejs
    start_vue
    install_redis
    start_django
    start_celery

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
