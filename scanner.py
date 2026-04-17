import requests

requests.packages.urllib3.disable_warnings()

def check_url_alive(target_url: str) -> bool:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(
            url=target_url,
            headers=headers,
            verify=False,
            timeout=5
        )
        if 100 <= response.status_code < 400:
            print(f"[+] {target_url} 存活 | 状态码: {response.status_code}")
            return True
        else:
            print(f"[-] {target_url} 异常 | 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] {target_url} 不可达 | 错误: {str(e)}")
        return False

def batch_check_urls(url_list: list):
    """批量检测URL存活"""
    print("===== 开始批量URL存活检测 =====")
    alive_count = 0
    for url in url_list:
        if check_url_alive(url):
            alive_count += 1
    print(f"===== 检测完成：总计 {len(url_list)} 个，存活 {alive_count} 个 =====")

if __name__ == "__main__":
    # 测试批量检测
    target_urls = [
        "https://www.baidu.com",
        "https://example.com",
        "https://nonexist-test-12345.com",
        "https://github.com"
    ]
    batch_check_urls(target_urls)