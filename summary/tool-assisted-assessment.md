# 工具辅助安全评估报告



## 1. 测试说明



本报告用于记录在本地授权靶场环境中使用安全工具进行辅助识别、验证和结果复核的过程。



工具扫描结果仅作为信息收集和辅助判断依据，不直接等同于漏洞结论。最终漏洞确认仍以 Burp Suite 抓包、页面复现结果、源码或配置分析和人工复核为准。



## 2. Nmap 本地服务识别

### 2.1 测试目的

在 Kali 环境中使用 Nmap 对 Windows 本地靶场主机进行端口和服务识别，确认 DVWA、Pikachu 所在 Web 服务端口，并观察本地测试环境是否存在其他开放服务。

Nmap 在本项目中用于资产识别和服务枚举，不直接作为漏洞验证结论。后续漏洞确认仍需要结合 Burp Suite 抓包、页面复现结果、业务影响和人工分析完成。

### 2.2 测试目标

本次测试目标为本地授权靶场主机：

```text
192.168.5.14
```

测试环境说明：

* 扫描主机：Kali
* 目标主机：Windows 本地靶场
* 目标 IP：`192.168.5.14`
* 靶场服务：DVWA、Pikachu
* Web 服务端口：80
* 测试范围：本地授权靶场环境

### 2.3 连通性与 HTTP 基线验证

测试过程中，Kali 对 Windows 主机的 ICMP Ping 未收到响应，但 HTTP 请求可以正常访问靶场服务。因此后续 Nmap 扫描使用 `-Pn` 参数跳过主机发现，直接进行端口和服务识别。

DVWA 基线请求：

```text
curl -I http://192.168.5.14/dvwa/
```

结果显示 DVWA 返回 `302 Found`，并跳转到 `login.php`，说明 DVWA 服务可访问但需要登录。

Pikachu 基线请求：

```text
curl -I http://192.168.5.14/pikachu/
```

结果显示 Pikachu 返回 `200 OK`，说明 Pikachu 首页可以从 Kali 正常访问。

相关证据文件：

```text
scan-results/nmap/http-baseline-dvwa.txt
scan-results/nmap/http-baseline-pikachu.txt
scan-results/nmap/http-baseline-dvwa.png
scan-results/nmap/http-baseline-pikachu.png
```

### 2.4 端口与服务识别

执行命令：

```text
nmap -sV -Pn -p 80,443,3306,8080,8000,8888 192.168.5.14 -oN scan-results/nmap/local-service-scan.txt
```

扫描结果摘要：

| 端口       | 状态       | 服务             | 结果说明                                  |
| -------- | -------- | -------------- | ------------------------------------- |
| 80/tcp   | open     | http           | 本地 Web 靶场服务端口，DVWA 和 Pikachu 均通过该端口访问 |
| 3306/tcp | open     | mysql          | 本地 MySQL 数据库服务端口                      |
| 443/tcp  | filtered | https          | HTTPS 端口被过滤或未开放                       |
| 8000/tcp | filtered | http-alt       | 备用 Web 端口被过滤或未开放                      |
| 8080/tcp | filtered | http-proxy     | 备用 Web 端口被过滤或未开放                      |
| 8888/tcp | filtered | sun-answerbook | 备用端口被过滤或未开放                           |

相关证据文件：

```text
scan-results/nmap/local-service-scan.txt
scan-results/nmap/nmap-local-service-scan.png
```

### 2.5 HTTP 指纹识别

执行命令：

```text
nmap -Pn -p 80 --script http-title,http-server-header 192.168.5.14 -oN scan-results/nmap/http-fingerprint.txt
```

识别结果显示目标主机 80 端口运行 Apache Web 服务，并返回 phpstudy for Windows 相关页面标题。

HTTP 服务信息包括：

| 项目      | 识别结果                      |
| ------- | ------------------------- |
| Web 服务  | Apache httpd              |
| 操作系统环境  | Windows                   |
| OpenSSL | OpenSSL 1.1.1b            |
| PHP     | PHP 7.3.4                 |
| 页面标题    | phpstudy for Windows 相关页面 |

相关证据文件：

