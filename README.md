# Web 常见漏洞复现与修复实践

## 项目说明

本仓库用于记录 Web 常见漏洞的本地授权靶场复现过程、漏洞原理分析、风险影响和修复建议。

所有测试均在 DVWA、Pikachu 等本地授权靶场环境中完成，仅用于安全学习、漏洞理解和报告编写练习，不涉及任何真实业务系统、公网目标或未授权测试。

## 项目目标

通过本项目，系统复现和总结常见 Web 安全漏洞，形成标准化漏洞复现报告，提升以下能力：

* Web 漏洞原理理解；
* Burp Suite 抓包与请求分析；
* 漏洞复现证据整理；
* 风险影响分析；
* 安全修复建议编写；
* 安全服务报告交付意识。

## 项目亮点

- 覆盖 11 类常见 Web 漏洞：SQL 注入、XSS、文件上传、命令执行、目录遍历、弱口令、水平越权、SSRF、CSRF、XXE、PHP 反序列化；
- 每类漏洞均包含漏洞原理、复现步骤、截图证据、Burp 抓包分析、风险影响、修复建议和复测结论；
- 额外整理模拟 Web 系统安全评估总报告，将单点漏洞报告整合为安全服务交付视角；
- 补充 Web 攻击日志表现与告警建议速查表，将漏洞复现与安全运营日志分析关联起来；
- 所有测试均在 DVWA、Pikachu 等本地授权靶场中完成，保留明确安全边界说明。
- 补充工具辅助安全评估流程：使用 Nmap 进行本地服务识别，使用 dirsearch 进行目录枚举，使用 SQLmap 对已手工确认的 SQL 注入点进行辅助验证，使用 Nuclei 进行基础模板扫描，并整理扫描结果和人工复核结论。

## 复现环境

* 操作系统：Windows
* Web 环境：小皮面板 / PHP / MySQL
* 靶场环境：DVWA、Pikachu
* 辅助工具：Chrome、Burp Suite
* 测试方式：本地授权靶场测试
- 辅助工具：Nmap、dirsearch、SQLmap、Nuclei
- 日志分析：Python、access-log-risk-summary.py

## 交付文档

| 文档 | 说明 |
|---|---|
| [Web 系统安全评估模拟报告](summary/web-security-assessment-report.md) | 从安全服务交付角度汇总测试范围、测试方法、漏洞清单、风险分析、整改建议和安全运营视角 |
| [项目总结](summary/project-summary.md) | 总结项目背景、完成内容、漏洞理解和后续计划 |
| [简历项目描述](summary/resume-project.md) | 用于简历中的项目描述、项目职责和技术栈 |
| [Web 漏洞修复建议速查表](notes/remediation-cheatsheet.md) | 汇总 11 类漏洞的常见修复建议 |
| [Web 攻击日志表现与告警建议速查表](notes/log-detection-cheatsheet.md) | 汇总常见 Web 攻击在日志中的表现和基础告警建议 |
| GitHub 项目展示说明 | [summary/github-showcase.md](summary/github-showcase.md) |
| 工具辅助安全评估报告 | [summary/tool-assisted-assessment.md](summary/tool-assisted-assessment.md) |
| 工具扫描结果与证据 | [scan-results/](scan-results/) |
| 项目面试讲解稿 | [summary/interview-guide.md](summary/interview-guide.md) |

## 已完成漏洞报告

