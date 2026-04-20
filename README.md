# Web漏洞扫描器 v0.4
Python 编写的轻量级Web漏洞扫描器

## 功能
- URL存活检测
- 批量URL检测
- 基础目录扫描
- phpinfo信息泄露漏洞检测
- robots.txt 敏感信息检测
- 支持扫描结果自动导出 TXT 报告

## 项目架构
- main.py：GUI主程序
- scanner.py：存活检测+多线程目录扫描
- poc.py：漏洞检测POC模块
- utils.py：工具函数

## 使用方法
python main.py