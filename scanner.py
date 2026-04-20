import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from concurrent.futures import ThreadPoolExecutor
import threading

requests.packages.urllib3.disable_warnings()

class WebScannerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("多线程Web安全扫描器 v0.3")
        self.window.geometry("750x550")

        # 常见目录
        self.common_dirs = [
            "admin", "login", "manage", "backend", "robots.txt",
            "index.php", "test", "backup", "sql", "console",
            "admin.php", "login.php", "phpinfo.php", "1.php", "install"
        ]

        self.thread_num = 20  # 线程数（安全工具常用值）
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.window, text="目标URL：", font=("微软雅黑",12)).pack(pady=5)
        self.entry_url = scrolledtext.ScrolledText(self.window, width=85, height=6)
        self.entry_url.pack(pady=5)

        self.btn_scan = ttk.Button(self.window, text="开始多线程扫描", command=self.start_scan_thread)
        self.btn_scan.pack(pady=5)

        self.result_box = scrolledtext.ScrolledText(self.window, width=85, height=20)
        self.result_box.pack(pady=5)

    def log(self, msg):
        # GUI 输出必须安全调用
        self.result_box.insert(tk.END, msg + "\n")
        self.result_box.see(tk.END)

    def check_alive(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=5, verify=False)
            if 200 <= r.status_code < 400:
                return True, f"[+] 存活 状态码:{r.status_code}"
            else:
                return False, f"[-] 异常 状态码:{r.status_code}"
        except Exception as e:
            return False, f"[-] 不可达 {str(e)}"

    def scan_single_dir(self, base_url, d):
        url = base_url.rstrip("/") + "/" + d.lstrip("/")
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=3, verify=False)
            if r.status_code == 200:
                self.log(f"[+] 发现目录: {url}")
        except:
            return

    def dir_scan_thread(self, base_url):
        self.log("\n[*] 开始多线程目录扫描...")
        with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
            for d in self.common_dirs:
                executor.submit(self.scan_single_dir, base_url, d)
        self.log("\n[√] 目录扫描完成")

    def check_phpinfo(self,base_url):
        target = base_url.rstrip("/") + "/phpinfo.php"
        headers =  {"User_Agent":"Mozilla/5.0"}
        try:
            r = requests.get(target,headers=headers,timeout=3,verify=False)
            if "phpinfo" in r.text and "PHP Version" in r.text:
                self.log(f"[高危]发现phpinfo信息泄露：{target}")

        except:
            pass

    def check_robots(self,base_url):
        target = base_url.rstrip("/") + "/robots.txt"
        headers = {"User_Agent": "Mozilla/5.0"}
        try:
            r = requests.get(target,headers=headers,timeout=3,verify=False)
            if r.status_code ==  200 and len(r.text) >  10:
                self.log(f"[中危]发现robots.txt敏感路径：{target}")
        except Exception:
            pass

    def start_scan_thread(self):
        # 开独立线程，避免GUI卡死
        t = threading.Thread(target=self.do_scan)
        t.start()

    def do_scan(self):
        url = self.entry_url.get("1.0", tk.END).strip()
        if not url:
            self.log("[!] 请输入URL")
            return

        self.log("="*50)
        self.log(f"[*] 目标: {url}")

        # 存活检测
        alive, msg = self.check_alive(url)
        self.log(msg)
        if not alive:
            self.log("[!] 目标不可达")
            self.log("="*50+"\n")
            return

        # 多线程目录扫描
        self.dir_scan_thread(url)
        # phpinfo信息泄露
        self.check_phpinfo(url)
        #robots.txt敏感路径
        self.check_robots(url)
        self.log("="*50+"\n")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WebScannerGUI()
    app.run()