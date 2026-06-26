# 项目验证记录

## 1. Python 脚本语法检查

执行命令：

    python -m py_compile tools\access-log-risk-summary.py

结果：

通过。

## 2. 日志风险摘要生成

执行命令：

    python tools\access-log-risk-summary.py sample-logs\access-demo.log -o summary\log-risk-summary.md

结果：

成功生成 summary/log-risk-summary.md。

## 3. 样例日志统计

日志文件：

sample-logs/access-demo.log

总行数：

35 行

覆盖风险类型：

SQL 注入、XSS、文件上传、命令执行、目录遍历、弱口令、水平越权、SSRF、CSRF、XXE、PHP 反序列化、目录扫描、敏感路径访问。

## 4. 验证说明

本项目中的可运行部分主要包括 Web access log 风险摘要脚本和样例日志分析流程。验证结果说明脚本语法正常，可以基于样例日志生成 Markdown 风险摘要。

漏洞复现部分基于本地授权靶场 DVWA 和 Pikachu 完成，工具辅助评估结果保存在 scan-results/ 目录中。
