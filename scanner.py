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

def start_check():
    # 获取输入框内容
    url_input = entry_url.get("1.0", tk.END).strip()
    if not url_input:
        result_box.insert(tk.END, "[!] 请输入URL\n")
        return

    # 按行拆分多个URL
    url_list = [u.strip() for u in url_input.splitlines() if u.strip()]

    result_box.insert(tk.END, "===== 开始检测 =====\n")

    for url in url_list:
        res = check_url_alive(url)
        result_box.insert(tk.END, res + "\n")

    result_box.insert(tk.END, "===== 检测完成 =====\n\n")

# ==================== GUI 界面 ====================
window = tk.Tk()
window.title("URL存活检测工具 v1.0")
window.geometry("700x500")

# 标签
tk.Label(window, text="请输入URL（一行一个）：", font=("微软雅黑", 12)).pack(pady=5)

# 输入框
entry_url = scrolledtext.ScrolledText(window, width=80, height=8)
entry_url.pack(pady=5)

# 检测按钮
btn_check = ttk.Button(window, text="开始检测", command=start_check)
btn_check.pack(pady=5)

# 结果显示框
result_box = scrolledtext.ScrolledText(window, width=80, height=14)
result_box.pack(pady=5)

window.mainloop()