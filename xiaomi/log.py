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
    print(token)
    getLogUrl = f"http://{ip}/cgi-bin/luci/;stok={token}/api/misystem/sys_log"
    # 生产日志信息

    print("正在获取日志信息...请稍后...")
    get_response = requests.get(getLogUrl, headers=headers)
    if get_response.status_code == 200:
        logUrl = get_response.json().get('path')
        webbrowser.open(logUrl)
    else:
        print(f"获取日志信息失败，状态码：{get_response.status_code}")

# 示例调用
if __name__ == "__main__":
    login("192.168.1.4","admin","1q2w3e4r..")