```text
scan-results/nmap/http-fingerprint.txt
scan-results/nmap/nmap-http-title.png
```

### 2.6 WhatWeb Web 指纹识别

为了补充 Web 指纹信息，使用 WhatWeb 对 DVWA 和 Pikachu 进行基础识别。

DVWA 指纹识别命令：

```text
whatweb http://192.168.5.14/dvwa/
```

Pikachu 指纹识别命令：

```text
whatweb http://192.168.5.14/pikachu/
```

识别结果显示：

| 目标      | 状态        | 识别信息                                        |
| ------- | --------- | ------------------------------------------- |
| DVWA    | 302 / 200 | Apache、PHP、DVWA、登录页面、Cookie、跳转到 `login.php` |
| Pikachu | 200       | Apache、PHP、Bootstrap、jQuery、Pikachu 页面标题    |

相关证据文件：

```text
scan-results/nmap/whatweb-dvwa.txt
scan-results/nmap/whatweb-pikachu.txt
scan-results/nmap/whatweb-dvwa.png
scan-results/nmap/whatweb-pikachu.png
```

其中公开展示前已对敏感信息进行打码处理。

### 2.7 结果分析

本阶段识别结果说明：

1. Kali 可以通过 HTTP 正常访问 Windows 本地靶场；
2. DVWA 返回 `302 Found` 并跳转到登录页，符合靶场登录逻辑；
3. Pikachu 返回 `200 OK`，首页可直接访问；
4. 目标主机 80 端口开放，运行 Apache Web 服务；
5. 目标主机 3306 端口开放，识别为 MySQL 服务；
6. 443、8000、8080、8888 等端口处于 filtered 状态；
7. HTTP 响应头和指纹识别结果暴露了 Apache、PHP、OpenSSL、phpstudy 等环境信息。

需要注意的是，端口开放和服务指纹暴露不等同于漏洞成立。真实安全评估中，应结合授权范围、访问控制、服务暴露面、版本信息和业务场景进行进一步人工判断。

### 2.8 后续测试映射

| 发现项                      | 说明             | 后续验证方向                                |
| ------------------------ | -------------- | ------------------------------------- |
| 80/tcp open              | Web 服务开放       | 访问 DVWA / Pikachu，进行 Web 漏洞手工验证       |
| DVWA 可访问                 | 返回 302 并跳转到登录页 | 登录后进行 SQL 注入、XSS、文件上传、命令执行、目录遍历、弱口令测试 |
| Pikachu 可访问              | 返回 200 OK      | 进行越权、SSRF、CSRF、XXE、PHP 反序列化测试         |
| 3306/tcp open            | MySQL 服务开放     | 在真实环境中应检查数据库端口是否限制访问来源                |
| Server / X-Powered-By 可见 | 暴露 Web 服务组件信息  | 作为信息收集结果，结合版本和配置进行人工判断                |
| phpstudy 指纹可见            | 暴露本地 Web 环境特征  | 在真实环境中应减少不必要的服务指纹暴露                   |

### 2.9 小结

本阶段通过 Nmap、curl 和 WhatWeb 完成了本地靶场的服务识别和 Web 指纹确认。

该阶段形成的结论是：目标主机存在可访问的 Web 服务，DVWA 和 Pikachu 均可从 Kali 访问，MySQL 服务端口处于开放状态，HTTP 响应中可识别 Apache、PHP、OpenSSL 和 phpstudy 等环境信息。

这些结果为后续目录扫描、SQLmap 辅助验证和手工漏洞复现提供了资产范围和基础信息。


## 3. 目录扫描与敏感路径识别

### 3.1 测试目的

在本地授权靶场环境中，使用 dirsearch 对 DVWA 进行路径枚举，识别登录入口、初始化页面、上传目录、漏洞模块目录、项目说明文件和可能需要人工复核的路径。

目录扫描结果仅作为信息收集线索，不直接等同于漏洞结论。对于扫描发现的路径，需要结合状态码、响应内容、访问权限、业务功能和是否泄露敏感信息进行人工复核。

### 3.2 测试目标

本次测试目标为本地授权靶场中的 DVWA：

```text
http://192.168.5.14/dvwa/
```

