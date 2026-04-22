# Web安全扫描器
一个基于Python + Tkinter的轻量级Web安全扫描工具

## 功能特点
- URL存活检测
- 多线程目录扫描
- POC漏洞检测（phpinfo/robots.txt/路径遍历/SQL注入/XSS）
- 扫描结果可导出为TXT报告
- 自定义请求头/超时时间
- 模块化设计，易扩展
- 简洁GUI界面，支持多功能单独选择扫描

## 文件说明
- main.py        GUI主界面与功能调度
- scanner.py     核心扫描逻辑（存活检测、目录扫描）
- poc.py         漏洞检测POC模块
- utils.py       工具类（报告保存）
- config.py      全局配置（线程数、关键词、请求头）

## 使用方法
1. 安装依赖：pip install requests
2. 运行：python main.py
3. 输入目标URL，选择对应功能开始扫描
4. 扫描完成后可导出 scan_report.txt