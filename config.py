# config.py
# 扫描线程数
THREAD_NUM = 10
# 常见目录列表
COMMON_DIRS = [
    "admin", "login", "static", "uploads", "css", "js", "images",
    "backup", "test", "api", "index.php", "config", "phpinfo.php"
]
# 请求头
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
# 扫描超时时间
TIMEOUT_SCAN = 5
# SQL注入关键词
KEYWORDS = ["MySQL server version", "You have an error in your SQL syntax", "Warning: mysql_", "mysqli_error", "SQL syntax"]

# XSS检测载荷与验证关键词
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "\"'><svg onload=alert(1)>",
    "%3Cscript%3Ealert%28%27XSS%27%29%3C/script%3E"  # URL编码版本
]
XSS_KEYWORDS = ["<script>alert('XSS')</script>", "alert(1)", "onerror=alert(1)", "onload=alert(1)"]