# Web Access Log 风险摘要

- 日志文件：`sample-logs\access-demo.log`
- 总行数：8

## 1. 风险等级统计

| 风险等级 | 命中次数 |
|---|---|
| High | 3 |
| Medium | 2 |

## 2. 风险类型统计

| 风险类型 | 命中次数 |
|---|---|
| XSS | 2 |
| Directory Traversal | 1 |
| SSRF | 1 |
| XXE | 1 |

## 3. Top 来源 IP

| IP | 请求次数 |
|---|---|
| 127.0.0.1 | 8 |

## 4. 风险样例

### XSS

- 风险等级：Medium
- 来源 IP：`127.0.0.1`

```text
127.0.0.1 - - [25/Jun/2026:10:01:02 +0800] "GET /dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E HTTP/1.1" 200 900 "-" "Mozilla/5.0"
```

- 风险等级：Medium
- 来源 IP：`127.0.0.1`

```text
127.0.0.1 - - [25/Jun/2026:10:06:07 +0800] "POST /pikachu/vul/unserilization/unser.php HTTP/1.1" 200 700 "-" "Mozilla/5.0" "o=O:1:\"S\":1:{s:4:\"test\";s:29:\"<script>alert('xss')</script>\";}"
```

### Directory Traversal

- 风险等级：High
- 来源 IP：`127.0.0.1`

```text
127.0.0.1 - - [25/Jun/2026:10:02:03 +0800] "GET /dvwa/vulnerabilities/fi/?page=../../hackable/uploads/read-test.txt HTTP/1.1" 200 800 "-" "Mozilla/5.0"
```

### SSRF

- 风险等级：High
- 来源 IP：`127.0.0.1`

```text
127.0.0.1 - - [25/Jun/2026:10:04:05 +0800] "GET /pikachu/vul/ssrf/ssrf_curl.php?url=http://127.0.0.1/pikachu/ HTTP/1.1" 200 1500 "-" "Mozilla/5.0"
```

### XXE

- 风险等级：High
- 来源 IP：`127.0.0.1`

```text
127.0.0.1 - - [25/Jun/2026:10:05:06 +0800] "POST /pikachu/vul/xxe/xxe_1.php HTTP/1.1" 200 700 "-" "Mozilla/5.0" "xml=<?xml version='1.0'?><!DOCTYPE note [<!ENTITY xxe SYSTEM 'file:///C:/data/phpstudy_pro/WWW/pikachu/xxe-test.txt'>]><name>&xxe;</name>"
```

## 5. 说明

本脚本基于关键字和正则表达式进行基础风险识别，结果只能作为初步研判线索。真实安全运营场景中，应结合请求上下文、响应状态码、响应大小、账号身份、访问频率、业务接口含义和历史基线进行综合分析。