测试环境说明：

* 扫描主机：Kali
* 目标主机：Windows 本地靶场
* 目标 IP：`192.168.5.14`
* 工具：dirsearch
* 测试范围：本地授权靶场 DVWA

### 3.3 测试命令

为了避免默认大字典产生大量无意义结果，本次使用小字典进行聚焦扫描。

```text
dirsearch -u http://192.168.5.14/dvwa/ -w dvwa-small-wordlist.txt -e php,txt,html,js -x 404 -o scan-results/dirscan/dvwa-dirsearch-focused.txt
```

人工复核重点路径时使用以下命令：

```text
curl -I http://192.168.5.14/dvwa/login.php
curl -I http://192.168.5.14/dvwa/setup.php
curl -I http://192.168.5.14/dvwa/hackable/uploads/
curl -I http://192.168.5.14/dvwa/.dockerignore
```

### 3.4 扫描结果摘要

本次聚焦扫描发现以下重点路径：

| 路径                            |      状态码 | 结果说明                    |
| ----------------------------- | -------: | ----------------------- |
| `/dvwa/login.php`             |      200 | 登录入口可访问                 |
| `/dvwa/setup.php`             |      200 | 初始化 / 配置页面可访问           |
| `/dvwa/README.md`             |      200 | 项目说明文件可访问               |
| `/dvwa/.dockerignore`         |      200 | 项目辅助文件可访问               |
| `/dvwa/config/config.inc.php` | 200 / 0B | 配置文件路径可访问，但响应体为空，需要人工复核 |
| `/dvwa/robots.txt`            |      200 | robots 文件可访问            |
| `/dvwa/hackable/uploads/`     |      403 | 上传目录存在，但目录索引被禁止         |
| `/dvwa/vulnerabilities/`      |      403 | 漏洞模块目录存在，但目录索引被禁止       |
| `/dvwa/config/`               |      403 | 配置目录存在，但目录索引被禁止         |
| `/dvwa/docs/`                 |      403 | 文档目录存在，但目录索引被禁止         |
| `/dvwa/tests/`                |      403 | 测试目录存在，但目录索引被禁止         |
| `/dvwa/external/`             |      403 | 第三方依赖目录存在，但目录索引被禁止      |
| `/dvwa/.github/`              |      403 | GitHub 配置目录存在，但目录索引被禁止  |

### 3.5 人工复核结果

对扫描发现的重点路径进行人工复核，结果如下：

| 路径                        | 复核结果          | 说明                              |
| ------------------------- | ------------- | ------------------------------- |
| `/dvwa/login.php`         | 200 OK        | 登录页面可访问，可作为后续弱口令和认证测试入口         |
| `/dvwa/setup.php`         | 200 OK        | 初始化页面可访问，真实环境中应避免暴露             |
| `/dvwa/hackable/uploads/` | 403 Forbidden | 上传目录存在，但不允许列目录，可与文件上传漏洞复现进行关联分析 |
| `/dvwa/.dockerignore`     | 200 OK        | 项目辅助文件可访问，真实环境中应避免暴露此类文件        |

### 3.6 结果分析

本次目录扫描发现了多个有价值的信息收集结果。

`login.php` 表明 DVWA 登录入口可访问，可作为后续认证测试、弱口令验证和登录防护分析入口。

`setup.php` 是 DVWA 初始化页面。在本地靶场中属于正常现象，但在真实生产环境中，如果初始化页面对外暴露，可能带来配置重置、环境信息泄露或误操作风险。

`README.md` 和 `.dockerignore` 属于项目说明或辅助文件。在靶场环境中用于学习和部署说明，但在真实业务系统中，公开暴露项目辅助文件可能泄露目录结构、部署方式或技术栈信息。

`hackable/uploads/` 返回 403，说明上传目录存在，但服务器禁止目录索引。这不能直接判定为漏洞，但可以与文件上传漏洞复现结果关联分析：如果上传后的文件可以被直接访问或执行，仍然存在风险。

`config/config.inc.php` 返回 200 但响应体为 0B，不能直接判定为配置泄露。该结果需要结合响应内容、服务端 PHP 解析配置和访问权限进一步人工复核。

