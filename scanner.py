import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

# 关闭SSL警告
requests.packages.urllib3.disable_warnings()


def check_url_alive(target_url):
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
            return f"[+] 存活 | 状态码: {response.status_code} | {target_url}"
        else:
            return f"[-] 异常 | 状态码: {response.status_code} | {target_url}"
    except Exception as e:
        return f"[-] 不可达 | 错误: {str(e)} | {target_url}"


def dir_scan(base_url):
    result = []
    result.append(f"\n===== 开始扫描【{base_url}】目录 =====")

    # 常见后台目录列表
    dir_list = [
        "admin", "login", "robots.txt", "index.php",
        "backup", "test", "manage", "console", "sql"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for d in dir_list:
        url = base_url.rstrip("/") + "/" + d.lstrip("/")
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=3)
            if res.status_code == 200:
                result.append(f"[+] 发现可访问目录: {url}")
        except:
            continue
    result.append("===== 目录扫描完成 =====\n")
    return "\n".join(result)


def start_check():
    url_input = entry_url.get("1.0", tk.END).strip()
    if not url_input:
        result_box.insert(tk.END, "[!] 请输入URL\n")
        return

    result_box.insert(tk.END, "===== 开始检测 =====\n")

    # 只取第一行当目标
    target = url_input.splitlines()[0].strip()

    # 1. 存活检测
    alive_res = check_url_alive(target)
    result_box.insert(tk.END, alive_res + "\n")

    # 2. 目录扫描
    scan_res = dir_scan(target)
    result_box.insert(tk.END, scan_res + "\n")

    result_box.insert(tk.END, "===== 全部任务完成 =====\n\n")


# ==================== GUI 界面 ====================
window = tk.Tk()
window.title("Web安全检测工具 v1.0")
window.geometry("750x550")

tk.Label(window, text="请输入目标URL（仅输入一个）：", font=("微软雅黑", 12)).pack(pady=5)
entry_url = scrolledtext.ScrolledText(window, width=85, height=6)
entry_url.pack(pady=5)

btn_check = ttk.Button(window, text="开始检测 + 目录扫描", command=start_check)
btn_check.pack(pady=5)

result_box = scrolledtext.ScrolledText(window, width=85, height=20)
result_box.pack(pady=5)

window.mainloop()