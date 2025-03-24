import os
import re
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlparse

import requests
import Encrypt
import webbrowser

def login(ip,username, password):
    """
    登录小米路由器的函数
    :param router: 路由器对象，包含用户名、密码和登录URL
    :return: 登录成功返回True，失败返回False
    """
    encrypt = Encrypt.Encrypt()
    nonce = encrypt.init()
    oldPwd = encrypt.oldPwd(password)

    headers = {
        "connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",

    }
    log_url = f'http://{ip}/cgi-bin/luci/api/xqsystem/login'

    data = {
        "username": username,
        "password": oldPwd,
        "logtype": 2,
        "nonce": nonce
    }
    # //获取token
    token = requests.post(log_url, headers=headers, data=data).json()['token']
    print('token:', token)
    getLogUrl = f"http://{ip}/cgi-bin/luci/;stok={token}/api/misystem/sys_log"
    # 生产日志信息

    print("正在获取日志信息...请稍后...")
    get_response = requests.get(getLogUrl, headers=headers)
    if get_response.status_code == 200:
        # 获取日志下载地址
        logUrl = get_response.json().get('path')
        parsed_url = urlparse(logUrl)
        # 获取路径部分
        path = parsed_url.path
        # 从路径中提取文件名
        filename = os.path.basename(path)
        try:
            response = requests.get('http://'+logUrl, stream=True)
            response.raise_for_status()
            invalid_chars = r'[\\/*?:"<>|]'
            safe_filename = re.sub(invalid_chars, '', filename)
            with open(safe_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("下载文件成功！")
        except requests.exceptions.RequestException as e:
            print(f"获取日志信息失败：{e}")
    else:
        print(f"获取日志信息失败，状态码：{get_response.status_code}")
def systemInfo(ip):
    """
    登录小米路由器的函数
    :param router: 路由器对象，包含用户名、密码和登录URL

    http://192.168.1.4/cgi-bin/luci/api/xqsystem/init_info
    :return: 登录成功返回True，失败返回False
    {'romversion': '2.0.23', 'countrycode': 'CN', 'code': 0, 'id': '26679/A9Z466941', 'routername': 'Redmi_C88D', 'inited': 1, 'connect': 0, 'routerId': 'b73b5360-1267-423d-719f-980ff8399475', 'model': 'xiaomi.router.rm2100', 'hardware': 'RM2100', 'bound': 0, 'language': 'zh_cn', 'modules': {'replacement_assistant': '1'}}
    """
    headers = {
        "connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }
    url =f'http://{ip}/cgi-bin/luci/api/xqsystem/init_info'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('硬件型号：', response.json().get('hardware'))
        print('固件版本：', response.json().get('romversion'))
    else:
        print(f"获取系统信息失败，状态码：{response.status_code}")
# 示例调用
if __name__ == "__main__":
    # login("192.168.1.4","admin","1q2w3e4r..")
    ip = '192.168.1.4'
    user = 'admin'
    password = '1q2w3e4r..'
    
    systemInfo(ip)
    login(ip, user, password)