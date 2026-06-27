# Web Security Lab Notes

本项目基于 DVWA、Pikachu 等本地授权靶场，记录 Web 常见漏洞的手工验证、Burp 抓包分析、修复建议、工具辅助评估和日志分析扩展。

项目定位是安全服务交付与 Web 安全测试实践：不只复现漏洞，也关注证据链、风险判断、整改建议和复测思路。

## 快速查看

如果需要快速了解项目，可以优先查看：

- [Web 系统安全评估模拟报告](./summary/web-security-assessment-report.md)：从安全服务交付角度汇总漏洞、风险和整改建议
- [SQL 注入漏洞报告](./reports/01-sql-injection.md)：展示手工验证、Burp 抓包和复测过程
- [文件上传漏洞报告](./reports/03-file-upload.md)：展示上传链路验证和修复建议
- [工具辅助安全评估报告](./summary/tool-assisted-assessment.md)：展示 Nmap、dirsearch、SQLmap、Nuclei 的辅助使用和人工复核
- [Web 攻击日志分析案例](./notes/log-analysis-case-study.md)：展示 access log 中攻击特征提取和安全运营研判思路

## 项目亮点

- 覆盖 11 类常见 Web 漏洞，均限定在本地授权靶场中完成。
- 每类漏洞按报告思路整理：漏洞现象、关键请求、风险影响、修复建议和复测结论。
- 使用 Burp Suite 保留关键请求证据，强调手工验证与人工复核。
- 补充 Nmap、dirsearch、SQLmap、Nuclei 的工具辅助评估流程。
- 增加 access log 风险摘要脚本和日志分析案例，将漏洞复现延伸到安全运营研判。

## 核心交付物

| 类型 | 文件 |
|---|---|
| 模拟安全评估总报告 | [`summary/web-security-assessment-report.md`](./summary/web-security-assessment-report.md) |
| 项目复盘 | [`summary/project-review.md`](./summary/project-review.md) |
| 工具辅助评估 | [`summary/tool-assisted-assessment.md`](./summary/tool-assisted-assessment.md) |
| 日志分析案例 | [`notes/log-analysis-case-study.md`](./notes/log-analysis-case-study.md) |
| 日志风险摘要脚本 | [`tools/access-log-risk-summary.py`](./tools/access-log-risk-summary.py) |
| 修复建议速查 | [`notes/remediation-cheatsheet.md`](./notes/remediation-cheatsheet.md) |
| 日志检测速查 | [`notes/log-detection-cheatsheet.md`](./notes/log-detection-cheatsheet.md) |

## 已完成漏洞报告

| 序号 | 漏洞类型 | 报告 |
|---|---|---|
| 01 | SQL 注入 | [`reports/01-sql-injection.md`](./reports/01-sql-injection.md) |
| 02 | XSS | [`reports/02-xss.md`](./reports/02-xss.md) |
| 03 | 文件上传 | [`reports/03-file-upload.md`](./reports/03-file-upload.md) |
| 04 | 命令执行 | [`reports/04-command-injection.md`](./reports/04-command-injection.md) |
| 05 | 目录遍历 / 任意文件读取 | [`reports/05-directory-traversal.md`](./reports/05-directory-traversal.md) |
| 06 | 弱口令 / 暴力破解 | [`reports/06-weak-password.md`](./reports/06-weak-password.md) |
| 07 | 水平越权 | [`reports/07-access-control.md`](./reports/07-access-control.md) |
| 08 | SSRF | [`reports/08-ssrf.md`](./reports/08-ssrf.md) |
| 09 | CSRF | [`reports/09-csrf.md`](./reports/09-csrf.md) |
| 10 | XXE | [`reports/10-xxe.md`](./reports/10-xxe.md) |
| 11 | PHP 反序列化 | [`reports/11-deserialization.md`](./reports/11-deserialization.md) |

## 工具辅助评估

工具仅用于信息收集、辅助验证和结果复核，不直接替代漏洞结论。

- Nmap：本地服务识别与 HTTP 指纹确认
- dirsearch：目录枚举与敏感路径人工复核
- SQLmap：对已手工确认的 SQL 注入点进行辅助验证
- Nuclei：基础模板扫描与结果人工复核

详细过程见 [`summary/tool-assisted-assessment.md`](./summary/tool-assisted-assessment.md)。

## 日志分析扩展

项目补充了 `access-log-risk-summary.py`，用于从 access log 中提取 SQL 注入、XSS、目录遍历、命令执行、SSRF、XXE、反序列化等攻击特征，并生成 Markdown 风险摘要。

相关材料：

- [`tools/access-log-risk-summary.py`](./tools/access-log-risk-summary.py)
- [`sample-logs/access-demo.log`](./sample-logs/access-demo.log)
- [`summary/log-risk-summary.md`](./summary/log-risk-summary.md)
- [`notes/log-analysis-case-study.md`](./notes/log-analysis-case-study.md)

## 安全声明

本项目仅用于本地授权靶场、安全测试流程学习和报告整理实践。所有验证均应在合法授权环境中完成，不得用于未授权系统、公网目标或真实业务攻击。
