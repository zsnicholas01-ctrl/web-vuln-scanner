# scanner.py
import requests
from concurrent.futures import ThreadPoolExecutor

class CoreScanner:
    def __init__(self, base_url, thread_num=20):
        self.base_url = base_url.rstrip("/")
        self.thread_num = thread_num
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.common_dirs = [
            "admin", "login", "manage", "backend", "robots.txt",
            "index.php", "test", "backup", "sql", "console",
            "admin.php", "login.php", "phpinfo.php", "install"
        ]

    # 存活检测
    def check_alive(self):
        try:
            r = requests.get(self.base_url, headers=self.headers, timeout=5, verify=False)
            if 200 <= r.status_code < 400:
                return True, f"[+] 存活 状态码:{r.status_code}"
            else:
                return False, f"[-] 异常 状态码:{r.status_code}"
        except Exception as e:
            return False, f"[-] 不可达 {str(e)}"

    # 单目录扫描
    def scan_dir(self, d, callback):
        target = f"{self.base_url}/{d.lstrip('/')}"
        try:
            r = requests.get(target, headers=self.headers, timeout=3, verify=False)
            if r.status_code == 200:
                callback(f"[+] 发现目录: {target}")
        except:
            pass

    # 多线程目录扫描
    def scan_all_dirs(self, callback):
        with ThreadPoolExecutor(max_workers=self.thread_num) as executor:
            for d in self.common_dirs:
                executor.submit(self.scan_dir, d, callback)