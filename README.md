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

## 复现环境

* 操作系统：Windows
* Web 环境：小皮面板 / PHP / MySQL
* 靶场环境：DVWA、Pikachu
* 辅助工具：Chrome、Burp Suite
* 测试方式：本地授权靶场测试

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

## 安全声明

本仓库仅用于本地授权靶场学习和安全能力建设。所有测试均在 DVWA、Pikachu 等合法授权环境中完成，不涉及真实业务系统、公网目标、第三方系统或任何未授权测试。

请勿将本项目中的测试方法用于未授权环境。
