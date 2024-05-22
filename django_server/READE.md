# net_devops 一个基于Django REST Framework的项目


### 介绍

net_devops 是一个基于`Django REST Framework`构建的Web服务项目。它提供了API接口，用于与后端数据库进行交互，并支持前后端分离的开发模式。


###  安装/设置

- **依赖项**：由于后端需要通过`SNMP`来获取设备信息，请确保操作系统是`Linux`。定时任务依赖`redis`，后端数据库可选择`mysql、postgre、sqlit3`随便一种，只需要看效果就无脑选`sqlite3`。

  ```shell
  # Pyhton >= 3.10
  python -m venv venv
  source venv/bin/activate
  pip install -i https://mirror.nju.edu.cn/pypi/web/simple -r requirements.txt
  ```

- **系统要求**：本人开发环境`Ubuntu22.04 LTS`，其它`Linux`环境也大差不差。

- **环境设置**：提供任何必要的环境变量设置或配置文件修改说明。

- **初始化步骤**：如果项目需要特定的初始化步骤（如数据库迁移），请详细说明。

