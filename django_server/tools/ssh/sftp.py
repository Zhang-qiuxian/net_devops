from paramiko import SSHClient, AutoAddPolicy, SFTPClient
import os


# def traverse_sftp_directory(sftp: SFTPClient, remote_path: str, indent=0):
#     """
#     递归遍历SFTP目录并打印文件/目录路径。
#
#     :param sftp: paramiko.SFTPClient 对象
#     :param remote_path: 远程目录路径
#     :param indent: 用于缩进的空格数，默认为0
#     """
#     # 获取目录内容
#     for item in sftp.listdir_attr(remote_path):
#         # 构建完整的远程路径
#         full_path = f"{remote_path}/{item.filename}"
#
#         # 如果是目录，则递归遍历
#         if item.st_mode & 0o40000:  # 检查是否是目录（S_IFDIR）
#             print(f"{' ' * indent}{item.filename}/")
#             traverse_sftp_directory(sftp, full_path, indent + 4)
#         else:
#             try:
#                 if item.filename in ['vrpcfg.zip', 'startup.cfg']:
#                     sftp.get(item.filename, item.filename)
#                     # 如果是文件，则打印文件名和大小
#                     print(f"{' ' * indent}{item.filename} {item.st_size} bytes")
#             except FileNotFoundError:
#                 continue
#

def traverse_sftp_directory(sftp: SFTPClient, remote_path: str, indent=0):
    """
    递归遍历SFTP目录并打印文件/目录路径。

    :param sftp: paramiko.SFTPClient 对象
    :param remote_path: 远程目录路径
    :param indent: 用于缩进的空格数，默认为0
    """
    # 获取目录内容
    for item in sftp.listdir_attr(remote_path):
        # 构建完整的远程路径
        full_path = f"{remote_path}/{item.filename}"

        # 打印目录或文件名
        print(">>>>>>", item.st_mode)
        if item.st_mode & 0o40000:  # 检查是否是目录（S_IFDIR）
            print(f"{' ' * indent}{item.filename}/")
            traverse_sftp_directory(sftp, full_path, indent + 4)
        else:
            # 检查是否是要下载的文件名
            if item.filename in ['vrpcfg.zip', 'startup.cfg']:
                # 构建本地文件路径
                local_path = os.path.join(os.getcwd(), item.filename)  # 假设下载到当前工作目录
                try:
                    # 下载文件
                    sftp.get(full_path, local_path)
                    # 打印文件名和大小
                    print(f"{' ' * indent}{item.filename} {item.st_size} bytes")
                    return
                except FileNotFoundError:
                    print(f"Local directory does not exist for {local_path}")
                except FileExistsError:
                    print(f"File {local_path} already exists, skipping download.")
                except OSError as e:
                    print(f"An OSError occurred: {e}")
            else:
                # 对于其他文件，只打印文件名和大小
                print(f"{' ' * indent}{item.filename} {item.st_size} bytes")


def get_sftp_client(hostname: str = '', port: int = 22, username: str = '', password: str = '') -> SFTPClient:
    """  
    获取SFTP客户端对象。  
      
    :param hostname: SFTP服务器主机名或IP地址  
    :param port: SFTP服务器端口号  
    :param username: 登录用户名  
    :param password: 登录密码  
    :return: paramiko.SFTPClient 对象  
    """
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(hostname, port, username, password)
    return client.open_sftp()


if __name__ == '__main__':
    d: list = [
        dict(hostname='10.10.10.2', username='admin', password='qxxx1473464511mm', port=22),
        dict(hostname='10.10.10.1', username='admin', password='qxxx1473464511mm', port=22),
    ]
    # 使用函数
    # hostname = '10.10.10.1'
    # port = 22  # 默认的SFTP端口是22
    # username = 'admin'
    # password = 'qxxx1473464511mm'
    remote_root_path = ''  # 远程根目录路径
    for i in d:
        # 获取SFTP客户端对象
        sftp = get_sftp_client(**i)
        # 遍历目录并打印文件/目录路径
        traverse_sftp_directory(sftp, remote_root_path)
        # 关闭SFTP连接
        sftp.close()
