#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序入口
GUI界面 + 功能按钮调度
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
from scanner import Scanner
from poc import POCScanner
from utils import save_report
import requests

class VulnScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web漏洞扫描器 v1.1")
        self.root.geometry("850x600")

        # 顶部URL输入
        tk.Label(root, text="目标URL:").place(x=10, y=10)
        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.place(x=80, y=10)
        self.url_entry.insert(0, "http://")

        # ==================== 功能按钮区域 ====================
        self.btn_alive = ttk.Button(root, text="存活检测", command=self.start_alive)
        self.btn_alive.place(x=10, y=50)

        self.btn_dir = ttk.Button(root, text="目录扫描", command=self.start_dir_scan)
        self.btn_dir.place(x=100, y=50)

        self.btn_phpinfo = ttk.Button(root, text="PHPinfo检测", command=self.start_phpinfo)
        self.btn_phpinfo.place(x=190, y=50)

        self.btn_robots = ttk.Button(root, text="Robots检测", command=self.start_robots)
        self.btn_robots.place(x=280, y=50)

        self.btn_path = ttk.Button(root, text="路径遍历检测", command=self.start_path_traversal)
        self.btn_path.place(x=370, y=50)

        self.btn_sqli = ttk.Button(root, text="SQL注入检测", command=self.start_sqli)
        self.btn_sqli.place(x=480, y=50)

        # 日志区域
        self.log_text = scrolledtext.ScrolledText(root, width=98, height=28)
        self.log_text.place(x=10, y=90)

        # 保存报告按钮
        ttk.Button(root, text="保存报告", command=self.save).place(x=10, y=550)

        # 变量
        self.target = ""

    # 日志输出
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()  # 实时刷新日志

    # 清空日志
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    # 校验URL格式
    def check_url(self):
        url = self.url_entry.get().strip()
        if not url.startswith(("http://", "https://")):
            self.log("[×] URL格式错误，请以 http:// 或 https:// 开头")
            return None
        self.target = url
        return url

    # ==================== 按钮对应功能 ====================
    def start_alive(self):
        threading.Thread(target=self.run_alive).start()

    def run_alive(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 正在检测：{url} 是否存活")
        s = Scanner(url)
        alive, msg = s.check_alive()  # 接收元组返回值
        self.log(msg)

    def start_dir_scan(self):
        threading.Thread(target=self.run_dir_scan).start()

    def run_dir_scan(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 开始目录扫描：{url}")
        self.log(f"[+] 线程数：{Scanner(url).thread_num}")
        s = Scanner(url)
        # 传入日志回调函数，实时打印发现的目录
        s.scan_all_dirs(callback=self.log)
        # 扫描完成后汇总结果
        if s.result:
            self.log(f"\n[√] 目录扫描完成，共发现 {len(s.result)} 个有效目录：")
            for path in s.result:
                self.log(f"    {path}")
        else:
            self.log("[-] 未发现有效目录")

    def start_phpinfo(self):
        threading.Thread(target=self.run_phpinfo).start()

    def run_phpinfo(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 开始检测 phpinfo 信息泄露：{url}")
        p = POCScanner(url)
        res = p.check_phpinfo()
        if res:
            self.log(res)
        else:
            self.log("[-] 未发现 phpinfo 漏洞")

    def start_robots(self):
        threading.Thread(target=self.run_robots).start()

    def run_robots(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 开始检测 robots.txt 泄露：{url}")
        p = POCScanner(url)
        res = p.check_robots()
        if res:
            self.log(res)
        else:
            self.log("[-] 未发现 robots.txt 泄露")

    def start_path_traversal(self):
        threading.Thread(target=self.run_path).start()

    def run_path(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 开始检测路径遍历漏洞：{url}")
        p = POCScanner(url)
        res = p.check_path_traversal()
        if res:
            self.log(res)
        else:
            self.log("[-] 未发现路径遍历漏洞")

    def start_sqli(self):
        threading.Thread(target=self.run_sqli).start()

    def run_sqli(self):
        self.clear_log()
        url = self.check_url()
        if not url:
            return
        self.log(f"[+] 开始检测 SQL 注入漏洞：{url}")
        p = POCScanner(url)
        res = p.check_sql()
        if res:
            self.log(res)
        else:
            self.log("[-] 未发现 SQL 注入漏洞")

    # 保存报告（修复文件名问题）
    def save(self):
        content = self.log_text.get(1.0, tk.END)
        if not content.strip():
            self.log("[×] 日志为空，无需保存")
            return
        # 弹出文件保存对话框
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="保存扫描报告"
        )
        if filename:
            save_report(filename, content)
            self.log(f"[√] 报告已保存至：{filename}")

if __name__ == "__main__":
    # 禁用requests警告
    requests.packages.urllib3.disable_warnings()
    root = tk.Tk()
    app = VulnScannerGUI(root)
    root.mainloop()