### 3.7 安全意义

目录扫描可以帮助识别隐藏路径和潜在攻击面，例如登录入口、上传目录、配置目录、初始化页面、项目说明文件等。

但目录扫描结果不能直接作为漏洞结论。真实安全评估中，需要进一步判断：

* 路径是否需要认证；
* 是否泄露敏感信息；
* 是否允许未授权访问；
* 是否存在目录索引；
* 是否能与文件上传、目录遍历、弱口令等漏洞形成关联；
* 是否属于靶场环境中的正常暴露。

### 3.8 证据文件

本阶段相关证据文件如下：

```text
scan-results/dirscan/dvwa-dirsearch-focused.txt
scan-results/dirscan/dvwa-path-review.txt
scan-results/dirscan/dirsearch-dvwa-focused-result.png
scan-results/dirscan/dirsearch-dvwa-path-review.png
```

### 3.9 小结

本阶段通过 dirsearch 完成了 DVWA 靶场的聚焦目录扫描，并对重点路径进行了人工复核。扫描结果为后续手工漏洞验证提供了路径线索，同时体现了“工具发现线索，人工确认风险”的安全评估思路。


## 4. SQLmap 辅助验证 SQL 注入

### 4.1 测试目的

在本地授权 DVWA 靶场环境中，先通过 Burp Suite 和手工测试确认 SQL 注入点，再使用 SQLmap 对同一注入点进行辅助验证，观察自动化工具对注入参数、注入类型、数据库类型和当前数据库名的识别结果。

SQLmap 在本项目中仅用于本地靶场辅助验证，不用于未授权目标测试，不进行敏感数据导出。

### 4.2 测试目标

本次测试目标为 DVWA SQL Injection 模块中的 `id` 参数：

```text
http://192.168.5.14/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit
```

测试前已确认：

* Kali 可以访问 DVWA；
* DVWA 已登录；
* DVWA 安全等级为 Low；
* `id` 参数已通过手工方式验证存在 SQL 注入风险。

### 4.3 测试命令

实际运行时使用有效的本地靶场 Cookie。提交到项目文档时，Cookie 已进行打码处理。

```text
sqlmap -u "http://192.168.5.14/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=***; security=low" --batch --level=1 --risk=1 -p id --dbms=mysql --current-db --flush-session -o
```

### 4.4 验证结果

SQLmap 识别到 GET 参数 `id` 存在 SQL 注入风险。

识别到的注入类型包括：

| 注入类型                | 说明         |
| ------------------- | ---------- |
| boolean-based blind | 布尔盲注       |
| error-based         | 报错注入       |
| time-based blind    | 时间盲注       |
| UNION query         | UNION 查询注入 |

SQLmap 同时识别出以下信息：

| 项目       | 结果                     |
| -------- | ---------------------- |
| 注入参数     | `id`                   |
| 参数位置     | GET                    |
| 后端数据库    | MySQL                  |
| Web 服务环境 | Windows / Apache / PHP |
| 当前数据库    | `dvwa`                 |

### 4.5 结果分析

本次 SQLmap 辅助验证结果与前期手工验证结论一致：DVWA Low 模式下 SQL Injection 模块的 `id` 参数存在 SQL 注入风险。

需要注意的是，SQLmap 输出结果只能作为辅助验证依据。真实安全评估中，不能只依赖工具结论，还需要结合页面响应、Burp 抓包、业务影响、数据敏感性和修复建议进行人工判断。

本次测试仅获取当前数据库名 `dvwa`，未进行数据表枚举、数据导出或敏感数据读取。

### 4.6 证据文件

本阶段相关证据文件如下：

```text
scan-results/sqlmap/dvwa-sqli-verify.txt
scan-results/sqlmap/sqlmap-dvwa-current-db.png
```

### 4.7 小结

本阶段通过 SQLmap 对已手工确认的 SQL 注入点进行了辅助验证。工具结果进一步确认了 `id` 参数存在 SQL 注入风险，并识别出后端数据库类型和当前数据库名。

该阶段体现了“手工验证为主，工具辅助复核”的安全评估思路。
