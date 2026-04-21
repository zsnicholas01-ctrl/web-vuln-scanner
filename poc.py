#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POC漏洞检测模块
实现常见信息泄露与简单漏洞验证
"""
import requests
from config import *

class POCScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def check_phpinfo(self):
        target = self.base_url + "/phpinfo.php"
        try:
            r = requests.get(target, headers=HEADERS, timeout=TIMEOUT_SCAN, verify=False)
            if "phpinfo" in r.text and "PHP Version" in r.text:
                return f"[高危] phpinfo信息泄露: {target}"
        except:
            return None

    def check_robots(self):
        target = self.base_url + "/robots.txt"
        try:
            r = requests.get(target, headers=HEADERS, timeout=TIMEOUT_SCAN, verify=False)
            if r.status_code == 200 and len(r.text) > 10:
                return f"[中危] robots.txt泄露: {target}"
        except:
            return None

    def check_path_traversal(self):
        target = self.base_url + "/../../etc/passwd"
        try:
            r = requests.get(target, headers=HEADERS, timeout=TIMEOUT_SCAN, verify=False)
            if "root:x:" in r.text:
                return f"[高危] 路径遍历漏洞: {target}"
        except:
            return None

    def check_sql(self):
        target = self.base_url.rstrip("/") + "?id=1'"
        try:
            r = requests.get(target,headers=HEADERS,timeout=TIMEOUT_SCAN,verify=False)
            keywords =  KEYWORDS
            for kw in keywords:
                if kw in r.text:
                    return f"[高危]可能存在sql注入：{target}"
        except:
            return None





