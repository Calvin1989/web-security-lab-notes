# Web Security Lab Notes

本项目用于记录 Web 常见漏洞验证、安全测试流程和报告整理实践，主要面向安全服务、渗透测试辅助、Web 安全测试实习岗位。

## 项目内容

已整理以下漏洞类型的验证过程：

- SQL 注入
- XSS
- 文件上传
- 命令执行
- 目录遍历
- 弱口令
- 越权
- SSRF
- CSRF
- XXE
- PHP 反序列化

## 使用工具

- Burp Suite：抓包、重放、参数分析
- Nmap：端口与服务识别
- dirsearch：目录枚举
- SQLmap：SQL 注入辅助验证
- Nuclei：漏洞模板辅助检测
- Linux 基础命令：日志查看、文件操作、网络排查

## 输出内容

本项目按照安全测试报告思路整理：

1. 漏洞现象
2. 影响接口或参数
3. 验证过程
4. 关键请求与响应
5. 风险影响
6. 修复建议
7. 复测结论

## 示例报告

- [SQL 注入验证报告](./reports/sql_injection_report.md)
- [文件上传漏洞验证报告](./reports/file_upload_report.md)
- [越权漏洞验证报告](./reports/idor_report.md)

## 当前整理重点

当前阶段优先补充 3 篇最常见、最容易在面试中被追问的 Web 安全测试报告：SQL 注入、文件上传、越权漏洞。后续再逐步扩展 XSS、命令执行、目录遍历、弱口令、SSRF、CSRF、XXE、PHP 反序列化等内容。

## 目录结构

```text
web-security-lab-notes/
├── README.md
├── reports/
│   ├── sql_injection_report.md
│   ├── file_upload_report.md
│   └── idor_report.md
├── screenshots/
│   └── README.md
├── notes/
├── scan-results/
├── sample-logs/
├── summary/
└── tools/
```

## 截图证据

截图建议统一放在 `screenshots/` 目录中。每个漏洞保留 2-3 张关键证据即可，重点体现 Burp 请求包、响应差异、工具辅助验证结果和复测结论。

建议命名示例：

```text
sql_injection_request
sqlmap_validation_result
file_upload_burp_request
file_upload_response
idor_userid_replace
idor_response_compare
```

## 安全声明

本项目仅用于本地授权靶场、安全测试流程学习和报告整理实践。所有验证应在合法授权环境中完成，不得用于未授权系统、公网目标或真实业务攻击。
