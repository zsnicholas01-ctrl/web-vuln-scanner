# main.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import requests
from scanner import CoreScanner
from poc import POCScanner
from utils import save_report

requests.packages.urllib3.disable_warnings()


class WebScannerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("模块化安全扫描器 v0.4")
        self.window.geometry("750x600")
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.window, text="目标URL：", font=("微软雅黑", 12)).pack(pady=5)
        self.entry_url = scrolledtext.ScrolledText(self.window, width=85, height=6)
        self.entry_url.pack(pady=5)

        self.btn_scan = ttk.Button(self.window, text="开始全面扫描", command=self.start_thread)
        self.btn_scan.pack(pady=5)

        self.result_box = scrolledtext.ScrolledText(self.window, width=85, height=24)
        self.result_box.pack(pady=5)

    def log(self, msg):
        self.result_box.insert(tk.END, msg + "\n")
        self.result_box.see(tk.END)

    def do_scan(self):
        url = self.entry_url.get("1.0", tk.END).strip()
        if not url:
            self.log("[!] 请输入URL")
            return

        self.log("=" * 60)
        self.log(f"[*] 开始扫描: {url}")

        # 1. 存活检测
        scanner = CoreScanner(url)
        alive, msg = scanner.check_alive()
        self.log(msg)
        if not alive:
            self.log("[!] 目标不可达")
            return

        # 2. 目录扫描
        self.log("\n[*] 开始目录扫描...")
        scanner.scan_all_dirs(callback=self.log)
        self.log("[√] 目录扫描完成")

        # 3. POC 漏洞检测
        self.log("\n[*] 开始POC漏洞检测...")
        poc = POCScanner(url)

        res = poc.check_phpinfo()
        if res: self.log(res)

        res = poc.check_robots()
        if res: self.log(res)

        res = poc.check_path_traversal()
        if res: self.log(res)

        self.log("\n 全部扫描完成！")
        self.log("=" * 60)
        # 导出报告
        report_content = self.result_box.get("1.0", tk.END)
        save_report("scan_report.txt", report_content)
        self.log("[+] 报告已保存: scan_report.txt")

    def start_thread(self):
        t = threading.Thread(target=self.do_scan)
        t.start()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = WebScannerGUI()
    app.run()