import requests
import re

#关闭SSL警告（因为我们用verify=Fales）。
requests.packages.urllib3.disable_warnings()

def is_valid_url(url: str) -> bool:
    """
    判断输入的是否为合法网址
    检查是否以 http:// 或 https:// 开头
    """
    # 正则表达式：匹配 http 或 https 开头
    pattern = r'^https?://.+'
    if re.match(pattern, url):
        return True
    return False

def check_url_alive(target_url:str) -> bool:
    """
    检测
    目标URL是否存活
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(
            url = target_url,
            headers = headers,
            verify = False, #关闭SSL验证。
            timeout = 5
        )
        #状态码1xx，2xx，3xx都视为存活。
        if 100 <= response.status_code <400:
            print(f"[+]{target_url}存活，状态码{response.status_code}")
            return True
    except Exception as e:
        print(f"[-]{target_url}不可达，原因：{str(e)}")
        return False

if __name__ == "__main__":
    print("===== Web漏洞扫描器 =====")
    # 让用户输入要检测的网址
    target = input("\n请输入要检测的网址（http/https开头）: ")

    # 调用 URL 校验函数
    if not is_valid_url(target):
        print("[-] 错误：请输入以 http:// 或 https:// 开头的正确网址！")
    else:
        # 合法则开始检测
        check_url_alive(target)














