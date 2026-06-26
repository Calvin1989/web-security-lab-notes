# Web Access Log 风险摘要

- 日志文件：`sample-logs\access-demo.log`
- 总行数：35

## 1. 风险等级统计

| 风险等级 | 命中次数 |
|---|---|
| High | 11 |
| Medium | 7 |

## 2. 风险类型统计

| 风险类型 | 命中次数 |
|---|---|
| Brute Force | 5 |
| Directory Traversal | 4 |
| SQL Injection | 2 |
| XSS | 2 |
| XXE | 2 |
| Sensitive File Upload | 1 |
| Command Injection | 1 |
| SSRF | 1 |

## 3. Top 来源 IP

| IP | 请求次数 |
|---|---|
| 192.168.5.32 | 6 |
| 192.168.5.21 | 4 |
| 192.168.5.20 | 3 |
| 192.168.5.22 | 3 |
| 192.168.5.25 | 3 |
| 192.168.5.26 | 3 |
| 192.168.5.23 | 2 |
| 192.168.5.24 | 2 |
| 192.168.5.27 | 2 |
| 192.168.5.28 | 2 |

## 4. 风险样例

### Brute Force

- 风险等级：Medium
- 来源 IP：`192.168.5.20`

```text
192.168.5.20 - - [26/Jun/2026:10:00:05 +0800] "GET /dvwa/login.php HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
```

- 风险等级：Medium
- 来源 IP：`192.168.5.20`

```text
192.168.5.20 - - [26/Jun/2026:10:00:12 +0800] "POST /dvwa/login.php HTTP/1.1" 302 512 "http://192.168.5.14/dvwa/login.php" "Mozilla/5.0"
```

- 风险等级：Medium
- 来源 IP：`192.168.5.26`

```text
192.168.5.26 - - [26/Jun/2026:10:06:01 +0800] "GET /dvwa/vulnerabilities/brute/?username=admin&password=123456&Login=Login HTTP/1.1" 200 1100 "-" "Mozilla/5.0"
```

### SQL Injection

- 风险等级：High
- 来源 IP：`192.168.5.21`

```text
192.168.5.21 - - [26/Jun/2026:10:01:18 +0800] "GET /dvwa/vulnerabilities/sqli/?id=1%27%20OR%20%271%27%3D%271&Submit=Submit HTTP/1.1" 200 4300 "-" "Mozilla/5.0"
```

- 风险等级：High
- 来源 IP：`192.168.5.21`

```text
192.168.5.21 - - [26/Jun/2026:10:01:25 +0800] "GET /dvwa/vulnerabilities/sqli/?id=1%27%20UNION%20SELECT%201,2--%20-&Submit=Submit HTTP/1.1" 200 3900 "-" "sqlmap/1.8"
```

### XSS

- 风险等级：Medium
- 来源 IP：`192.168.5.22`

```text
192.168.5.22 - - [26/Jun/2026:10:02:12 +0800] "GET /dvwa/vulnerabilities/xss_r/?name=%3Cscript%3Ealert(1)%3C/script%3E HTTP/1.1" 200 1700 "-" "Mozilla/5.0"
```

- 风险等级：Medium
- 来源 IP：`192.168.5.22`

```text
192.168.5.22 - - [26/Jun/2026:10:02:18 +0800] "GET /dvwa/vulnerabilities/xss_r/?name=%3Cimg%20src=x%20onerror=alert(1)%3E HTTP/1.1" 200 1750 "-" "Mozilla/5.0"
```

### Sensitive File Upload

- 风险等级：High
- 来源 IP：`192.168.5.23`

```text
192.168.5.23 - - [26/Jun/2026:10:03:18 +0800] "GET /dvwa/hackable/uploads/upload-test.php HTTP/1.1" 200 64 "-" "Mozilla/5.0"
```

### Command Injection

- 风险等级：High
- 来源 IP：`192.168.5.24`

```text
192.168.5.24 - - [26/Jun/2026:10:04:10 +0800] "GET /dvwa/vulnerabilities/exec/?ip=127.0.0.1%20%26%20whoami&Submit=Submit HTTP/1.1" 200 2500 "-" "Mozilla/5.0"
```

### Directory Traversal

- 风险等级：High
- 来源 IP：`192.168.5.25`

```text
192.168.5.25 - - [26/Jun/2026:10:05:10 +0800] "GET /dvwa/vulnerabilities/fi/?page=../../hackable/uploads/read-test.txt HTTP/1.1" 200 900 "-" "Mozilla/5.0"
```

- 风险等级：High
- 来源 IP：`192.168.5.25`

```text
192.168.5.25 - - [26/Jun/2026:10:05:16 +0800] "GET /dvwa/vulnerabilities/fi/?page=../../../../etc/passwd HTTP/1.1" 200 1200 "-" "Mozilla/5.0"
```

- 风险等级：High
- 来源 IP：`192.168.5.28`

```text
192.168.5.28 - - [26/Jun/2026:10:08:10 +0800] "GET /pikachu/vul/ssrf/ssrf_curl.php?url=file:///etc/passwd HTTP/1.1" 200 1200 "-" "Mozilla/5.0"
```

### SSRF

- 风险等级：High
- 来源 IP：`192.168.5.28`

```text
192.168.5.28 - - [26/Jun/2026:10:08:01 +0800] "GET /pikachu/vul/ssrf/ssrf_curl.php?url=http://127.0.0.1/pikachu/ HTTP/1.1" 200 2200 "-" "Mozilla/5.0"
```

### XXE

- 风险等级：High
- 来源 IP：`192.168.5.28`

```text
192.168.5.28 - - [26/Jun/2026:10:08:10 +0800] "GET /pikachu/vul/ssrf/ssrf_curl.php?url=file:///etc/passwd HTTP/1.1" 200 1200 "-" "Mozilla/5.0"
```

- 风险等级：High
- 来源 IP：`192.168.5.30`

```text
192.168.5.30 - - [26/Jun/2026:10:10:08 +0800] "POST /pikachu/vul/xxe/xxe_1.php HTTP/1.1" 200 2300 "-" "Mozilla/5.0 XXE SYSTEM file"
```

## 5. 说明

本脚本基于关键字和正则表达式进行基础风险识别，结果只能作为初步研判线索。真实安全运营场景中，应结合请求上下文、响应状态码、响应大小、账号身份、访问频率、业务接口含义和历史基线进行综合分析。