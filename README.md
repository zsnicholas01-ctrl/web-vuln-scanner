# Web安全扫描工具
一款基于Python + Tkinter开发的模块化Web安全扫描器

## 功能特点
- URL存活检测
- 多线程目录扫描
- POC漏洞检测（phpinfo/robots.txt/路径遍历）
- 扫描结果自动导出TXT报告
- 配置文件分离管理
- 模块化架构设计

## 项目架构
- main.py        GUI主程序与任务调度
- scanner.py     核心扫描逻辑（存活、目录扫描）
- poc.py         漏洞检测POC模块
- utils.py       工具函数（报告导出）
- config.py      全局配置（线程数、字典、请求头）

## 使用方法
1. 安装依赖：pip install requests
2. 运行：python main.py
3. 输入目标URL，点击开始扫描
4. 扫描完成后自动生成 scan_report.txt