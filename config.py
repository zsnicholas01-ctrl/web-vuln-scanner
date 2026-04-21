# config.py
# 扫描配置
THREAD_NUM = 20
COMMON_DIRS = [
    "admin", "login", "manage", "backend", "robots.txt",
    "index.php", "test", "backup", "sql", "console",
    "admin.php", "login.php", "phpinfo.php", "install"
]

# 请求头配置
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
# 常见SQL报错关键词
KEYWORDS = ["MySQL", "SQL syntax", "error", "ORA-", "Microsoft SQL Server"]

# 超时配置
TIMEOUT_ALIVE = 5
TIMEOUT_SCAN = 3