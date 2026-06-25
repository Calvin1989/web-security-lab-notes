\# Web 常见漏洞复现与安全评估实践



\## 项目简介



本项目基于本地授权靶场环境，对 Web 应用中常见安全漏洞进行复现、分析和修复总结。项目覆盖 SQL 注入、XSS、文件上传、命令执行、目录遍历、弱口令、越权漏洞、SSRF 等常见 Web 安全问题。



\## 合规声明



本仓库仅用于本地授权靶场学习，所有测试均在 DVWA、Pikachu、Vulhub、PortSwigger Web Security Academy 等合法环境中完成，不涉及任何真实互联网目标测试。



\## 项目目标



\- 理解常见 Web 漏洞的产生原因；

\- 掌握 Burp Suite 抓包、改包和 HTTP 请求分析方法；

\- 能够完成漏洞复现、证据截图、风险分析和修复建议；

\- 形成安全服务/渗透测试实习可展示的项目报告合集。



\## 实验环境



\- Windows

\- Docker

\- DVWA

\- Pikachu

\- Burp Suite Community

\- Chrome / Firefox

\- Markdown



\## 第一阶段漏洞清单



| 编号 | 漏洞类型 | 报告文件 |

|---|---|---|

| 01 | SQL 注入 | reports/01-sql-injection.md |

| 02 | XSS | reports/02-xss.md |

| 03 | 文件上传漏洞 | reports/03-file-upload.md |

| 04 | 命令执行漏洞 | reports/04-command-injection.md |

| 05 | 目录遍历 / 任意文件读取 | reports/05-directory-traversal.md |

| 06 | 弱口令 / 暴力破解 | reports/06-weak-password.md |

| 07 | 越权漏洞 | reports/07-access-control.md |

| 08 | SSRF | reports/08-ssrf.md |



\## 报告格式



每篇报告均包含以下内容：



1\. 漏洞概述

2\. 漏洞原理

3\. 复现环境

4\. 复现步骤

5\. 漏洞验证结果

6\. 风险影响

7\. 修复建议

8\. 复测结论