| 序号 | 漏洞类型          | 靶场      | 报告                                                             |
| -- | ------------- | ------- | -------------------------------------------------------------- |
| 01 | SQL 注入        | DVWA    | [01-sql-injection.md](reports/01-sql-injection.md)             |
| 02 | XSS           | DVWA    | [02-xss.md](reports/02-xss.md)                                 |
| 03 | 文件上传漏洞        | DVWA    | [03-file-upload.md](reports/03-file-upload.md)                 |
| 04 | 命令执行漏洞        | DVWA    | [04-command-injection.md](reports/04-command-injection.md)     |
| 05 | 目录遍历 / 任意文件读取 | DVWA    | [05-directory-traversal.md](reports/05-directory-traversal.md) |
| 06 | 弱口令 / 暴力破解    | DVWA    | [06-weak-password.md](reports/06-weak-password.md)             |
| 07 | 水平越权漏洞        | Pikachu | [07-access-control.md](reports/07-access-control.md)           |
| 08 | SSRF 服务端请求伪造  | Pikachu | [08-ssrf.md](reports/08-ssrf.md)                               |
| 09 | CSRF 跨站请求伪造 | Pikachu | [09-csrf.md](reports/09-csrf.md) |
| 10 | XXE XML 外部实体注入 | Pikachu | [10-xxe.md](reports/10-xxe.md) |
| 11 | PHP 反序列化漏洞 | Pikachu | [11-deserialization.md](reports/11-deserialization.md) |

## 截图证据目录

| 漏洞类型   | 截图目录                               |
| ------ | ---------------------------------- |
| SQL 注入 | `screenshots/sql-injection/`       |
| XSS    | `screenshots/xss/`                 |
| 文件上传   | `screenshots/file-upload/`         |
| 命令执行   | `screenshots/command-injection/`   |
| 目录遍历   | `screenshots/directory-traversal/` |
| 弱口令    | `screenshots/weak-password/`       |
| 越权漏洞   | `screenshots/access-control/`      |
| SSRF   | `screenshots/ssrf/`                |
| CSRF | `screenshots/csrf/` |
| XXE | `screenshots/xxe/` |
| PHP 反序列化 | `screenshots/deserialization/` |

## 报告格式

每篇漏洞报告均按照以下结构整理：

1. 漏洞概述
2. 漏洞原理
3. 复现环境
4. 复现步骤
5. 漏洞验证结果
6. 风险影响
7. 修复建议
8. 复测结论

## 日志分析扩展

除漏洞复现报告外，本项目补充了 Web 攻击日志表现与告警建议速查表，用于将漏洞复现行为与安全运营分析思路关联起来。

该部分重点总结以下内容：

- SQL 注入、XSS、文件上传、命令执行、目录遍历、暴力破解、越权、SSRF 等攻击行为在访问日志中的可能表现；
- 基于 URL 参数、请求方法、状态码、响应大小、User-Agent、Cookie、访问频率等字段的分析思路；
- 常见告警规则设计建议；
- 误报控制和多字段关联分析思路；
- 与日志分析项目形成“漏洞复现 -> Burp 请求分析 -> 日志特征 -> 告警规则 -> 安全运营研判”的闭环。

## 日志风险分析工具

本项目不仅包含 Web 漏洞复现报告，还补充了一个基础日志风险分析脚本：

```text
tools/access-log-risk-summary.py
```

该脚本用于读取 Web access.log，并根据常见 Web 攻击特征生成 Markdown 风险摘要。当前支持识别的风险类型包括：

* SQL 注入
* XSS
* 文件上传风险
* 命令执行
* 目录遍历 / 任意文件读取
* 弱口令 / 暴力破解
* SSRF
* XXE
* PHP 反序列化

示例运行命令：

```powershell
python tools\access-log-risk-summary.py sample-logs\access-demo.log -o summary\log-risk-summary.md
```

输出结果：

```text
summary/log-risk-summary.md
```

该工具用于把漏洞复现中的攻击请求特征转化为日志检测思路，形成：

```text
漏洞复现 -> Burp 请求分析 -> 日志特征提取 -> 风险摘要输出 -> 安全运营研判
```

需要说明的是，该脚本基于正则和关键字进行基础检测，结果用于学习和初步研判，不等同于完整 WAF、SIEM 或 EDR 检测能力。


## 安全声明

本仓库仅用于本地授权靶场学习和安全能力建设。所有测试均在 DVWA、Pikachu 等合法授权环境中完成，不涉及真实业务系统、公网目标、第三方系统或任何未授权测试。

请勿将本项目中的测试方法用于未授权环境。

